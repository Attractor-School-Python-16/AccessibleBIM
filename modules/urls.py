from django.urls import path

from modules.views.modules import HomeView, ModulesView, ModulesDetailView, StepTextView, StepVideoView, StepFileView

app_name = 'modules'

urlpatterns = [
    path('', HomeView.as_view(), name="index"),
    path('courses/', ModulesView.as_view(), name="modules"),
    path('course/1', ModulesDetailView.as_view(), name="module"),# поменять число на PK Courses
    path('accounts/login/', ModulesDetailView.as_view(), name="login"),
    path('accounts/register/', ModulesDetailView.as_view(), name="register"),
    path('accounts/1/', ModulesDetailView.as_view(), name="profile"), # поменять число на PK Users
    path('step/1/text/', StepTextView.as_view(), name="step_text"), # поменять число на PK Chapter / text
    path('step/1/video/', StepVideoView.as_view(), name="step_video"), # поменять число на PK Chapter / video
    path('step/1/file/', StepFileView.as_view(), name="step_file"), # поменять число на PK Chapter / video
]
