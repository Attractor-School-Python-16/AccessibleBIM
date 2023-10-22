from datetime import date, timedelta

from django.contrib.auth.decorators import permission_required
from django.db.models import Count
from django.http import JsonResponse

from subscription.models.user_subscription import UsersSubscription


@permission_required('accounts.can_view_sales_statistics')
def get_new_subscriptions_qty_view(request, *args, **kwargs):
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
        'create_at__date').annotate(count=Count('pk')).order_by('create_at__date')
    result['labels'] = [first_day + timedelta(days=day) for day in range(days)]
    result['values'] = [0 for _ in range(days)]
    for record in results_from_db:
        result['values'][result['labels'].index(record['create_at__date'])] = record['count']
    return JsonResponse(result)