from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView, CreateView
from view_breadcrumbs import CreateBreadcrumbMixin, DeleteBreadcrumbMixin, \
    UpdateBreadcrumbMixin
from quiz_bim.models import QuestionBim
from quiz_bim.models.answer_bim import AnswerBim
from quiz_bim.forms.answer_bim_form import AnswerBimForm
from django.urls import reverse
from django.utils.functional import cached_property


class AnswerBimCreateView(CreateBreadcrumbMixin, PermissionRequiredMixin, CreateView):
    model = AnswerBim
    form_class = AnswerBimForm
    template_name = "quiz_bim/answer_bim/answer_bim_create.html"

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def form_valid(self, form):
        question = get_object_or_404(QuestionBim, pk=self.kwargs.get("pk"))
        answer = form.save(commit=False)
        answer.question_bim = question
        answer.save()
        return redirect("quiz_bim:questionbim_detail", pk=question.pk)

    @cached_property
    def crumbs(self):
        return [("Создание ответа", reverse("quiz_bim:answerbim_create", kwargs={'pk': self.kwargs.get("pk")}))]


class AnswerBimUpdateView(UpdateBreadcrumbMixin, PermissionRequiredMixin, UpdateView):
    model = AnswerBim
    form_class = AnswerBimForm
    template_name = 'quiz_bim/answer_bim/answer_bim_update.html'
    context_object_name = 'answer'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("quiz_bim:questionbim_detail", kwargs={"pk": self.object.question_bim.pk})

    @cached_property
    def crumbs(self):
        return [("Редактирование ответа", reverse("quiz_bim:answerbim_update", kwargs={'pk': self.kwargs.get("pk")}))]

class AnswerBimDeleteView(DeleteBreadcrumbMixin, PermissionRequiredMixin, DeleteView):
    model = AnswerBim
    context_object_name = 'answer'
    template_name = 'quiz_bim/answer_bim/answer_bim_delete.html'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("quiz_bim:questionbim_detail", kwargs={"pk": self.object.question_bim.pk})

    @cached_property
    def crumbs(self):
        return [("Удаление ответа", reverse("quiz_bim:answerbim_delete", kwargs={'pk': self.kwargs.get("pk")}))]