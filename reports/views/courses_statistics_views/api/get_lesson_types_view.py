from django.contrib.auth.decorators import permission_required
from django.db.models import Count
from django.http import JsonResponse

from step.models import StepModel


@permission_required('accounts.can_view_course_statistics')
def get_lesson_types_view(request, *args, **kwargs):
    if request.method == "GET":
        result = {
            'error': False,
            'error_messages': [],
            'labels': [],
            'values': []
        }

        results_from_db = StepModel.objects.values('lesson_type').annotate(lessons_qty=Count('lesson_type'))
        for record in results_from_db:
            result['labels'].append(record['lesson_type'])
            result['values'].append(record['lessons_qty'])

        return JsonResponse(result)
