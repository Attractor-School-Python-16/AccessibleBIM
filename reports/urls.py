from django.urls import path

from reports.views import UsersMainStatisticsView

urlpatterns = [
    path('users/', UsersMainStatisticsView.as_view(), name='stats_users_main'),
]
