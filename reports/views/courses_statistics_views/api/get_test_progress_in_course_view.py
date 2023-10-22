from django.contrib.auth.decorators import permission_required
from django.db.models import Avg, Count, Sum, Q, F
from django.http import JsonResponse

from progress.models import ProgressTest
from step.models import StepModel


@permission_required('accounts.can_view_course_statistics')
def get_test_progress_in_course_view(request, *args, **kwargs):
    if request.method == "GET":
        result = {
            'error': False,
            'error_messages': [],
            'labels': [],
            'values': []
        }

        try:
            course_pk = int(request.GET['course'])
        except ValueError or KeyError:
            result['error'] = True
            result['error_messages'] = 'Wrong query parameters'
            return JsonResponse(result)

        step_test = StepModel.objects.filter(chapter__course__pk=course_pk, test__isnull=False).values('test_id')
        test_progress = ProgressTest.objects.filter(test__pk__in=step_test, is_passed=True).values('test__pk',
                        'test__title').annotate(total=Count(F('pk'), filter=Q(user_progress__answer__is_correct=True)
                        ) * 100 / Count(F('test__question_bim__pk')))

        for t in test_progress:
            result['labels'].append(t['test__title'])
            result['values'].append(t['total'])

        print('test_progress', test_progress)

        return JsonResponse(result)
