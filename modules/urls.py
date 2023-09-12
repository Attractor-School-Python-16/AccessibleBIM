from django.urls import path

from modules.views.modules import HomeView, StepTextView, StepVideoView, StepFileView, \
    TestDetailView, SubscriptionDetailView, AccountDetailView, RegisterLoginView, AccountLoginView

from modules.views.modules import ModulesListView, ModuleCreateView, ModuleDetailView, ModuleDeleteView, \
    ModuleUpdateView

from modules.views.teachers import TeachersListView, TeacherCreateView, TeacherDetailView, TeacherDeleteView, \
    TeacherUpdateView

from modules.views.course_target import CourseTargetsListView, CourseTargetCreateView, CourseTargetDetailView, \
    CourseTargetDeleteView, CourseTargetUpdateView

from modules.views.courses import CoursesListView, CourseCreateView, CourseDetailView, CourseDeleteView, \
    CourseUpdateView

app_name = 'modules'

urlpatterns = [
    path('', HomeView.as_view(), name="index"),
    path('modules/', ModulesListView.as_view(), name="modules_list"),
    path('module/create/', ModuleCreateView.as_view(), name="module_create"),
    path('module/<int:pk>/detail/', ModuleDetailView.as_view(), name="module_detail"),
    path('module/<int:pk>/update/', ModuleUpdateView.as_view(), name="module_update"),
    path('module/<int:pk>/delete/', ModuleDeleteView.as_view(), name="module_delete"),

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

    path('courses/', CoursesListView.as_view(), name="courses_list"),
    path('course/create/', CourseCreateView.as_view(), name="course_create"),
    path('course/<int:pk>/detail/', CourseDetailView.as_view(), name="course_detail"),
    path('course/<int:pk>/update/', CourseUpdateView.as_view(), name="course_update"),
    path('course/<int:pk>/delete/', CourseDeleteView.as_view(), name="course_delete"),

    path('subscription/', SubscriptionDetailView.as_view(), name="subscription"),
]
