from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.http import JsonResponse


def get_new_users_qty_view(request, *args, **kwargs):
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

    first_day = date.today() - timedelta(days=days-1)
    results_from_db = get_user_model().objects.filter(date_joined__date__gte=first_day).values('date_joined__date').annotate(count=Count('pk')).order_by('date_joined__date')
    result['labels'] = [first_day + timedelta(days=day) for day in range(days)]
    result['values'] = [0 for _ in range(days)]
    for record in results_from_db:
        result['values'][result['labels'].index(record['date_joined__date'])] = record['count']

    # for day in range(days):
    #     new_date = first_day + timedelta(days=day)
    #     users_qty = get_user_model().objects.filter(date_joined__date=new_date).count()
    #     result['labels'].append(new_date) # .strftime('%d.%m.%y')
    #     result['values'].append(users_qty)
    return JsonResponse(result)
