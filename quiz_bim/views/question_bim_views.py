from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from view_breadcrumbs import DetailBreadcrumbMixin, CreateBreadcrumbMixin, DeleteBreadcrumbMixin, \
    UpdateBreadcrumbMixin
from quiz_bim.models import QuizBim
from quiz_bim.models.question_bim import QuestionBim
from quiz_bim.forms.question_bim_form import QuestionBimForm
from django.urls import reverse
from django.utils.functional import cached_property


class QuestionBimDetailView(DetailBreadcrumbMixin, PermissionRequiredMixin, DetailView):
    model = QuestionBim
    queryset = QuestionBim.objects.all()
    template_name = "quiz_bim/question_bim/question_bim_detail.html"
    context_object_name = 'question'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_context_data(self, **kwargs):
        answers = self.object.answer_bim.all()
        kwargs['answers'] = answers
        return super().get_context_data(**kwargs)

    @cached_property
    def crumbs(self):
        return [("Детальный просмотр вопроса", reverse("quiz_bim:questionbim_update", kwargs={'pk': self.object.pk}))]


class QuestionBimCreateView(CreateBreadcrumbMixin, PermissionRequiredMixin, CreateView):
    model = QuestionBim
    form_class = QuestionBimForm
    template_name = "quiz_bim/question_bim/question_bim_create.html"

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def form_valid(self, form):
        quiz = get_object_or_404(QuizBim, pk=self.kwargs.get("pk"))
        question = form.save(commit=False)
        question.test_bim = quiz
        question.save()
        return redirect("quiz_bim:quizbim_detail", pk=quiz.pk)

    @cached_property
    def crumbs(self):
        return [("Создание вопроса", reverse("quiz_bim:questionbim_create", kwargs={'pk': self.kwargs.get("pk")}))]


class QuestionBimUpdateView(UpdateBreadcrumbMixin, PermissionRequiredMixin, UpdateView):
    model = QuestionBim
    form_class = QuestionBimForm
    template_name = 'quiz_bim/question_bim/question_bim_update.html'
    context_object_name = 'question'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("quiz_bim:quizbim_detail", kwargs={"pk": self.object.test_bim.pk})

    @cached_property
    def crumbs(self):
        return [("Изменение вопроса", reverse("quiz_bim:questionbim_update", kwargs={'pk': self.object.pk}))]


class QuestionBimDeleteView(DeleteBreadcrumbMixin, PermissionRequiredMixin, DeleteView):
    model = QuestionBim
    context_object_name = 'question'
    template_name = 'quiz_bim/question_bim/question_bim_delete.html'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("quiz_bim:quizbim_detail", kwargs={"pk": self.object.test_bim.pk})

    @cached_property
    def crumbs(self):
        return [("Удаления вопроса", reverse("quiz_bim:questionbim_delete", kwargs={'pk': self.object.pk}))]
