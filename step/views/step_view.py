from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from step.forms.step_form import StepForm
from step.forms.video_form import VideoForm
# from test_bim.forms.test_form import TestForm
from step.models import VideoModel, TextModel, FileModel, file_upload_to, video_upload_to
from step.models.step import StepModel
from test_bim.models import TestBim


class StepListView(ListView):
    model = StepModel
    template_name = 'step/step_list.html'
    context_object_name = 'steps'
    paginate_by = 1
    success_url = reverse_lazy('modules:index')


class StepDetailView(DetailView):
    queryset = StepModel.objects.all()
    template_name = "step/step_detail.html"


class StepCreateView(CreateView):
    model = StepModel
    form_class = StepForm
    template_name = "../templates/steps/step/step_create.html"

    def form_valid(self, form):
        lesson_type = form.cleaned_data['lesson_type']
        if lesson_type == 'text':
            text_instance = self.handle_text_lesson(form)
        elif lesson_type == 'video':
            video_instance = self.handle_video_lesson(form)
        elif lesson_type == 'test':

            pass
        form.instance.save()
        self.handle_uploaded_file(form)
        return super().form_valid(form)

    def handle_text_lesson(self, form):
        text_title = self.request.POST.get('text_title')
        text_description = self.request.POST.get('text_description')
        content = self.request.POST.get('content')
        text_instance = TextModel.objects.create(
            text_title=text_title,
            text_description=text_description,
            content=content
        )
        form.instance.text = text_instance
        return text_instance

    def handle_video_lesson(self, form):
        form.instance.save()
        video_instance = VideoModel.objects.create(
            video_title=self.request.POST.get('video_title'),
            video_description=self.request.POST.get('video_description'),
            video_file=self.request.FILES.get('video_file'),

        )
        video_upload_to(instance=form.instance, filename=self.request.POST.get('video_title'))
        form.instance.video = video_instance
        return video_instance

    def handle_uploaded_file(self, form):
        selected_file = form.cleaned_data.get('file')
        if selected_file:
            form.instance.file = selected_file
        uploaded_file = self.request.FILES.get('lesson_file')
        if uploaded_file:
            file_instance = FileModel.objects.create(
                file_title=self.request.POST.get('file_title'),
                lesson_file=uploaded_file
            )
            file_upload_to(instance=form.instance, filename=self.request.POST.get('file_title'))
            form.instance.file = file_instance
            return file_instance



class StepUpdateView(UpdateView):
    model = StepModel
    form_class = StepForm
    template_name = 'step/step_create.html'
    success_url = reverse_lazy('step_list')


class StepDeleteView(DeleteView):
    model = StepModel
    template_name = 'step/step_delete.html'
    success_url = reverse_lazy('step_list')
