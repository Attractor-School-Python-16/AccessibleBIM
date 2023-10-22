from django.db.models import Count, F, Avg, Q
from django.http import JsonResponse

from modules.models.user_course_progress import UserCourseProgress, CourseProgressStatusChoices
from step.models import StepModel


def get_steps_completion_time_view(request, *args, **kwargs):
    result = {
        'error': False,
        'error_messages': [],
        'labels': [],
        'values': []
    }

    course_pk = request.GET.get('course')
    results_from_db = UserCourseProgress.objects.filter(step__chapter__course__pk=course_pk,
        status=CourseProgressStatusChoices.FINISHED).values('step__title').annotate(
        completion_time=(Avg(F('updated_at') - F('created_at'))))

    for record in results_from_db:
        result['labels'].append(record['step__title'])
        result['values'].append(calculate_minutes(record['completion_time']))

    return JsonResponse(result)


def calculate_minutes(timedelta_object):
    return timedelta_object.days *24 * 60 + timedelta_object.seconds // 60
