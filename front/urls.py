from django.urls import path

from front.views.static_view import AccessibleBIM, About, Contacts, PrivacyPolicy
from front.views.courses_view import CoursesUserListView, CourseUserDetailView

app_name = 'static_pages'

urlpatterns = [
    path("", AccessibleBIM.as_view(), name="accessible_bim"),
    path("about/", About.as_view(), name="about"),
    path("contacts/", Contacts.as_view(), name="contacts"),
    path("privacy-policy/", PrivacyPolicy.as_view(), name="privacy_policy"),
    path('courses/', CoursesUserListView.as_view(), name="course_user_list"),
    path('course/<int:pk>/detail/', CourseUserDetailView.as_view(), name="course_user_detail"),
]