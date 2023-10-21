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
        status=CourseProgressStatusChoices.FINISHED).values(
        'step__title', completion_time=(F('updated_at') - F('created_at')))

    completion_time = {}
    counts = {}
    for record in results_from_db:
        title = record.get('step__title')
        if completion_time.get(title):
            completion_time[title] += record['completion_time']
            counts[title] += 1
        else:
            completion_time[title] = record['completion_time']
            counts[title] = 1


    for key, value in completion_time.items():
        completion_time = value / counts[key]
        result['labels'].append(key)
        result['values'].append(calculate_minutes(completion_time))

    return JsonResponse(result)


def calculate_minutes(timedelta_object):
    return timedelta_object.days *24 * 60 + timedelta_object.seconds // 60
