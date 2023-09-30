from django.views.generic import TemplateView


class VerificationEmailNotSentView(TemplateView):
    template_name = 'accounts/email/verification-email-not-sent.html'
