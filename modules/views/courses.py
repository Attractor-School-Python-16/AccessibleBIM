from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from modules.forms.courses_form import CoursesForm
from modules.models import CourseModel


class CoursesListView(PermissionRequiredMixin, ListView):
    model = CourseModel
    template_name = 'courses/courses_list.html'
    context_object_name = 'courses'
    ordering = ("-create_at",)
    permission_required = 'modules.view_coursemodel'


class CourseCreateView(PermissionRequiredMixin, CreateView):
    template_name = "courses/course_create.html"
    model = CourseModel
    form_class = CoursesForm
    permission_required = 'modules.add_coursemodel'

    def get_success_url(self):
        return reverse("modules:course_detail", kwargs={"pk": self.object.pk})


class CourseDetailView(PermissionRequiredMixin, DetailView):
    model = CourseModel
    context_object_name = 'course'
    template_name = 'courses/course_detail.html'
    permission_required = 'modules.view_coursemodel'


class CourseUpdateView(PermissionRequiredMixin, UpdateView):
    model = CourseModel
    form_class = CoursesForm
    context_object_name = 'course'
    template_name = 'courses/course_update.html'
    permission_required = 'modules.change_coursemodel'

    def get_success_url(self):
        return reverse("modules:course_detail", kwargs={"pk": self.object.pk})


class CourseDeleteView(PermissionRequiredMixin, DeleteView):
    model = CourseModel
    template_name = "courses/course_delete.html"
    context_object_name = 'course'
    success_url = reverse_lazy("modules:courses_list")
    permission_required = 'modules.delete_coursemodel'
