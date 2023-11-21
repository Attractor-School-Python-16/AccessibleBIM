from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView, ListView

from progress.models import ProgressTest, ProgressTestAnswers
from progress.views.progress_test_answers_view import create_progress_tests_answers
from progress.views.progress_test_view import create_progress_test
from quiz_bim.models import QuizBim, QuestionBim, AnswerBim
from modules.models.user_course_progress import UserCourseProgress
from django.utils import timezone
from django.urls import reverse


class TakeQuizView(LoginRequiredMixin, DetailView):
    queryset = QuizBim.objects.all()
    template_name = "quiz_bim/take_quiz/take_test.html"
    context_object_name = 'test'

    def post(self, request, pk, *args, **kwargs):
        if not ProgressTest.objects.filter(test_id=pk, user_id=request.user.pk):
            progress_test = create_progress_test(user=request.user, test=self.get_object())
        else:
            progress_test = ProgressTest.objects.get(test_id=pk, user_id=request.user.pk)
        if progress_test.is_passed:
            if self.request.user.groups.filter(name='moderators').exists() or self.request.user.is_superuser:
                progress_test.in_progress = True
                progress_test.is_passed = False
                progress_test.save()
                progress_test.user_progress.all().delete()
            else:
                return redirect("quiz_bim:test_result", pk=progress_test.pk)
        if not progress_test.is_passed and progress_test.test.questions_qty == progress_test.user_progress.count() and \
                not progress_test.in_progress:
            progress_test.in_progress = True
            progress_test.save()
            progress_test.user_progress.all().delete()
        return redirect("quiz_bim:test_completion", pk=progress_test.pk)


class QuestionsCompletionView(UserPassesTestMixin, ListView):
    context_object_name = "questions"
    template_name = "quiz_bim/take_quiz/questions_completion.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        progress = ProgressTest.objects.get(id=self.kwargs.get("pk"))
        context["progress_test_id"] = progress.pk
        context["quiz_title"] = progress.test.title
        context["user_answers_id"] = progress.user_progress.values_list("answer_id", flat=True)
        return context

    def get_queryset(self):
        progress_test = get_object_or_404(ProgressTest, pk=self.kwargs.get("pk"))
        return QuestionBim.objects.filter(test_bim_id=progress_test.test.pk)

    def test_func(self):
        progress_test = get_object_or_404(ProgressTest, pk=self.kwargs.get("pk"))
        return self.request.user == progress_test.user


# TODO: Желательно переместить API представления в соответствующее приложение
class UserAnswerAPIView(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        answer_id = list(request.POST.values())[0]
        test = get_object_or_404(ProgressTest, pk=pk)
        answer = get_object_or_404(AnswerBim, pk=answer_id)
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


class QuizResultView(UserPassesTestMixin, DetailView):
    queryset = ProgressTest.objects.all()
    template_name = "quiz_bim/take_quiz/test_result.html"
    context_object_name = 'progress'

    def get(self, request, *args, **kwargs):
        progress = self.get_object()
        if progress.user_progress.count() != progress.test.question_bim.count():
            return redirect("quiz_bim:test_completion", pk=progress.pk)
        return super().get(request, *args, **kwargs)

    def post(self, request, pk, *args, **kwargs):
        # TODO: Нужно будет явно уточнить пользователю что он еще не ответил на все вопросы
        # Если пользователь еще не ответил на все вопросы то его перекидывает в начало теста
        progress = self.get_object()
        if not progress.is_passed and progress.user_progress.count() == progress.test.question_bim.count():
            progress.end_time = timezone.now()
            progress.is_passed = (progress.accuracy() >= 0.75)
            progress.save()
            progress.in_progress = False
            progress.save()
            progress_chapter = UserCourseProgress.objects.filter(user=self.request.user,
                                                                 status=0,
                                                                 step__test__progress=self.get_object())
            if progress_chapter and progress.is_passed:
                progress_chapter[0].status = 1
                progress_chapter[0].save()
            # return redirect("quiz_bim:test_result", pk=progress.pk)
            return HttpResponse(status=200)
        return redirect("quiz_bim:test_completion", pk=pk)

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_answers_id"] = self.get_object().user_progress.values_list("answer_id", flat=True)
        context["questions"] = QuestionBim.objects.filter(test_bim_id=self.get_object().test.pk)
        if self.request.user.groups.filter(name='moderators').exists() or self.request.user.is_superuser:
            context["is_moderator"] = True
        return context
