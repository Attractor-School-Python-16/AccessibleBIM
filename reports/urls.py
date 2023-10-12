from django.urls import path

from reports.views import UsersMainStatisticsView
from reports.views.users_statistics_views.api import get_new_users_gty_view

app_name = 'reports'

urlpatterns = [
    path('users/', UsersMainStatisticsView.as_view(), name='stats_users_main'),

    path('get-new-users-qty/', get_new_users_gty_view, name='get_new_users_qty'),
]
