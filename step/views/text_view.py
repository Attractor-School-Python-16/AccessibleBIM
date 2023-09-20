from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from step.forms.text_form import TextForm
from step.models import TextModel


class TextListView(LoginRequiredMixin, ListView):
    model = TextModel
    template_name = 'steps/text/text_list.html'
    context_object_name = 'texts'


class TextDetailView(LoginRequiredMixin, DetailView):
    queryset = TextModel.objects.all()
    template_name = "steps/text/text_detail.html"
    context_object_name = 'text'

class TextCreateView(PermissionRequiredMixin, CreateView):
    model = TextModel
    form_class = TextForm
    template_name = "steps/text/text_create.html"

    def has_permission(self):
        return self.request.user.has_perm('step.add_textmodel')


class TextUpdateView(UpdateView):
    model = TextModel
    form_class = TextForm
    template_name = 'steps/text/text_update.html'
    success_url = reverse_lazy('step:text_list')


class TextDeleteView(DeleteView):
    model = TextModel
    template_name = 'steps/text/text_delete.html'
    success_url = reverse_lazy('step:text_list')
