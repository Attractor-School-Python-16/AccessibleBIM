from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from step.forms.step_forms import StepForm
from step.models.step import StepModel


class StepListView(ListView):
    model = StepModel
    template_name = 'step_list.html'
    context_object_name = 'steps'
    paginate_by = 1


class StepDetailView(DetailView):
    queryset = StepModel.objects.all()
    template_name = "step_detail.html"


class StepUpdateView(UpdateView):
    model = StepModel
    form_class = StepForm
    template_name = 'step_create.html'
    success_url = reverse_lazy('step_list')


class StepDeleteView(DeleteView):
    model = StepModel
    template_name = 'step_delete.html'
    success_url = reverse_lazy('step_list')
