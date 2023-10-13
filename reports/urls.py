from django.urls import path

from reports.views import UsersMainStatisticsView, UsersListStatisticsView, UserDetailedStatisticsView
from reports.views.users_statistics_views.api import get_new_users_gty_view

app_name = 'reports'

urlpatterns = [
    path('users/', UsersMainStatisticsView.as_view(), name='stats_users_main'),
    path('users-list/', UsersListStatisticsView.as_view(), name='stats_users_list'),
    path('user/<int:pk>/', UserDetailedStatisticsView.as_view(), name='stats_user_detailed'),

    path('get-new-users-qty/', get_new_users_gty_view, name='get_new_users_qty'),
]
