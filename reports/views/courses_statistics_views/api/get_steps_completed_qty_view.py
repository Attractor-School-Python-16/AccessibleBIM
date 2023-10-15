from datetime import date, timedelta

from django.db.models import Count
from django.http import JsonResponse

from modules.models.user_course_progress import UserCourseProgress, CourseProgressStatusChoices


def get_steps_completed_qty_view(request, *args, **kwargs):
    result = {
        'error': False,
        'error_messages': [],
        'labels': [],
        'values': []
    }

    try:
        days = int(request.GET.get('days'))
    except ValueError:
        result['error'] = True
        result['error_messages'].append('Invalid query parameter')
        return JsonResponse(result)

    first_day = date.today() - timedelta(days=days - 1)
    results_from_db = UserCourseProgress.objects.filter(updated_at__date__gte=first_day,
                                                        status=CourseProgressStatusChoices.FINISHED).values(
        'updated_at__date').annotate(count=Count('pk')).order_by('updated_at__date')
    result['labels'] = [first_day + timedelta(days=day) for day in range(days)]
    result['values'] = [0 for _ in range(days)]
    for record in results_from_db:
        result['values'][result['labels'].index(record['updated_at__date'])] = record['count']
    return JsonResponse(result)
