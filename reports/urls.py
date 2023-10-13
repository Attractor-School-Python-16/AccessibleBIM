from django.urls import path

from reports.views import UsersMainStatisticsView, CoursesMainStatisticsView
from reports.views.courses_statistics_views.api import get_steps_completed_qty_view
from reports.views.users_statistics_views.api import get_new_users_qty_view

app_name = 'reports'

urlpatterns = [
    path('users/', UsersMainStatisticsView.as_view(), name='stats_users_main'),
    path('courses/', CoursesMainStatisticsView.as_view(), name='stats_courses_main'),

    path('get-new-users-qty/', get_new_users_qty_view, name='get_new_users_qty'),
    path('get-steps-completed-qty/', get_steps_completed_qty_view, name='get_steps_completed_qty'),
]
