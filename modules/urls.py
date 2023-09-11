from django.urls import path

from modules.views.modules import HomeView, ModulesView, StepTextView, StepVideoView, StepFileView, TeacherDetailView, \
    TestDetailView, SubscriptionDetailView, AccountDetailView, RegisterLoginView, AccountLoginView, ModuleCreateView, \
    ModulesDetailView, ModulesDeleteView, ModulesUpdateView

app_name = 'modules'

urlpatterns = [
    path('', HomeView.as_view(), name="index"),
    path('courses/', ModulesView.as_view(), name="modules_list"),
    path('course/create/', ModuleCreateView.as_view(), name="module_create"),
    path('course/<int:pk>/detail/', ModulesDetailView.as_view(), name="module_detail"),
    path('course/<int:pk>/update/', ModulesUpdateView.as_view(), name="module_update"),
    path('course/<int:pk>/delete/', ModulesDeleteView.as_view(), name="module_delete"),


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
