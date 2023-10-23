from django.utils import timezone

from modules.models.user_course_progress import UserCourseProgress


# поле status по дефолту = 0
# функцию create_user_course_progress нужно вызвать в get в StepDetailView
# и результат сохранить в атрибуте класса

# Проверяем наличие объекта прогресса перед созданием, что бы избежать генерации одинаковых объектов прогресса
def create_user_course_progress(user, step):
    if not UserCourseProgress.objects.filter(user=user,
                                             step=step):
        user_course_progress = UserCourseProgress.objects.create(
            user=user,
            step=step,
        )
        return user_course_progress


# функцию update_status_user_course_progress вызываем в представлении,
# которую напишем для ссылки <a href="#" class="btn btn-success">Следующее занятие</a>
# в step_detail_text.html
def update_status_user_course_progress(user_course_progress):
    user_course_progress.status = 'finished'
    user_course_progress.updated_at = timezone.now()
    user_course_progress.save()


# решила отказаться от асинхронности  в функции удаления, лучше взять
# из модели Users_Subscription поле created_at + 30 дней и запустить функцию удаления в это время.
def delete_user_course_progress(user_course_progress):
    user_course_progress.delete()
