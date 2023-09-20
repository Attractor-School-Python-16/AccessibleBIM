from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from modules.forms.teachers_form import TeacherForm
from modules.models import TeacherModel


class TeachersListView(PermissionRequiredMixin, ListView):
    model = TeacherModel
    template_name = 'teachers/teachers_list.html'
    context_object_name = 'teachers'
    ordering = ("-create_at",)
    permission_required = 'modules.view_teachermodel'


class TeacherCreateView(PermissionRequiredMixin, CreateView):
    template_name = "teachers/teacher_create.html"
    model = TeacherModel
    form_class = TeacherForm
    permission_required = 'modules.add_teachermodel'

    def get_success_url(self):
        return reverse("modules:teacher_detail", kwargs={"pk": self.object.pk})


class TeacherDetailView(PermissionRequiredMixin, DetailView):
    model = TeacherModel
    context_object_name = 'teacher'
    template_name = 'teachers/teacher_detail.html'
    permission_required = 'modules.view_teachermodel'


class TeacherUpdateView(PermissionRequiredMixin, UpdateView):
    model = TeacherModel
    form_class = TeacherForm
    context_object_name = 'teacher'
    template_name = 'teachers/teacher_update.html'
    permission_required = 'modules.change_teachermodel'

    def get_success_url(self):
        return reverse("modules:teacher_detail", kwargs={"pk": self.object.pk})


class TeacherDeleteView(PermissionRequiredMixin, DeleteView):
    model = TeacherModel
    template_name = "teachers/teacher_delete.html"
    context_object_name = 'teacher'
    success_url = reverse_lazy("modules:teachers_list")
    permission_required = 'modules.delete_teachermodel'
