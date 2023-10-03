from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.urls import reverse, reverse_lazy
from modules.models import ChapterModel
from step.forms.step_form import StepForm
from step.models import VideoModel, TextModel, FileModel, video_upload_to
from step.models.step import StepModel
from quiz_bim.models import QuizBim, QuestionBim, AnswerBim
from view_breadcrumbs import DetailBreadcrumbMixin, ListBreadcrumbMixin, CreateBreadcrumbMixin, DeleteBreadcrumbMixin, \
    UpdateBreadcrumbMixin

from step.step_validators import quiz_validate, text_validate, video_validate, get_returning_context


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

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        step = context['step']
        files = FileModel.objects.filter(step=step)
        context['files'] = files
        if self.object.lesson_type == 'test':
            context['questions'] = self.object.test.question_bim.all()
        return context


class StepCreateView(CreateBreadcrumbMixin, PermissionRequiredMixin, CreateView):
    model = StepModel
    form_class = StepForm
    template_name = "steps/step/step_create.html"
    chapter = None
    home_path = reverse_lazy('modules:moderator_page')

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_initial(self):
        self.chapter = self.request.GET.get('chapter_pk')
        return {'chapter': self.chapter}


    def form_valid(self, form):
        print(self.request.POST)
        form.instance.chapter = ChapterModel.objects.get(id=self.chapter)
        lesson_type = form.cleaned_data['lesson_type']
        if lesson_type == 'text':
            error_messages = text_validate(self)
            if error_messages:
                returned = get_returning_context(self)
                print(returned)
                return render(self.request, self.template_name, {'form': form, 'error_messages': error_messages,
                                                                 'returned': returned})
            self.handle_text_lesson(form)
        elif lesson_type == 'video':
            video_validate(self, form)
            self.handle_video_lesson(form)
        elif lesson_type == 'test':
            quiz_validate(self, form)
            self.handle_quiz_lesson(form)
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

    def handle_quiz_lesson(self, form):
        print(self.request.POST)
        test = self.request.POST.get('test')
        if test:
            form.instance.test = test
            return test
        test_instance = QuizBim.objects.create(
            title=self.request.POST.get('test_title'),
            questions_qty=self.request.POST.get('test_questions_qty')
        )
        for i in range(1, int(self.request.POST.get('question_blocks_count')) + 1):
            question_text = self.request.POST.get(f'question_title_{i}')
            question = QuestionBim.objects.create(title=question_text, test_bim=test_instance)
            answers_qty = 0
            for j in range(1, 11):  # Предположим, что не может быть больше 10 вариантов
                answer_text = self.request.POST.get(f'answer_{i}_{j}')
                if answer_text:
                    answers_qty += 1
            for j in range(1, answers_qty + 1):
                answer_text = self.request.POST.get(f'answer_{i}_{j}')
                is_correct = bool(self.request.POST.get(f'is_correct_{i}_{j}'))
                if answer_text:
                    AnswerBim.objects.create(answer=answer_text, is_correct=is_correct, question_bim=question)
        form.instance.test = test_instance
        return test_instance

    def get_success_url(self):
        return reverse("modules:chaptermodel_detail", kwargs={"pk": self.object.chapter.pk})



class StepUpdateView(UpdateBreadcrumbMixin, PermissionRequiredMixin, UpdateView):
    model = StepModel
    form_class = StepForm
    template_name = 'steps/step/step_update.html'
    home_path = reverse_lazy('modules:moderator_page')
    chapter = None

    def get_initial(self):
        self.chapter = self.request.GET.get('chapter_pk')
        return {'chapter': self.chapter}

    def get_success_url(self):
        return reverse('modules:chaptermodel_detail', kwargs={"pk": self.chapter})

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

    def get_initial(self):
        self.chapter = self.request.GET.get('chapter_pk')
        return {'chapter': self.chapter}

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def get_success_url(self):
        return reverse("modules:chaptermodel_detail", kwargs={"pk": self.object.chapter.pk})
