from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView, ListView

from progress.models import ProgressTest
from progress.views.progress_test_view import create_progress_test
from test_bim.models import TestBim, QuestionBim


class TakeTestView(DetailView):
    queryset = TestBim.objects.all()
    template_name = "tests_bim/take_test/take_test.html"
    context_object_name = 'test'

    def post(self, request, pk, *args, **kwargs):
        progress_test = create_progress_test(user=request.user, test=self.get_object())
        return redirect("test_bim:test_completion", pk=progress_test.pk)


class QuestionsCompletionView(ListView):
    paginate_by = 1
    context_object_name = "question"
    template_name = "tests_bim/take_test/questions_completion.html"

    def get_queryset(self):
        progress_test = get_object_or_404(ProgressTest, pk=self.kwargs.get("pk"))
        return QuestionBim.objects.filter(test_bim_id=progress_test.test.pk)
