from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.utils.functional import cached_property
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.urls import reverse, reverse_lazy
from modules.models import ChapterModel
from quiz_bim.models import QuizBim
from step.models import FileModel, TextModel, VideoModel
from step.models.step import StepModel
from view_breadcrumbs import DetailBreadcrumbMixin, ListBreadcrumbMixin, DeleteBreadcrumbMixin

from step.forms.step_multi_form import MultiStepVideoForm, MultiStepQuizForm, MultiStepTextForm


# Представление StepListView в текущем состоянии не актуально. Добавлять проверку на разрешения в него не стал.
class StepListView(ListBreadcrumbMixin, ListView):
    model = StepModel
    template_name = 'steps/step/step_list.html'
    context_object_name = 'steps'
    success_url = reverse_lazy('modules:index')
    home_path = reverse_lazy('modules:moderator_page')


class StepDetailView(DetailBreadcrumbMixin, PermissionRequiredMixin, DetailView):
    model = StepModel
    queryset = StepModel.objects.all()
    context_object_name = 'step'
    template_name = "steps/step/step_detail.html"
    home_path = reverse_lazy('modules:moderator_page')

    @cached_property
    def crumbs(self):
        step = self.get_object()
        chapter = step.chapter
        course = chapter.course
        module = course.module_id

        return [
            (module._meta.verbose_name_plural, reverse_lazy("modules:modulemodel_list")),
            (module.title, reverse_lazy("modules:modulemodel_detail", kwargs={"pk": module.pk})),
            (course.title, reverse_lazy("modules:coursemodel_detail", kwargs={"pk": course.pk})),
            (chapter.title, reverse_lazy("modules:chaptermodel_detail", kwargs={"pk": chapter.pk})),
            (step.title, reverse_lazy("modules:chaptermodel_detail", kwargs={"pk": step.chapter.pk})),
        ]

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        step = context['step']
        files = FileModel.objects.filter(step=step)
        context['files'] = files
        return context


class StepCreateView(PermissionRequiredMixin, CreateView):
    template_name = "steps/step/step_create.html"
    chapter = None
    home_path = reverse_lazy('modules:moderator_page')

    def get_form_class(self):
        url_path = self.request.path.split('/')
        match url_path[-2]:
            case 'text':
                return MultiStepTextForm
            case 'video':
                return MultiStepVideoForm
            case "quiz":
                return MultiStepQuizForm

    def form_valid(self, form):
        url_path = self.request.path.split('/')
        match url_path[-2]:
            case 'text':
                return self.save_step_text_model(form)
            case 'video':
                return self.save_step_video_model(form)
            case 'quiz':
                return self.save_step_quiz_model(form)

    def save_step_text_model(self, form):
        step = form['step'].save(commit=False)
        step.lesson_type = 'text'
        step.chapter = get_object_or_404(ChapterModel, pk=self.chapter)

        if form['text'].cleaned_data['text_title']:
            text = form['text'].save()
        else:
            text = form['step'].cleaned_data['text']

        step.text = text
        return redirect("modules:chaptermodel_detail", self.chapter)

    def save_step_video_model(self, form):
        step = form['step'].save(commit=False)
        step.lesson_type = 'video'
        step.chapter = get_object_or_404(ChapterModel, pk=self.chapter)
        if form['video'].cleaned_data['video_title']:
            video = form['video'].save()
        else:
            video = form['step'].cleaned_data['video']
        step.video = video
        self.work_with_files(step, form)
        return redirect("modules:chaptermodel_detail", self.chapter)

    def save_step_quiz_model(self, form):
        step = form['step'].save(commit=False)
        step.lesson_type = 'test'
        step.chapter = get_object_or_404(ChapterModel, pk=self.chapter)
        if form['quiz'].cleaned_data['title']:
            test = form['quiz'].save()
        else:
            test = form['step'].cleaned_data['test']
        step.test = test
        step.save()
        return redirect("quiz_bim:quizbim_detail", test.pk)

    def work_with_files(self, step, form):
        step.save()
        print(step)
        if form['step'].cleaned_data['file']:
            file_loaded = form['step'].cleaned_data['file']
            step.file.set(file_loaded, )
        if form['file'].cleaned_data['lesson_file']:
            file_download = form['file'].save()
            step.file.add(file_download, )
        return step

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_initial(self):
        super().get_initial()
        self.chapter = self.request.GET.get('chapter_pk')
        return {'chapter': self.chapter}


