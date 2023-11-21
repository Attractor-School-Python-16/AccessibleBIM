from django.core.paginator import Paginator
from django.http import HttpResponseNotFound, Http404
from django.views.generic import DetailView
from modules.models import ChapterModel
from modules.models.user_course_progress import UserCourseProgress
from progress.models import ProgressTest
from step.models import StepModel
from subscription.models.user_subscription import UsersSubscription
from front.views.course_progress_view import create_user_course_progress


class ChapterUserDetailView(DetailView):
    model = ChapterModel
    context_object_name = 'chapter'
    template_name = 'front/chapter/chapter_user_detail_view.html'
    pk_url_kwarg = 'chapter_pk'

    def new_progress_obj(self, chapter, new_chapter_progress=False):
        # Создаем новый объект прогресса
        if new_chapter_progress:
            next_step = StepModel.objects.filter(chapter__serial_number=chapter.serial_number + 1,
                                                 chapter__course=chapter.course,
                                                 serial_number=1)
        else:
            next_step = chapter.step.filter(serial_number=int(self.request.GET.get('page')))
        if next_step:
            new_progress_odj = create_user_course_progress(user=self.request.user, step=next_step[0])
            return new_progress_odj

    def chapter_next_step_control(self, user_progress: UserCourseProgress):
        # Проверяем, является ли новый шаг последним. Если да, то сразу завершаем его.
        if not user_progress.step.test:
            chapter = user_progress.step.chapter
            finished_steps = UserCourseProgress.objects.filter(user=self.request.user,
                                                               step__chapter=chapter,
                                                               status=1)
            if finished_steps.count() == chapter.step.count() - 1:
                user_progress.status = 1
                user_progress.save()

    def chapter_progress_check(self):
        # Проверяем наличие объектов прогресса по действующей подписке.
        current_user_subscription = UsersSubscription.objects.filter(user=self.request.user, is_active=True)[0]
        progress_objects = \
            UserCourseProgress.objects.filter(user=self.request.user,
                                              step__chapter__course=current_user_subscription.subscription.course,
                                              step__chapter=self.get_object())
        return progress_objects

    def pagination_check(self):
        # Проверяем query параметр
        if self.request.GET.get('page'):
            try:
                int(self.request.GET.get('page'))
            except ValueError as e:
                return e
        else:
            return True

    def dispatch(self, request, *args, **kwargs):
        # Создаем первый объект прогресса, если на данный курс действует подписка.
        current_user = request.user
        current_user_subscription = UsersSubscription.objects.filter(user=current_user, is_active=True)[0]
        if current_user_subscription:
            current_progress = UserCourseProgress.objects.filter(user=current_user,
                                                                 step__chapter__course=current_user_subscription.subscription.course)
            if not current_progress and request.GET.get('page') == '1':
                current_user_course = current_user_subscription.subscription.course
                first_user_course_chapter = current_user_course.ct_course.filter(serial_number=1)[0]
                if first_user_course_chapter.pk == kwargs['chapter_pk']:
                    first_user_course_step = first_user_course_chapter.step.filter(serial_number=1)[0]
                    current_progress = UserCourseProgress.objects.create(user=current_user,
                                                                         step=first_user_course_step)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        progress_obj = self.chapter_progress_check()
        if not progress_obj or self.pagination_check():
            raise Http404

        current_user = request.user
        current_user_subscription = UsersSubscription.objects.filter(user=self.request.user, is_active=True)[0]
        last_progress_object = \
            UserCourseProgress.objects.filter(user=self.request.user,
                                              step__chapter__course=current_user_subscription.subscription.course).order_by(
                '-updated_at')[0]
        last_progress_chapter = last_progress_object.step.chapter
        if last_progress_chapter == self.get_object():
            if last_progress_object.step.serial_number != int(request.GET.get('page')):
                if last_progress_object.step.test:
                    progress_test_passed = ProgressTest.objects.filter(user=current_user,
                                                                       test__step=last_progress_object.step,
                                                                       is_passed=True)
                    if not progress_test_passed:
                        next_progress_obj = self.new_progress_obj(chapter=last_progress_chapter)
                        if next_progress_obj:
                            self.chapter_next_step_control(next_progress_obj)
                        return super().get(request, *args, **kwargs)
                if last_progress_object.status == 0:
                    last_progress_object.status = 1
                    last_progress_object.save()

                next_step = \
                    last_progress_chapter.step.filter(serial_number=int(request.GET.get('page')))[0]

                next_progress_obj = create_user_course_progress(user=current_user, step=next_step)

                if next_progress_obj:
                    self.chapter_next_step_control(next_progress_obj)

            finished_steps = UserCourseProgress.objects.filter(user=current_user,
                                                               step__chapter=last_progress_chapter,
                                                               status=1)
            finished_chapters = ChapterModel.objects.filter(
                course=current_user_subscription.subscription.course,
                step__step_course_progress__status=1,
                step__step_course_progress__user=self.request.user).distinct()
            if finished_steps.count() == last_progress_chapter.step.count() and finished_chapters.count() < current_user_subscription.subscription.course.ct_course.count():
                self.new_progress_obj(chapter=last_progress_chapter, new_chapter_progress=True)
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

        # Определение открытых глав пользователя и передача их в контекст
        current_user_subscription = UsersSubscription.objects.filter(user=self.request.user, is_active=True)[0]
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
            chapter_progress = UserCourseProgress.objects.filter(user=self.request.user, status=0,
                                                                 step__chapter__serial_number=self.get_object().serial_number + 1)
            if chapter_progress and next_chapter[0].step.all():
                context['chapter_end'] = True
        previous_chapter = ChapterModel.objects.filter(course=self.get_object().course,
                                                       serial_number=self.get_object().serial_number - 1)
        if previous_chapter and self.request.GET.get('page') == '1':
            context['previous_chapter'] = previous_chapter[0]
            last_step = previous_chapter[0].step.all().order_by('serial_number').last()
            context['last_step_serial_number'] = last_step.serial_number
        last_progress_step = \
            UserCourseProgress.objects.filter(user=self.request.user,
                                              step__chapter__course=current_user_subscription.subscription.course).order_by(
                '-updated_at')[0]
        opened_chapters = ChapterModel.objects.filter(course=current_user_subscription.subscription.course,
                                                      serial_number__lte=last_progress_step.step.chapter.serial_number)
        closed_chapters = ChapterModel.objects.filter(course=current_user_subscription.subscription.course,
                                                      serial_number__gt=last_progress_step.step.chapter.serial_number)
        finished_steps = StepModel.objects.filter(chapter=self.object,
                                                  step_course_progress__user=self.request.user,
                                                  step_course_progress__status=1).order_by('serial_number')

        context['opened_chapters'] = opened_chapters
        context['closed_chapters'] = closed_chapters
        context['finished_steps'] = finished_steps

        return context
