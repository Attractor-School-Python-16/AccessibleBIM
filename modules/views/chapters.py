from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from modules.forms.chapters_form import ChaptersForm
from modules.models import ChapterModel


class ChaptersListView(PermissionRequiredMixin, ListView):
    model = ChapterModel
    template_name = 'chapters/chapters_list.html'
    context_object_name = 'chapters'
    ordering = ("-create_at",)
    permission_required = 'modules.view_chaptermodel'


class ChapterCreateView(PermissionRequiredMixin, CreateView):
    template_name = "chapters/chapter_create.html"
    model = ChapterModel
    form_class = ChaptersForm
    permission_required = 'modules.add_chaptermodel'

    def get_success_url(self):
        return reverse("modules:chapter_detail", kwargs={"pk": self.object.pk})


class ChapterDetailView(PermissionRequiredMixin, DetailView):
    model = ChapterModel
    context_object_name = 'chapter'
    template_name = 'chapters/chapter_detail.html'
    permission_required = 'modules.view_chaptermodel'


class ChapterUpdateView(PermissionRequiredMixin, UpdateView):
    model = ChapterModel
    form_class = ChaptersForm
    context_object_name = 'chapter'
    template_name = 'chapters/chapter_update.html'
    permission_required = 'modules.change_chaptermodel'

    def get_success_url(self):
        return reverse("modules:chapter_detail", kwargs={"pk": self.object.pk})


class ChapterDeleteView(PermissionRequiredMixin, DeleteView):
    model = ChapterModel
    template_name = "chapters/chapter_delete.html"
    context_object_name = 'chapter'
    success_url = reverse_lazy("modules:chapters_list")
    permission_required = 'modules.delete_chaptermodel'