class StepUpdateView(PermissionRequiredMixin, UpdateView):
    model = StepModel
    template_name = 'steps/step/step_update.html'
    home_path = reverse_lazy('modules:moderator_page')
    chapter = None

    @cached_property
    def crumbs(self):
        chapter = self.get_object().chapter
        course = chapter.course
        module = course.module_id

        return [
            (module._meta.verbose_name_plural, reverse_lazy("modules:modulemodel_list")),
            (module.title, reverse_lazy("modules:modulemodel_detail", kwargs={"pk": module.pk})),
            (course.title, reverse_lazy("modules:coursemodel_detail", kwargs={"pk": course.pk})),
            (chapter.title, reverse_lazy("modules:chaptermodel_detail", kwargs={"pk": chapter.pk}))
        ] + super().crumbs

    def get_initial(self):
        self.chapter = self.request.GET.get('chapter_pk')
        return {'chapter': self.chapter}

    def get_form_kwargs(self):
        kwargs = super(StepUpdateView, self).get_form_kwargs()
        match self.object.lesson_type:
            case 'text':
                kwargs.update(instance={
                    'step': self.object,
                    'text': self.object.text,
                })
            case 'video':
                kwargs.update(instance={
                    'step': self.object,
                    'text': self.object.text,
                })
            case "test":
                kwargs.update(instance={
                    'step': self.object,
                    'text': self.object.text,
                })
        return kwargs

    def get_form_class(self):
        match self.object.lesson_type:
            case 'text':
                return MultiStepTextForm
            case 'video':
                return MultiStepVideoForm
            case "quiz":
                return MultiStepQuizForm

    def form_valid(self, form):
        step = form['step'].save(commit=False)
        match self.object.lesson_type:
            case 'text':
                return self.update_step_text_model(step, form)
            case 'video':
                return self.update_step_video_model(step, form)
            case 'quiz':
                return self.update_step_quiz_model(step, form)

    def update_step_text_model(self, step, form):
        if form['text'].cleaned_data['text_title']:
            step.text = form['text'].save()
        self.work_with_files(step, form)

    def update_step_video_model(self, step, form):
        if form['video'].cleaned_data['video_title']:
            step.text = form['video'].save()
        self.work_with_files(step, form)

    def update_step_quiz_model(self, step, form):
        if form['quiz'].cleaned_data['title']:
            step.test = form['quiz'].save()
        step.save()
        return redirect("modules:chaptermodel_detail", self.chapter)

    def work_with_files(self, step, form):
        step.save()
        if form['step'].cleaned_data['file']:
            file_loaded = form['step'].cleaned_data['file']
            step.file.set(file_loaded, )
        if form['file'].cleaned_data['lesson_file']:
            file_download = form['file'].save()
            step.file.add(file_download, )
        return redirect("modules:chaptermodel_detail", self.chapter)

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text'], context['video'], context['test'] = self.object.text, self.object.video, self.object.test
        return context

    def form_valid(self, form):
        lesson_type = form.cleaned_data['lesson_type']
        if lesson_type == 'text':
            text = self.request.POST.get('text')
            if text:
                form.instance.text = TextModel.objects.get(pk=text)
                form.instance.video = None
                form.instance.test = None
            else:
                return render(
                    self.request,
                    self.template_name,
                    {'form': form, 'error_message': 'Текст не выбран'}
                )
        elif lesson_type == 'video':
            video = self.request.POST.get('video')
            if video:
                form.instance.video = VideoModel.objects.get(pk=video)
                form.instance.text = None
                form.instance.test = None
            else:
                return render(
                    self.request,
                    self.template_name,
                    {'form': form, 'error_message': 'Видео не выбрано'}
                )
        elif lesson_type == 'test':
            test = self.request.POST.get('test')
            if test:
                form.instance.test = QuizBim.objects.get(pk=test)
                form.instance.video = None
                form.instance.text = None
            else:
                return render(
                    self.request,
                    self.template_name,
                    {'form': form, 'error_message': 'Тест не выбран'}
                )
        form.instance.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("modules:chaptermodel_detail", kwargs={"pk": self.object.chapter.pk})


class StepDeleteView(DeleteBreadcrumbMixin, PermissionRequiredMixin, DeleteView):
    model = StepModel
    template_name = 'steps/step/step_delete.html'
    home_path = reverse_lazy('modules:moderator_page')
    chapter = None

    @cached_property
    def crumbs(self):
        chapter = self.get_object().chapter
        course = chapter.course
        module = course.module_id

        return [
            (module._meta.verbose_name_plural, reverse_lazy("modules:modulemodel_list")),
            (module.title, reverse_lazy("modules:modulemodel_detail", kwargs={"pk": module.pk})),
            (course.title, reverse_lazy("modules:coursemodel_detail", kwargs={"pk": course.pk})),
            (chapter.title, reverse_lazy("modules:chaptermodel_detail", kwargs={"pk": chapter.pk}))
        ] + super().crumbs

    def get_initial(self):
        self.chapter = self.request.GET.get('chapter_pk')
        return {'chapter': self.chapter}

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("modules:chaptermodel_detail", kwargs={"pk": self.get_object().chapter.id})
    
    
    def form_valid(self, form):
        step = self.get_object()
        chapter = step.chapter
        response = super().form_valid(form)
        self.update_serial_numbers(chapter)
        return response

    def update_serial_numbers(self, chapter):
        steps = StepModel.objects.filter(chapter=chapter).order_by('serial_number')
        current_serial_number = 1
        for step in steps:
            if step.serial_number != current_serial_number:
                step.serial_number = current_serial_number
                step.save()
            current_serial_number += 1
