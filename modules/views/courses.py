from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from modules.forms.courses_form import CoursesForm
from modules.models import CourseModel, ModuleModel, ChapterModel


class CoursesListView(ListView):
    model = CourseModel
    template_name = 'courses/courses_list.html'
    context_object_name = 'courses'
    ordering = ("-create_at",)

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists()


class CourseCreateView(PermissionRequiredMixin, CreateView):
    template_name = "courses/course_create.html"
    model = CourseModel
    form_class = CoursesForm
    module_pk = None

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists()

    def get_initial(self):
        self.module_pk = self.request.GET.get('module_pk')
        return {'module_id': self.module_pk}

    def form_valid(self, form):
        form.instance.module_id = ModuleModel.objects.get(id=self.module_pk)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("modules:course_detail", kwargs={"pk": self.object.pk})


class CourseDetailView(PermissionRequiredMixin, DetailView):
    model = CourseModel
    context_object_name = 'course'
    template_name = 'courses/course_detail.html'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chapters'] = ChapterModel.objects.filter(course=self.object.id)
        return context


class CourseUpdateView(PermissionRequiredMixin, UpdateView):
    model = CourseModel
    form_class = CoursesForm
    context_object_name = 'course'
    template_name = 'courses/course_update.html'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists()

    def get_success_url(self):
        return reverse("modules:course_detail", kwargs={"pk": self.object.pk})


class CourseDeleteView(PermissionRequiredMixin, DeleteView):
    model = CourseModel
    template_name = "courses/course_delete.html"
    context_object_name = 'course'
    success_url = reverse_lazy("modules:courses_list")

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists()
