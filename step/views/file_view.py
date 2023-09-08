from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from step.forms.file_form import FileForm
from step.models import FileModel


class FileListView(ListView):
    model = FileModel
    template_name = 'file/file_list.html'
    context_object_name = 'files'


class FileDetailView(DetailView):
    queryset = FileModel.objects.all()
    template_name = "file/file_detail.html"


class FileCreateView(CreateView):
    form_class = FileForm
    template_name = "file/file_create.html"


class FileUpdateView(UpdateView):
    model = FileModel
    form_class = FileForm
    template_name = 'file/file_update.html'
    success_url = reverse_lazy('file_list')


class FileDeleteView(DeleteView):
    model = FileModel
    template_name = 'file/file_delete.html'
    success_url = reverse_lazy('file_list')
