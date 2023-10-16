from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse

from progress.models import ProgressTest
from step.models import StepModel


@permission_required('accounts.can_view_user_statistics')
def get_test_progress_view(request, *args, **kwargs):
    if request.method == "GET":
        result = {
            'error': False,
            'error_messages': [],
            'labels': [],
            'values': []
        }

        try:
            user_pk = int(request.GET['user'])
            course_pk = int(request.GET['course'])
        except ValueError or KeyError:
            result['error'] = True
            result['error_messages'] = 'Wrong query parameters'
            return JsonResponse(result)

        step_test = StepModel.objects.filter(chapter__course__pk=course_pk, test__isnull=False).values('test_id')
        test_progress = ProgressTest.objects.filter(user__pk=user_pk, test__pk__in=step_test, is_passed=True)
        for t in test_progress:
            result['labels'].append(t.test.title)
            result['values'].append(t.accuracy()*100)
        return JsonResponse(result)
