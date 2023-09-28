from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from view_breadcrumbs import DetailBreadcrumbMixin, ListBreadcrumbMixin, CreateBreadcrumbMixin, DeleteBreadcrumbMixin, \
    UpdateBreadcrumbMixin
from modules.forms.teachers_form import TeacherForm
from modules.models import TeacherModel


class TeachersListView(ListBreadcrumbMixin, PermissionRequiredMixin, ListView):
    model = TeacherModel
    template_name = 'teachers/teachers_list.html'
    context_object_name = 'teachers'
    ordering = ("-create_at",)

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class TeacherCreateView(CreateBreadcrumbMixin, PermissionRequiredMixin, CreateView):
    template_name = "teachers/teacher_create.html"
    model = TeacherModel
    form_class = TeacherForm

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("modules:teachermodel_detail", kwargs={"pk": self.object.pk})


class TeacherDetailView(DetailBreadcrumbMixin, PermissionRequiredMixin, DetailView):
    model = TeacherModel
    context_object_name = 'teacher'
    template_name = 'teachers/teacher_detail.html'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class TeacherUpdateView(UpdateBreadcrumbMixin, PermissionRequiredMixin, UpdateView):
    model = TeacherModel
    form_class = TeacherForm
    context_object_name = 'teacher'
    template_name = 'teachers/teacher_update.html'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("modules:teachermodel_list")


class TeacherDeleteView(DeleteBreadcrumbMixin, PermissionRequiredMixin, DeleteView):
    model = TeacherModel
    template_name = "teachers/teacher_delete.html"
    context_object_name = 'teacher'
    success_url = reverse_lazy("modules:teachermodel_list")

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser
