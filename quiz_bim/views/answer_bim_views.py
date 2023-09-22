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

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists()

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

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists()


class AnswerBimDeleteView(PermissionRequiredMixin, DeleteView):
    model = AnswerBim
    context_object_name = 'answer'
    template_name = 'quiz_bim/answer_bim/answer_bim_delete.html'
    success_url = reverse_lazy('quiz_bim:tests_list')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists()
