from django.core.paginator import Paginator
from django.http import Http404, HttpResponseNotFound
from django.views.generic import DetailView
from modules.models import ChapterModel
from modules.models.user_course_progress import UserCourseProgress
from progress.models import ProgressTest
from step.models import StepModel
from subscription.models.user_subscription import UsersSubscription
from modules.views.user_course_progress_view import create_user_course_progress


class ChapterUserDetailView(DetailView):
    model = ChapterModel
    context_object_name = 'chapter'
    template_name = 'chapters/chapter_user_detail_view.html'
    pk_url_kwarg = 'chapter_pk'

    # Проверка, что в главе сданы все тесты.
    def chapter_tests_failed(self, chapter):
        current_user = self.request.user
        tests_failed = ProgressTest.objects.filter(user=current_user, is_passed=False, test__step__chapter=chapter)
        return tests_failed

    def dispatch(self, request, *args, **kwargs):
        current_user = request.user
        # Нашел текущую активную подписку пользователя.
        current_user_subscription = UsersSubscription.objects.filter(user=current_user, is_active=True)[0]
        if current_user_subscription:
            # Если подписка есть, нашел текущий прогресс по данному курсу
            current_progress = UserCourseProgress.objects.filter(user=current_user,
                                                                 step__chapter__course=current_user_subscription.subscription.course)
            # Если нет прогресса (пользователь только начал проходить курс), то необходимо создать объект прогресса с
            # первым шагом первой главы курса. В дальнейшем, при рефакторинге кода, это можно будеть реализовать при
            # выдаче подписки.
            if not current_progress:
                current_user_course = current_user_subscription.subscription.course
                first_user_course_chapter = current_user_course.ct_course.filter(serial_number=1)[0]
                first_user_course_step = first_user_course_chapter.step.filter(serial_number=1)[0]
                current_progress = UserCourseProgress.objects.create(user=current_user,
                                                                     step=first_user_course_step)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        current_user = request.user
        # Текущая подписка юзера
        current_user_subscription = UsersSubscription.objects.filter(user=self.request.user, is_active=True)[0]
        # Последний объект прогресса
        last_progress_object = \
            UserCourseProgress.objects.filter(user=self.request.user,
                                              step__chapter__course=current_user_subscription.subscription.course).order_by(
                '-updated_at')[0]
        # Последняя глава прогресса
        last_progress_chapter = last_progress_object.step.chapter
        # Проверка текущего прогресса (на какой главе остановился пользователь). Проверка осуществляется с помощью
        # фильтрации Шагов со статусом in_progress(0). Однако, при окончании главы, все шаги имеют статус finished(1).
        # Необходимо открыть следующую главу.

        # Проверка будет проходить по серийным номерам и page пагинации. Нужно убедиться, что текущая
        # глава является главой последнего объекта прогресса.

        if last_progress_chapter == self.get_object():
            # Проверяем, что есть query параметры page
            if request.GET.get('page'):
                # Проверяем, что query параметры page являются числом
                try:
                    int(request.GET.get('page'))
                except ValueError as e:
                    return HttpResponseNotFound('Not Found')
                # Проверяем, что query параметры page соответствуют диапазону Шагов в главе
                if 0 < int(request.GET.get('page')) <= last_progress_chapter.step.count():
                    # Проверяем, что пользователь перешел с последнего шага прогресса на другой шаг(вперед или назад)
                    if last_progress_object.step.serial_number != int(request.GET.get('page')):
                        # проверяем, что последний шаг прогресса не является тестом.
                        if last_progress_object.step.test:
                            # Если он является тестом, проверяем, пройден ли тест
                            progress_test_passed = ProgressTest.objects.filter(user=current_user,
                                                                               test__step=last_progress_object.step,
                                                                               is_passed=True)
                            # Если Тест не пройден, то пользователь может перейти на другой шаг, однако статус шага теста
                            # останется неизменным. (В таблице прогресса могут быть как минимум два занчения со статусом
                            # in_progress(0) - непройденный тест и следующий шаг, на который перешел пользователь)
                            if not progress_test_passed:
                                next_step = \
                                    last_progress_chapter.step.filter(serial_number=int(request.GET.get('page')))[0]
                                # Обязательно нужно проверить, что данный прогресс шага еще не создан иначе будут
                                # создаваться одинаковые экземпляры объектов прогресса. Если объекта нет, создаем его
                                # и возвращаем get.
                                create_user_course_progress(user=current_user, step=next_step)
                                return super().get(request, *args, **kwargs)
                        # Обновляем статус последнего объекта прогресса на finished(1)
                        if last_progress_object.status == 0:
                            last_progress_object.status = 1
                            last_progress_object.save()

                        next_step = \
                            last_progress_chapter.step.filter(serial_number=int(request.GET.get('page')))[0]
                        create_user_course_progress(user=current_user, step=next_step)
                    # Если пользователь, вместо перехода на следующий шаг, перешел на прошлый и закрыл главу. Проверяем,
                    # что точно все шаги закрыты и создаем модель прогресса первого шага следующей главы

                    finished_steps = UserCourseProgress.objects.filter(user=current_user,
                                                                       step__chapter=last_progress_chapter,
                                                                       status=1)

                    # Завершенные главы.
                    finished_chapters = ChapterModel.objects.filter(
                        course=current_user_subscription.subscription.course,
                        step__step_course_progress__status=1).distinct()

                    # Если количество завершенных шагов главы совпадает с общим количеством шагов данной главы,
                    # то создаем объект прогресса первым шагом следующей главы
                    if finished_steps.count() == last_progress_chapter.step.count() and finished_chapters.count() < current_user_subscription.subscription.course.ct_course.count():
                        next_step = \
                            StepModel.objects.filter(chapter__serial_number=last_progress_chapter.serial_number + 1,
                                                     serial_number=1)[0]
                        create_user_course_progress(user=current_user, step=next_step)
                        # if not UserCourseProgress.objects.filter(user=current_user,
                        #                                          step=next_step):
                        #     UserCourseProgress.objects.create(user=current_user,
                        #                                       step=next_step)
            else:
                return HttpResponseNotFound("Not found")
        # Если пользователь пытается перейти на одну главу вперед
        elif last_progress_chapter.serial_number + 1 == self.get_object().serial_number and request.GET.get('page'):
            # Проверяем, что последний объект прогресса является последним шагом главы и имеет статус in_progress(0)
            if last_progress_object.status == 0 and last_progress_object.step == last_progress_chapter.step.order_by(
                    '-serial_number').first():
                # Проверяем, что если шаг является тестом, то он должен быть пройден
                if last_progress_object.step.test:
                    progress_test_passed = ProgressTest.objects.filter(user=current_user,
                                                                       test__step=last_progress_object.step,
                                                                       is_passed=True)
                    if not progress_test_passed:
                        # Пока возвращает 404, но потом можно будет перекидывать на непройденный тест
                        return HttpResponseNotFound("Not found")
                # Меняем статус шага.
                last_progress_object.status = 1
                last_progress_object.save()

                # Проверим, что все шаги главы завершены
                finished_steps = UserCourseProgress.objects.filter(user=current_user,
                                                                   step__chapter=last_progress_chapter,
                                                                   status=1)
                # Завершенные главы.
                finished_chapters = ChapterModel.objects.filter(
                    course=current_user_subscription.subscription.course,
                    step__step_course_progress__status=1).distinct()

                # Если количество завершенных шагов главы совпадает с общим количеством шагов данной главы,
                # то создаем объект прогресса первым шагом следующей главы
                if finished_steps.count() == last_progress_chapter.step.count() and finished_chapters.count() < current_user_subscription.subscription.course.ct_course.count():
                    next_step = StepModel.objects.filter(chapter=self.get_object(), serial_number=1)[0]

                    create_user_course_progress(user=current_user, step=next_step)
                else:
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

        # Определение открытых глав пользователя и передача их в контекст
        current_user_subscription = UsersSubscription.objects.filter(user=self.request.user, is_active=True)[0]
        next_chapter = ChapterModel.objects.filter(course=self.get_object().course,
                                                   serial_number=self.get_object().serial_number + 1)
        if next_chapter:
            context['next_chapter'] = next_chapter[0]
        previous_chapter = ChapterModel.objects.filter(course=self.get_object().course,
                                                       serial_number=self.get_object().serial_number - 1)
        if previous_chapter:
            context['previous_chapter'] = previous_chapter[0]
        last_progress_step = \
            UserCourseProgress.objects.filter(user=self.request.user,
                                              step__chapter__course=current_user_subscription.subscription.course).order_by(
                '-updated_at')[0]

        opened_chapters = ChapterModel.objects.filter(course=current_user_subscription.subscription.course,
                                                      serial_number__lte=last_progress_step.step.chapter.serial_number)

        closed_chapters = ChapterModel.objects.filter(course=current_user_subscription.subscription.course,
                                                      serial_number__gt=last_progress_step.step.chapter.serial_number)

        finished_steps = StepModel.objects.filter(chapter=self.object,
                                                  step_course_progress__status=1).order_by('serial_number')

        context['opened_chapters'] = opened_chapters
        context['closed_chapters'] = closed_chapters
        context['finished_steps'] = finished_steps

        chapter_progress = UserCourseProgress.objects.filter(user=self.request.user, status=0,
                                                             step__chapter=self.get_object())
        if not chapter_progress:
            context['chapter_end'] = True
        return context
