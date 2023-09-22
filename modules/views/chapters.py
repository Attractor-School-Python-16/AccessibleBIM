from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from modules.forms.chapters_form import ChaptersForm
from modules.models import ChapterModel, CourseModel
from step.models import StepModel


class ChaptersListView(PermissionRequiredMixin, ListView):
    model = ChapterModel
    template_name = 'chapters/chapters_list.html'
    context_object_name = 'chapters'
    ordering = ("-create_at",)

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists()


class ChapterCreateView(PermissionRequiredMixin, CreateView):
    template_name = "chapters/chapter_create.html"
    model = ChapterModel
    form_class = ChaptersForm
    course = None

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists()

    def get_initial(self):
        self.course = self.request.GET.get('course_pk')
        return {'course': self.course}

    def form_valid(self, form):
        form.instance.course = CourseModel.objects.get(id=self.course)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("modules:chapter_detail", kwargs={"pk": self.object.pk})


class ChapterDetailView(PermissionRequiredMixin, DetailView):
    model = ChapterModel
    context_object_name = 'chapter'
    template_name = 'chapters/chapter_detail.html'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['steps'] = StepModel.objects.filter(chapter=self.object.id)
        return context


class ChapterUpdateView(PermissionRequiredMixin, UpdateView):
    model = ChapterModel
    form_class = ChaptersForm
    context_object_name = 'chapter'
    template_name = 'chapters/chapter_update.html'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists()

    def get_success_url(self):
        return reverse("modules:chapter_detail", kwargs={"pk": self.object.pk})


class ChapterDeleteView(PermissionRequiredMixin, DeleteView):
    model = ChapterModel
    template_name = "chapters/chapter_delete.html"
    context_object_name = 'chapter'
    success_url = reverse_lazy("modules:chapters_list")

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists()
