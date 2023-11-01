from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from view_breadcrumbs import DetailBreadcrumbMixin, ListBreadcrumbMixin, CreateBreadcrumbMixin, DeleteBreadcrumbMixin, \
    UpdateBreadcrumbMixin
from step.forms.text_form import TextForm
from step.models import TextModel, StepModel


class TextListView(ListBreadcrumbMixin, LoginRequiredMixin, ListView):
    model = TextModel
    template_name = 'steps/text/text_list.html'
    context_object_name = 'texts'
    home_path = reverse_lazy('modules:moderator_page')


class TextDetailView(DetailBreadcrumbMixin, LoginRequiredMixin, DetailView):
    model = TextModel
    queryset = TextModel.objects.all()
    template_name = "steps/text/text_detail.html"
    context_object_name = 'text'
    home_path = reverse_lazy('modules:moderator_page')


class TextCreateView(CreateBreadcrumbMixin, PermissionRequiredMixin, CreateView):
    model = TextModel
    form_class = TextForm
    template_name = "steps/text/text_create.html"
    success_url = reverse_lazy('step:textmodel_list')
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        return self.request.user.has_perm('step.add_textmodel')


class TextUpdateView(UpdateBreadcrumbMixin, PermissionRequiredMixin, UpdateView):
    model = TextModel
    form_class = TextForm
    template_name = 'steps/text/text_update.html'
    success_url = reverse_lazy('step:textmodel_list')
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        return self.request.user.has_perm('step.change_textmodel')


class TextDeleteView(DeleteBreadcrumbMixin, PermissionRequiredMixin, DeleteView):
    model = TextModel
    template_name = 'steps/text/text_delete.html'
    success_url = reverse_lazy('step:textmodel_list')
    home_path = reverse_lazy('modules:moderator_page')
    context_object_name = "text"

    def form_valid(self, form):
        steps = StepModel.objects.all().filter(text=self.object)
        if steps:
            return render(self.request, 'steps/text/text_delete.html', context={
                "form": form,
                "steps": steps,
                "text": self.object
            })
        return super().form_valid(form)

    def has_permission(self):
        return self.request.user.has_perm('step.delete_textmodel')
