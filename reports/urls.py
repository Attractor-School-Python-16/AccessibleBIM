from django.urls import path

from reports.views import UsersMainStatisticsView, UsersListStatisticsView, UserDetailedStatisticsView, \
    CoursesMainStatisticsView, SalesMainStatisticsView
from reports.views.users_statistics_views.api import get_new_users_qty_view, get_test_progress_view
from reports.views.courses_statistics_views.api import get_steps_completed_qty_view, get_lesson_types_view


app_name = 'reports'

urlpatterns = [
    path('users/', UsersMainStatisticsView.as_view(), name='stats_users_main'),
    path('users-list/', UsersListStatisticsView.as_view(), name='stats_users_list'),
    path('user/<int:pk>/', UserDetailedStatisticsView.as_view(), name='stats_user_detailed'),
    path('courses/', CoursesMainStatisticsView.as_view(), name='stats_courses_main'),
    path('sales/', SalesMainStatisticsView.as_view(), name='stats_sales_main'),

    path('get-new-users-qty/', get_new_users_qty_view, name='get_new_users_qty'),
    path('get-steps-completed-qty/', get_steps_completed_qty_view, name='get_steps_completed_qty'),
    path('get-lesson-types/', get_lesson_types_view, name='get_lesson_types'),
    path('get-test-progress/', get_test_progress_view, name='get_test_progress'),
]
