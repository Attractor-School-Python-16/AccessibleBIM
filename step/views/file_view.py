from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from view_breadcrumbs import DetailBreadcrumbMixin, ListBreadcrumbMixin, CreateBreadcrumbMixin, DeleteBreadcrumbMixin, \
    UpdateBreadcrumbMixin
from step.forms.file_form import FileForm
from step.models import FileModel


class FileListView(ListBreadcrumbMixin, PermissionRequiredMixin, ListView):
    model = FileModel
    template_name = 'steps/file/file_list.html'
    context_object_name = 'files'
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class FileDetailView(DetailBreadcrumbMixin, PermissionRequiredMixin, DetailView):
    model = FileModel
    queryset = FileModel.objects.all()
    template_name = "steps/file/file_detail.html"
    context_object_name = 'file'
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class FileCreateView(CreateBreadcrumbMixin, PermissionRequiredMixin, CreateView):
    model = FileModel
    form_class = FileForm
    template_name = "steps/file/file_create.html"
    success_url = reverse_lazy('step:filemodel_list')
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

class FileUpdateView(UpdateBreadcrumbMixin, PermissionRequiredMixin, UpdateView):
    model = FileModel
    form_class = FileForm
    template_name = 'steps/file/file_update.html'
    success_url = reverse_lazy('step:filemodel_list')
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser


class FileDeleteView(DeleteBreadcrumbMixin, PermissionRequiredMixin, DeleteView):
    model = FileModel
    template_name = 'steps/file/file_delete.html'
    success_url = reverse_lazy('step:filemodel_list')
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser
