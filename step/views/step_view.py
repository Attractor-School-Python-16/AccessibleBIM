from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from modules.models import ChapterModel
from step.forms.step_form import StepForm
from step.models import VideoModel, TextModel, FileModel, video_upload_to
from step.models.step import StepModel
from quiz_bim.models import QuizBim


class StepListView(ListView):
    model = StepModel
    template_name = 'steps/step/step_list.html'
    context_object_name = 'steps'
    success_url = reverse_lazy('modules:index')


class StepDetailView(DetailView):
    queryset = StepModel.objects.all()
    context_object_name = 'step'
    template_name = "steps/step/step_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        step = context['step']
        files = FileModel.objects.filter(step=step)
        context['files'] = files
        if self.object.lesson_type == 'test':
            context['questions'] = self.object.test.question_bim.all()
        return context


class StepCreateView(CreateView):
    model = StepModel
    form_class = StepForm
    template_name = "steps/step/step_create.html"
    chapter = None

    def get_initial(self):
        self.chapter = self.request.GET.get('chapter_pk')
        return {'chapter': self.chapter}



    def form_valid(self, form):
        print(form)
        form.instance.chapter = ChapterModel.objects.get(id=self.chapter)
        lesson_type = form.cleaned_data['lesson_type']
        if lesson_type == 'text':
            self.handle_text_lesson(form)
        elif lesson_type == 'video':
            self.handle_video_lesson(form)
        elif lesson_type == 'test':
            form.instance.test = QuizBim.objects.get(pk=self.request.POST.get('test'))
        form.instance.save()
        return super().form_valid(form)

    def handle_text_lesson(self, form):
        text = self.request.POST.get('text')
        if text:
            form.instance.text = TextModel.objects.get(pk=text)
            return text
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
        video = self.request.POST.get('video')
        if video:
            form.instance.video = video
            return video
        form.instance.save()
        video_instance = VideoModel.objects.create(
            video_title=self.request.POST.get('video_title'),
            video_description=self.request.POST.get('video_description'),
            video_file=self.request.FILES.get('video_file'),
        )
        video_upload_to(instance=form.instance, filename=self.request.POST.get('video_title'))
        form.instance.video = video_instance
        return video_instance



class StepUpdateView(UpdateView):
    model = StepModel
    form_class = StepForm
    template_name = 'steps/step/step_update.html'
    success_url = reverse_lazy('step:step_list')

    def form_valid(self, form):
        lesson_type = form.cleaned_data['lesson_type']
        if lesson_type == 'text':
            self.handle_text_lesson(form)
        elif lesson_type == 'video':
            self.handle_video_lesson(form)
        elif lesson_type == 'test':
            pass
        form.instance.save()
        return super().form_valid(form)

    def handle_text_lesson(self, form):
        text = self.request.POST.get('text')
        if text:
            form.instance.text = TextModel.objects.get(pk=text)
            return text
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
        video = self.request.POST.get('video')
        if video:
            form.instance.video = VideoModel.objects.get(pk=video)
            return video
        form.instance.save()
        video_instance = VideoModel.objects.create(
            video_title=self.request.POST.get('video_title'),
            video_description=self.request.POST.get('video_description'),
            video_file=self.request.FILES.get('video_file'),
        )
        video_upload_to(instance=form.instance, filename=self.request.POST.get('video_title'))
        form.instance.video = video_instance
        return video_instance



class StepDeleteView(DeleteView):
    model = StepModel
    template_name = 'steps/step/step_delete.html'
    success_url = reverse_lazy('step:step_list')
