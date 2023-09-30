from django.urls import path

from modules.views.modules import HomeView, ModeratorView

from modules.views.modules import ModulesListView, ModuleCreateView, ModuleDetailView, ModuleDeleteView, \
    ModuleUpdateView

from modules.views.teachers import TeachersListView, TeacherCreateView, TeacherDetailView, TeacherDeleteView, \
    TeacherUpdateView

from modules.views.course_target import CourseTargetsListView, CourseTargetCreateView, CourseTargetDetailView, \
    CourseTargetDeleteView, CourseTargetUpdateView

from modules.views.courses import CoursesListView, CourseCreateView, CourseDetailView, CourseDeleteView, \
    CourseUpdateView, CourseChangeChaptersOrderView, CoursesUserListView, CourseUserDetailView

from modules.views.chapters import ChaptersListView, ChapterCreateView, ChapterDetailView, ChapterDeleteView, \
    ChapterUpdateView, ChapterChangeStepsOrderView

app_name = 'modules'

urlpatterns = [
    path('', HomeView.as_view(), name="index"),
    path('moderator/', ModeratorView.as_view(), name='moderator_page'),
    path('modules/', ModulesListView.as_view(), name="modulemodel_list"),
    path('module/create/', ModuleCreateView.as_view(), name="modulemodel_create"),
    path('module/<int:pk>/', ModuleDetailView.as_view(), name="modulemodel_detail"),
    path('module/<int:pk>/update/', ModuleUpdateView.as_view(), name="modulemodel_update"),
    path('module/<int:pk>/delete/', ModuleDeleteView.as_view(), name="modulemodel_delete"),

    path('teachers/', TeachersListView.as_view(), name="teachermodel_list"),
    path('teacher/create/', TeacherCreateView.as_view(), name="teachermodel_create"),
    path('teacher/<int:pk>/detail/', TeacherDetailView.as_view(), name="teachermodel_detail"),
    path('teacher/<int:pk>/update/', TeacherUpdateView.as_view(), name="teachermodel_update"),
    path('teacher/<int:pk>/delete/', TeacherDeleteView.as_view(), name="teachermodel_delete"),

    path('course_targets/', CourseTargetsListView.as_view(), name="coursetargetmodel_list"),
    path('course_target/create/', CourseTargetCreateView.as_view(), name="coursetargetmodel_create"),
    path('course_target/<int:pk>/detail/', CourseTargetDetailView.as_view(), name="coursetargetmodel_detail"),
    path('course_target/<int:pk>/update/', CourseTargetUpdateView.as_view(), name="coursetargetmodel_update"),
    path('course_target/<int:pk>/delete/', CourseTargetDeleteView.as_view(), name="coursetargetmodel_delete"),
    path('course/<int:pk>/change_chapters_order', CourseChangeChaptersOrderView.as_view(),
         name="change_chapters_order"),

    path('courses/', CoursesListView.as_view(), name="coursemodel_list"),
    path('course/create/', CourseCreateView.as_view(), name="coursemodel_create"),
    path('user_courses/', CoursesUserListView.as_view(), name="coursemodel_user_list"),
    path('user_course/<int:pk>/detail/', CourseUserDetailView.as_view(), name="coursemodel_user_detail"),
    path('course/<int:pk>/detail/', CourseDetailView.as_view(), name="coursemodel_detail"),
    path('course/<int:pk>/update/', CourseUpdateView.as_view(), name="coursemodel_update"),
    path('course/<int:pk>/delete/', CourseDeleteView.as_view(), name="coursemodel_delete"),
    path('course/<int:pk>/change_chapters_order', CourseChangeChaptersOrderView.as_view(),
         name="change_chapters_order"),

    path('chapters/', ChaptersListView.as_view(), name="chaptermodel_list"),
    path('chapter/create/', ChapterCreateView.as_view(), name="chaptermodel_create"),
    path('chapter/<int:pk>/detail/', ChapterDetailView.as_view(), name="chaptermodel_detail"),
    path('chapter/<int:pk>/update/', ChapterUpdateView.as_view(), name="chaptermodel_update"),
    path('chapter/<int:pk>/delete/', ChapterDeleteView.as_view(), name="chaptermodel_delete"),
    path('chapter/<int:pk>/change_steps_order', ChapterChangeStepsOrderView.as_view(),
         name="change_steps_order"),
]
