import json
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView, ListView

from progress.models import ProgressTest, ProgressTestAnswers
from progress.views.progress_test_answers_view import create_progress_tests_answers
from progress.views.progress_test_view import create_progress_test
from quiz_bim.models import QuizBim, QuestionBim, AnswerBim


class TakeTestView(LoginRequiredMixin, DetailView):
    queryset = QuizBim.objects.all()
    template_name = "quiz_bim/take_test/take_test.html"
    context_object_name = 'test'

    def post(self, request, pk, *args, **kwargs):
        if not ProgressTest.objects.filter(test_id=pk, user_id=request.user.pk):
            progress_test = create_progress_test(user=request.user, test=self.get_object())
        else:
            progress_test = ProgressTest.objects.get(test_id=pk, user_id=request.user.pk)
        return redirect("quiz_bim:test_completion", pk=progress_test.pk)


class QuestionsCompletionView(LoginRequiredMixin, ListView):
    paginate_by = 1
    context_object_name = "question"
    template_name = "quiz_bim/take_test/questions_completion.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        pk = self.kwargs.get("pk")
        context["progress_test_id"] = pk
        context["user_answers_id"] = ProgressTest.objects.get(id=pk).user_progress.values_list("answer_id", flat=True)
        return context

    def get_queryset(self):
        progress_test = get_object_or_404(ProgressTest, pk=self.kwargs.get("pk"))
        return QuestionBim.objects.filter(test_bim_id=progress_test.test.pk)


# TODO: Желательно нужно будет переместить API представления в соответствующее приложение
class UserAnswerAPIView(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        body = json.loads(request.body)
        test = get_object_or_404(ProgressTest, pk=pk)
        answer = get_object_or_404(AnswerBim, pk=body.get("answer_id"))
        question = answer.question_bim

        # Если еще не отвечал
        if not ProgressTestAnswers.objects.filter(progress_test_id=pk, question=question):
            create_progress_tests_answers(progress_test=test, question=question, answer=answer)
        else:
            user_answer = ProgressTestAnswers.objects.get(progress_test_id=pk, question=answer.question_bim)
            # Перезаписать ответ
            user_answer.answer = answer
            user_answer.save()

        return HttpResponse(status=200)


class TestResultView(LoginRequiredMixin, DetailView):
    queryset = ProgressTest.objects.all()
    template_name = "quiz_bim/take_test/test_result.html"
    context_object_name = 'progress'

    def get(self, request, *args, **kwargs):
        progress = self.get_object()
        if progress.user_progress.count() != progress.test.questions_qty:
            return redirect("quiz_bim:test_completion", pk=progress.pk)
        return super().get(request, *args, **kwargs)

    def post(self, request, pk, *args, **kwargs):
        # Если пользователь еще не ответил на все вопросы то его перекидывает в начало теста
        # TODO: Нужно будет явно уточнить пользователю что он еще не ответи на все вопросы
        progress = self.get_object()
        if progress.user_progress.count() == progress.test.questions_qty:
            progress.end_time = datetime.now()
            progress.is_passed = (progress.accuracy() > 0.75)
            progress.save()
            return redirect("quiz_bim:test_result", pk=progress.pk)
        return redirect("quiz_bim:test_completion", pk=pk)
