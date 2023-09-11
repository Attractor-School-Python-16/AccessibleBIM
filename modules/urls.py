from django.urls import path

from modules.views.modules import HomeView, StepTextView, StepVideoView, StepFileView, \
    TestDetailView, SubscriptionDetailView, AccountDetailView, RegisterLoginView, AccountLoginView

from modules.views.modules import ModulesListView, ModuleCreateView, ModuleDetailView, ModuleDeleteView, \
    ModuleUpdateView

from modules.views.teachers import TeachersListView, TeacherCreateView, TeacherDetailView, TeacherDeleteView, \
    TeacherUpdateView

from modules.views.course_target import CourseTargetsListView, CourseTargetCreateView, CourseTargetDetailView, \
    CourseTargetDeleteView, CourseTargetUpdateView

app_name = 'modules'

urlpatterns = [
    path('', HomeView.as_view(), name="index"),
    path('courses/', ModulesListView.as_view(), name="modules_list"),
    path('course/create/', ModuleCreateView.as_view(), name="module_create"),
    path('course/<int:pk>/detail/', ModuleDetailView.as_view(), name="module_detail"),
    path('course/<int:pk>/update/', ModuleUpdateView.as_view(), name="module_update"),
    path('course/<int:pk>/delete/', ModuleDeleteView.as_view(), name="module_delete"),

    path('teachers/', TeachersListView.as_view(), name="teachers_list"),
    path('teacher/create/', TeacherCreateView.as_view(), name="teacher_create"),
    path('teacher/<int:pk>/detail/', TeacherDetailView.as_view(), name="teacher_detail"),
    path('teacher/<int:pk>/update/', TeacherUpdateView.as_view(), name="teacher_update"),
    path('teacher/<int:pk>/delete/', TeacherDeleteView.as_view(), name="teacher_delete"),

    path('course_targets/', CourseTargetsListView.as_view(), name="course_targets_list"),
    path('course_target/create/', CourseTargetCreateView.as_view(), name="course_target_create"),
    path('course_target/<int:pk>/detail/', CourseTargetDetailView.as_view(), name="course_target_detail"),
    path('course_target/<int:pk>/update/', CourseTargetUpdateView.as_view(), name="course_target_update"),
    path('course_target/<int:pk>/delete/', CourseTargetDeleteView.as_view(), name="course_target_delete"),

    path('accounts/login/', AccountLoginView.as_view(), name="login"),
    path('accounts/register/', RegisterLoginView.as_view(), name="register"),
    path('accounts/1/', AccountDetailView.as_view(), name="profile"),  # поменять число на PK Users
    path('step/1/text/', StepTextView.as_view(), name="step_text"),  # поменять число на PK Chapter / text
    path('step/1/video/', StepVideoView.as_view(), name="step_video"),  # поменять число на PK Chapter / video
    path('step/1/file/', StepFileView.as_view(), name="step_file"),  # поменять число на PK Chapter / video
    path('teacher/1/', TeacherDetailView.as_view(), name="teacher_detail"),
    path('test/1/', TestDetailView.as_view(), name="test_bim"),  # поменять число на PK Test
    path('subscription/', SubscriptionDetailView.as_view(), name="subscription"),
]
