from django.views.generic import TemplateView


class VerificationEmailNotSentView(TemplateView):
    template_name = 'front/accounts/email/verification-email-not-sent.html'
