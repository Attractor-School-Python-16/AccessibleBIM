from django.urls import path

from modules.views.modules import HomeView, StepTextView, StepVideoView, StepFileView, QuizDetailView, ModeratorView

from modules.views.modules import ModulesListView, ModuleCreateView, ModuleDetailView, ModuleDeleteView, \
    ModuleUpdateView

from modules.views.teachers import TeachersListView, TeacherCreateView, TeacherDetailView, TeacherDeleteView, \
    TeacherUpdateView

from modules.views.course_target import CourseTargetsListView, CourseTargetCreateView, CourseTargetDetailView, \
    CourseTargetDeleteView, CourseTargetUpdateView

from modules.views.courses import CoursesListView, CourseCreateView, CourseDetailView, CourseDeleteView, \
    CourseUpdateView

from modules.views.chapters import ChaptersListView, ChapterCreateView, ChapterDetailView, ChapterDeleteView, \
    ChapterUpdateView

app_name = 'modules'

urlpatterns = [
    path('', HomeView.as_view(), name="index"),
    path('moderator/', ModeratorView.as_view(), name='moderator_page'),
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

    path('сhapters/', ChaptersListView.as_view(), name="chapters_list"),
    path('сhapter/create/', ChapterCreateView.as_view(), name="chapter_create"),
    path('сhapter/<int:pk>/detail/', ChapterDetailView.as_view(), name="chapter_detail"),
    path('сhapter/<int:pk>/update/', ChapterUpdateView.as_view(), name="chapter_update"),
    path('сhapter/<int:pk>/delete/', ChapterDeleteView.as_view(), name="chapter_delete"),

    path('step/1/text/', StepTextView.as_view(), name="step_text"),  # поменять число на PK Chapter / text
    path('step/1/video/', StepVideoView.as_view(), name="step_video"),  # поменять число на PK Chapter / video
    path('step/1/file/', StepFileView.as_view(), name="step_file"),  # поменять число на PK Chapter / video

    path('quiz/1/', QuizDetailView.as_view(), name="quiz_bim"),  # поменять число на PK Quiz
]
