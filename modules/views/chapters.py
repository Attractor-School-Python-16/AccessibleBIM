from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from modules.forms.chapters_form import ChaptersForm
from modules.models import ChapterModel


class ChaptersListView(ListView):
    model = ChapterModel
    template_name = 'chapters/chapters_list.html'
    context_object_name = 'chapters'
    ordering = ("-create_at",)


class ChapterCreateView(CreateView):
    template_name = "chapters/chapter_create.html"
    model = ChapterModel
    form_class = ChaptersForm

    def get_success_url(self):
        return reverse("modules:chapter_detail", kwargs={"pk": self.object.pk})


class ChapterDetailView(DetailView):
    model = ChapterModel
    context_object_name = 'chapter'
    template_name = 'chapters/chapter_detail.html'


class ChapterUpdateView(UpdateView):
    model = ChapterModel
    form_class = ChaptersForm
    context_object_name = 'chapter'
    template_name = 'chapters/chapter_update.html'

    def get_success_url(self):
        return reverse("modules:chapter_detail", kwargs={"pk": self.object.pk})


class ChapterDeleteView(DeleteView):
    model = ChapterModel
    template_name = "chapters/chapter_delete.html"
    context_object_name = 'chapter'
    success_url = reverse_lazy("modules:chapters_list")
