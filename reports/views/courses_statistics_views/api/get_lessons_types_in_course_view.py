from django.db.models import Count
from django.http import JsonResponse

from step.models import StepModel


def get_lesson_types_in_course_view(request, *args, **kwargs):
    result = {
        'error': False,
        'error_messages': [],
        'labels': [],
        'values': []
    }

    course_pk = request.GET.get('course')

    results_from_db = StepModel.objects.filter(chapter__course__pk=course_pk).values('lesson_type').annotate(
        lessons_qty=Count('lesson_type'))
    for record in results_from_db:
        result['labels'].append(record['lesson_type'])
        result['values'].append(record['lessons_qty'])

    return JsonResponse(result)
