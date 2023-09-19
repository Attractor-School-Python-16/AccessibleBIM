from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from step.forms.file_form import FileForm
from step.models import FileModel


class FileListView(LoginRequiredMixin, ListView):
    model = FileModel
    template_name = 'steps/file/file_list.html'
    context_object_name = 'files'



class FileDetailView(LoginRequiredMixin, DetailView):
    queryset = FileModel.objects.all()
    template_name = "steps/file/file_detail.html"
    context_object_name = 'file'


class FileCreateView(PermissionRequiredMixin, CreateView):
    form_class = FileForm
    template_name = "steps/file/file_create.html"

    def has_permission(self):
        return self.request.user.has_perm('step.add_filemodel')


class FileUpdateView(PermissionRequiredMixin, UpdateView):
    model = FileModel
    form_class = FileForm
    template_name = 'steps/file/file_update.html'
    success_url = reverse_lazy('file_list')

    def has_permission(self):
        return self.request.user.has_perm('step.change_filemodel')


class FileDeleteView(PermissionRequiredMixin, DeleteView):
    model = FileModel
    template_name = 'steps/file/file_delete.html'
    success_url = reverse_lazy('file_list')

    def has_permission(self):
        return self.request.user.has_perm('step.delete_filemodel')
