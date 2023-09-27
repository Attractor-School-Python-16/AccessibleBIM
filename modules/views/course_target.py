from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from view_breadcrumbs import DetailBreadcrumbMixin, ListBreadcrumbMixin, CreateBreadcrumbMixin, DeleteBreadcrumbMixin, \
    UpdateBreadcrumbMixin
from modules.forms.course_target_form import CourseTargetForm
from modules.models import CourseTargetModel


class CourseTargetsListView(ListBreadcrumbMixin, PermissionRequiredMixin, ListView):
    model = CourseTargetModel
    template_name = 'course_target/course_target_list.html'
    context_object_name = 'course_targets'
    ordering = ("-create_at",)

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class CourseTargetCreateView(CreateBreadcrumbMixin, PermissionRequiredMixin, CreateView):
    template_name = "course_target/course_target_create.html"
    model = CourseTargetModel
    form_class = CourseTargetForm

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("modules:course_target_detail", kwargs={"pk": self.object.pk})


class CourseTargetDetailView(DetailBreadcrumbMixin, PermissionRequiredMixin, DetailView):
    model = CourseTargetModel
    context_object_name = 'course_target'
    template_name = 'course_target/course_target_detail.html'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class CourseTargetUpdateView(UpdateBreadcrumbMixin, PermissionRequiredMixin, UpdateView):
    model = CourseTargetModel
    form_class = CourseTargetForm
    context_object_name = 'course_target'
    template_name = 'course_target/course_target_update.html'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("modules:course_target_detail", kwargs={"pk": self.object.pk})


class CourseTargetDeleteView(DeleteBreadcrumbMixin, PermissionRequiredMixin, DeleteView):
    model = CourseTargetModel
    template_name = "course_target/course_target_delete.html"
    context_object_name = 'course_target'
    success_url = reverse_lazy("modules:course_targets_list")

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser
