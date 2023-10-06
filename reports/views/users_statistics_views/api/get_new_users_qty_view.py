from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.http import JsonResponse


def get_new_users_gty_view(request, *args, **kwargs):
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
    for day in range(days):
        new_date = first_day + timedelta(days=day)
        users_qty = get_user_model().objects.filter(date_joined__date=new_date).count()
        result['labels'].append(new_date.strftime('%d.%m.%y'))
        result['values'].append(users_qty)
    return JsonResponse(result)
