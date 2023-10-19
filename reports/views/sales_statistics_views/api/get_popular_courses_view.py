from datetime import date, timedelta

from django.contrib.auth.decorators import permission_required
from django.db.models import Count
from django.http import JsonResponse

from subscription.models.user_subscription import UsersSubscription


@permission_required('accounts.can_view_sales_statistics')
def get_popular_courses_view(request, *args, **kwargs):
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
    results_from_db = UsersSubscription.objects.filter(create_at__date__gte=first_day).values(
        'subscription__course__title').annotate(count=Count('pk')).order_by('count')[:5]

    for record in results_from_db:
        result['labels'].append(record.get('subscription__course__title'))
        result['values'].append(record.get('count'))

    return JsonResponse(result)