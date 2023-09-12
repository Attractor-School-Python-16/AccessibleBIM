from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from progress.models import ProgressTestAnswers


class ProgressTestAnswersCreateView(CreateView):
    model = ProgressTestAnswers
    fields = ['user', 'progress_test', 'question', 'answer']


class ProgressTestAnswersUpdateView(UpdateView):
    model = ProgressTestAnswers
    fields = ['user', 'progress_test', 'question', 'answer']
    template_name_suffix = '_update_form'


class ProgressTestAnswersDeleteView(DeleteView):
    model = ProgressTestAnswers
    success_url = '/success/'


class ProgressTestAnswersDetailView(DetailView):
    model = ProgressTestAnswers
