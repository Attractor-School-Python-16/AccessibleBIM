from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'index.html'


class ModulesView(TemplateView):
    template_name = 'modules/modules_view.html'


class ModulesDetailView(TemplateView):
    template_name = 'modules/modules_detail.html'


class AccountDetailView(TemplateView):
    template_name = 'accounts/profile.html'


class AccountLoginView(TemplateView):
    template_name = 'accounts/login.html'


class RegisterLoginView(TemplateView):
    template_name = 'accounts/register.html'


class StepVideoView(TemplateView):
    template_name = 'steps/step_detail_video.html'


class StepTextView(TemplateView):
    template_name = 'steps/step_detail_text.html'


class StepFileView(TemplateView):
    template_name = 'steps/step_detail_file.html'


class TeacherDetailView(TemplateView):
    template_name = 'teachers/teacher_detail.html'
