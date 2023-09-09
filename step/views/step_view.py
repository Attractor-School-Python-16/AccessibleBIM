from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from step.forms.step_form import StepForm
from step.forms.video_form import VideoForm
# from test_bim.forms.test_form import TestForm
from step.models import VideoModel, TextModel
from step.models.step import StepModel
from test_bim.models import TestBim


class StepListView(ListView):
    model = StepModel
    template_name = 'step/step_list.html'
    context_object_name = 'steps'
    paginate_by = 1


class StepDetailView(DetailView):
    queryset = StepModel.objects.all()
    template_name = "step/step_detail.html"


class StepCreateView(CreateView):
    model = StepModel
    form_class = StepForm
    template_name = "step/step_create.html"
    success_url = reverse_lazy('step_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['video_form'] = VideoForm()
        context['text_form'] = TextForm()
        context['test_form'] = TestForm()
        return context
    def form_valid(self, form):
        step = form.save(commit=False)
        lesson_type = form.cleaned_data.get('lesson_type')

        if lesson_type == 'video':
            video_form = VideoForm(self.request.POST, self.request.FILES)
            if video_form.is_valid():
                video = video_form.save(commit=False)
                video.step = step
                video.save()
        elif lesson_type == 'text':
            text_form = TextForm(self.request.POST)
            if text_form.is_valid():
                text = text_form.save(commit=False)
                text.step = step
                text.save()
        elif lesson_type == 'test':
            test_form = TestForm(self.request.POST)
            if test_form.is_valid():
                test = test_form.save(commit=False)
                test.step = step
                test.save()
        step.save()
        return super().form_valid(form)


class StepUpdateView(UpdateView):
    model = StepModel
    form_class = StepForm
    template_name = 'step/step_create.html'
    success_url = reverse_lazy('step_list')


class StepDeleteView(DeleteView):
    model = StepModel
    template_name = 'step/step_delete.html'
    success_url = reverse_lazy('step_list')
