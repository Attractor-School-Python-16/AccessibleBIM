from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView

from quiz_bim.models import QuizBim
from quiz_bim.models.question_bim import QuestionBim
from quiz_bim.forms.question_bim_form import QuestionBimForm


class QuestionBimDetailView(DetailView):
    queryset = QuestionBim.objects.all()
    template_name = "quiz_bim/question_bim/question_bim_detail.html"
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        answers = self.object.answer_bim.all()
        kwargs['answers'] = answers
        return super().get_context_data(**kwargs)


class QuestionBimCreateView(CreateView):
    form_class = QuestionBimForm
    template_name = "quiz_bim/question_bim/question_bim_create.html"

    def form_valid(self, form):
        test = get_object_or_404(QuizBim, pk=self.kwargs.get("pk"))
        question = form.save(commit=False)
        question.test_bim = test
        question.save()
        return redirect("quiz_bim:test_detail", pk=test.pk)


class QuestionBimUpdateView(UpdateView):
    model = QuestionBim
    form_class = QuestionBimForm
    template_name = 'quiz_bim/question_bim/question_bim_update.html'
    success_url = reverse_lazy('quiz_bim:tests_list')
    context_object_name = 'question'


class QuestionBimDeleteView(DeleteView):
    model = QuestionBim
    context_object_name = 'question'
    template_name = 'quiz_bim/question_bim/question_bim_delete.html'
    success_url = reverse_lazy('quiz_bim:tests_list')
