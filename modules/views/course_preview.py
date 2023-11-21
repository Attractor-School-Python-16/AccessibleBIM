from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.views.generic import DetailView
from modules.models import ChapterModel
from modules.models.user_course_progress import UserCourseProgress
from progress.models import ProgressTest
from step.models import StepModel
from subscription.models.user_subscription import UsersSubscription
from front.views.course_progress_view import create_user_course_progress


class CoursePreviewView(PermissionRequiredMixin, DetailView):
    model = ChapterModel
    context_object_name = 'chapter'
    template_name = 'courses/course_preview.html'
    pk_url_kwarg = 'chapter_pk'

    def has_permission(self):
        user = self.request.user
        return user.groups.filter(name='moderators').exists() or user.is_superuser

    def pagination_check(self):
        # Проверяем query параметр
        if self.request.GET.get('page'):
            try:
                int(self.request.GET.get('page'))
            except ValueError as e:
                return e
        else:
            return True

    def get(self, request, *args, **kwargs):
        if self.pagination_check():
            return HttpResponseNotFound("Not found")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chapter_steps = self.object.step.order_by('serial_number')
        paginator = Paginator(chapter_steps, 1)
        page_num = self.request.GET.get('page', 1)
        page = paginator.get_page(page_num)
        context['page_obj'] = page
        context['steps'] = page.object_list
        context['is_paginated'] = page.has_other_pages()
        context['title'] = f'{self.object.serial_number}. {self.object.title}'

        chapters = ChapterModel.objects.filter(course=self.get_object().course).order_by('serial_number')
        if chapters:
            context['chapters'] = chapters

        # Определение открытых глав пользователя и передача их в контекст
        next_chapter = ChapterModel.objects.filter(course=self.get_object().course,
                                                   serial_number=self.get_object().serial_number + 1)
        # Если шаг является тестом, проверяем, пройден ли он
        current_step = StepModel.objects.filter(chapter=self.object, serial_number=self.request.GET.get('page'))
        if current_step:
            current_step = StepModel.objects.filter(chapter=self.object, serial_number=self.request.GET.get('page'))[0]
            if current_step.test:
                progress_quiz = ProgressTest.objects.filter(test=current_step.test, user=self.request.user)
                if progress_quiz:
                    context['progress_quiz'] = progress_quiz[0]

        # Проверяем, что следующая глава есть и в ней присутствуют уроки
        if next_chapter:
            context['next_chapter'] = next_chapter[0]
            if next_chapter[0].step.all():
                context['chapter_end'] = True

        previous_chapter = ChapterModel.objects.filter(course=self.get_object().course,
                                                       serial_number=self.get_object().serial_number - 1)
        if previous_chapter and self.request.GET.get('page') == '1':
            if previous_chapter[0].step.all():
                context['previous_chapter'] = previous_chapter[0]
                last_step = previous_chapter[0].step.all().order_by('serial_number').last()
                context['last_step_serial_number'] = last_step.serial_number




        return context
