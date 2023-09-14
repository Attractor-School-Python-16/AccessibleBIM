from django.utils import timezone

from modules.models.user_course_progress import UserCourseProgress


#поле status по дефолту = in_progress
#функцию create_user_course_progress нужно вызвать в get в StepDetailView
# и результат сохранить в атрибуте класса
def create_user_course_progress(user, step):
    user_course_progress = UserCourseProgress.objects.create(
        user=user,
        step=step,
    )
    return user_course_progress



