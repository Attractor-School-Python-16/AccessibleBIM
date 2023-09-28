from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from view_breadcrumbs import DetailBreadcrumbMixin, ListBreadcrumbMixin, CreateBreadcrumbMixin, DeleteBreadcrumbMixin, \
    UpdateBreadcrumbMixin
from step.forms.file_form import FileForm
from step.models import FileModel


class FileListView(ListBreadcrumbMixin, LoginRequiredMixin, ListView):
    model = FileModel
    template_name = 'steps/file/file_list.html'
    context_object_name = 'files'


class FileDetailView(DetailBreadcrumbMixin, LoginRequiredMixin, DetailView):
    model = FileModel
    queryset = FileModel.objects.all()
    template_name = "steps/file/file_detail.html"
    context_object_name = 'file'


class FileCreateView(CreateBreadcrumbMixin, PermissionRequiredMixin, CreateView):
    model = FileModel
    form_class = FileForm
    template_name = "steps/file/file_create.html"
    success_url = reverse_lazy('step:filemodel_list')

    def has_permission(self):
        return self.request.user.has_perm('step.add_filemodel')


class FileUpdateView(UpdateBreadcrumbMixin, PermissionRequiredMixin, UpdateView):
    model = FileModel
    form_class = FileForm
    template_name = 'steps/file/file_update.html'
    success_url = reverse_lazy('step:filemodel_list')

    def has_permission(self):
        return self.request.user.has_perm('step.change_filemodel')


class FileDeleteView(DeleteBreadcrumbMixin, PermissionRequiredMixin, DeleteView):
    model = FileModel
    template_name = 'steps/file/file_delete.html'
    success_url = reverse_lazy('step:filemodel_list')

    def has_permission(self):
        return self.request.user.has_perm('step.delete_filemodel')
