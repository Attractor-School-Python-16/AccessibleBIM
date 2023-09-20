from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView, CreateView

from quiz_bim.models import QuestionBim
from quiz_bim.models.answer_bim import AnswerBim
from quiz_bim.forms.answer_bim_form import AnswerBimForm


class AnswerBimCreateView(PermissionRequiredMixin, CreateView):
    form_class = AnswerBimForm
    template_name = "quiz_bim/answer_bim/answer_bim_create.html"
    permission_required = 'quiz_bim.add_answerbim'

    def form_valid(self, form):
        question = get_object_or_404(QuestionBim, pk=self.kwargs.get("pk"))
        answer = form.save(commit=False)
        answer.question_bim = question
        answer.save()
        return redirect("quiz_bim:question_detail", pk=question.pk)


class AnswerBimUpdateView(PermissionRequiredMixin, UpdateView):
    model = AnswerBim
    form_class = AnswerBimForm
    template_name = 'quiz_bim/answer_bim/answer_bim_update.html'
    success_url = reverse_lazy('quiz_bim:tests_list')
    context_object_name = 'answer'
    permission_required = 'quiz_bim.change_answerbim'


class AnswerBimDeleteView(PermissionRequiredMixin, DeleteView):
    model = AnswerBim
    context_object_name = 'answer'
    template_name = 'quiz_bim/answer_bim/answer_bim_delete.html'
    success_url = reverse_lazy('quiz_bim:tests_list')
    permission_required = 'quiz_bim.delete_answerbim'
