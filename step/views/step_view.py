from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from step.forms.step_form import StepForm
from step.forms.video_form import VideoForm
# from test_bim.forms.test_form import TestForm
from step.models import VideoModel, TextModel, FileModel, file_upload_to
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
    template_name = "../templates/steps/step/step_create.html"

    def form_valid(self, form):
        lesson_type = form.cleaned_data['lesson_type']
        if lesson_type == 'text':
            self.handle_text_lesson(form)
        elif lesson_type == 'video':
            self.handle_video_lesson(form)
        elif lesson_type == 'test':
            self.handle_test_lesson(form)
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

    def handle_video_lesson(self, form):
        video_title = self.request.POST.get('video_title')
        video_description = self.request.POST.get('video_description')
        video_file = self.request.FILES.get('video_file')
        video_instance = VideoModel.objects.create(
            video_title=video_title,
            video_description=video_description,
            video_file=video_file
        )
        form.instance.video = video_instance

    def handle_test_lesson(self, form):
        # Handle test case if needed
        pass

    def handle_uploaded_file(self, form):
        form.instance.save()
        selected_file = form.cleaned_data.get('file')
        if selected_file:
            form.instance.file.add(selected_file)

        uploaded_file = self.request.FILES.get('lesson_file')
        if uploaded_file:
            file_path = file_upload_to(form.instance, uploaded_file.name)
            file_instance = FileModel.objects.create(
                file_title=uploaded_file.name,
                lesson_file=uploaded_file
            )
            form.instance.file.add(file_instance)



class StepUpdateView(UpdateView):
    model = StepModel
    form_class = StepForm
    template_name = 'step/step_create.html'
    success_url = reverse_lazy('step_list')


class StepDeleteView(DeleteView):
    model = StepModel
    template_name = 'step/step_delete.html'
    success_url = reverse_lazy('step_list')
