from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from modules.forms.courses_form import CoursesForm
from modules.models import CourseModel, ModuleModel


class CoursesListView(ListView):
    model = CourseModel
    template_name = 'courses/courses_list.html'
    context_object_name = 'courses'
    ordering = ("-create_at",)


class CourseCreateView(CreateView):
    template_name = "courses/course_create.html"
    model = CourseModel
    form_class = CoursesForm
    module_pk = None

    def get_initial(self):
        self.module_pk = self.request.GET.get('module_pk')
        return {'module_id': self.module_pk}

    def form_valid(self, form):
        form.instance.module_id = ModuleModel.objects.get(id=self.module_pk)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("modules:course_detail", kwargs={"pk": self.object.pk})


class CourseDetailView(DetailView):
    model = CourseModel
    context_object_name = 'course'
    template_name = 'courses/course_detail.html'


class CourseUpdateView(UpdateView):
    model = CourseModel
    form_class = CoursesForm
    context_object_name = 'course'
    template_name = 'courses/course_update.html'

    def get_success_url(self):
        return reverse("modules:course_detail", kwargs={"pk": self.object.pk})


class CourseDeleteView(DeleteView):
    model = CourseModel
    template_name = "courses/course_delete.html"
    context_object_name = 'course'
    success_url = reverse_lazy("modules:courses_list")
