from django.urls import path

from front.views.chapter_progress_view import ChapterUserDetailView
from front.views.static_view import AccessibleBIM, About, PrivacyPolicy, TermsOfUse
from front.views.courses_view import CoursesUserListView, CourseUserDetailView

app_name = 'front'

urlpatterns = [
    path("", AccessibleBIM.as_view(), name="accessible_bim"),
    path("about/", About.as_view(), name="about"),
    # path("contacts/", Contacts.as_view(), name="contacts"),
    path("privacy-policy/", PrivacyPolicy.as_view(), name="privacy_policy"),
    path("terms_of_use/", TermsOfUse.as_view(), name="terms_of_use"),
    path('courses/', CoursesUserListView.as_view(), name="course_user_list"),
    path('course/<int:pk>/detail/', CourseUserDetailView.as_view(), name="course_user_detail"),
    path('chapter/<int:chapter_pk>/', ChapterUserDetailView.as_view(), name="chaptermodel_user_detail")
]
