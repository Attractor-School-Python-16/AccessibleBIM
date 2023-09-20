from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from modules.forms.chapters_form import ChaptersForm
from modules.models import ChapterModel, CourseModel


class ChaptersListView(ListView):
    model = ChapterModel
    template_name = 'chapters/chapters_list.html'
    context_object_name = 'chapters'
    ordering = ("-create_at",)


class ChapterCreateView(CreateView):
    template_name = "chapters/chapter_create.html"
    model = ChapterModel
    form_class = ChaptersForm
    course = None

    def get_initial(self):
        self.course = self.request.GET.get('course_pk')
        return {'course': self.course}

    def form_valid(self, form):
        form.instance.course = CourseModel.objects.get(id=self.course)
        return super().form_valid(form)

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
