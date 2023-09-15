import json

from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView, ListView

from progress.models import ProgressTest, ProgressTestAnswers
from progress.views.progress_test_answers_view import create_progress_tests_answers
from progress.views.progress_test_view import create_progress_test
from test_bim.models import TestBim, QuestionBim, AnswerBim


class TakeTestView(DetailView):
    queryset = TestBim.objects.all()
    template_name = "tests_bim/take_test/take_test.html"
    context_object_name = 'test'

    def post(self, request, pk, *args, **kwargs):
        progress_test = ProgressTest.objects.filter(test_id=pk, user_id=request.user.pk)
        if not progress_test:
            progress_test = create_progress_test(user=request.user, test=self.get_object())
        return redirect("test_bim:test_completion", pk=progress_test[0].pk)


class QuestionsCompletionView(ListView):
    paginate_by = 1
    context_object_name = "question"
    template_name = "tests_bim/take_test/questions_completion.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        pk = self.kwargs.get("pk")
        context["progress_test_id"] = pk
        context["user_answers_id"] = ProgressTest.objects.get(id=pk).user_progress.values_list("answer_id", flat=True)
        return context

    def get_queryset(self):
        progress_test = get_object_or_404(ProgressTest, pk=self.kwargs.get("pk"))
        return QuestionBim.objects.filter(test_bim_id=progress_test.test.pk)


class UserAnswerAPIView(View):

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
