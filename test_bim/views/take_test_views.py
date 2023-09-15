from django.shortcuts import redirect, get_object_or_404
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
        if progress_test:
            progress_test = create_progress_test(user=request.user, test=self.get_object())
        return redirect("test_bim:test_completion", pk=progress_test[0].pk)


class QuestionsCompletionView(ListView):
    paginate_by = 1
    context_object_name = "question"
    template_name = "tests_bim/take_test/questions_completion.html"

    def post(self, request, pk, *args, **kwargs):
        test = ProgressTest.objects.get(id=pk)
        answer_id = request.POST.get("answer")

        # Если пользователь не выбирал ответ
        if not answer_id:
            page = request.GET.get('page')
            # Редирект на текущею страницу или в начало
            url = request.path + f"?page={int(page) - 1}" if page and int(page) > 0 else request.path
            return redirect(url)
        answer = AnswerBim.objects.get(id=answer_id)

        # Если еще не отвечал
        if not ProgressTestAnswers.objects.filter(progress_test_id=pk, question=answer.question_bim):
            create_progress_tests_answers(progress_test=test, question=answer.question_bim, answer=answer)
        else:
            user_answer = ProgressTestAnswers.objects.get(progress_test_id=pk, question=answer.question_bim)
            # Перезаписать ответ
            user_answer.answer = answer
            user_answer.save()

        return self.get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context["user_answers_id"] = ProgressTest.objects.get(id=self.kwargs.get("pk")).user_progress.values_list("answer_id", flat=True)
        return context

    def get_queryset(self):
        progress_test = get_object_or_404(ProgressTest, pk=self.kwargs.get("pk"))
        return QuestionBim.objects.filter(test_bim_id=progress_test.test.pk)
