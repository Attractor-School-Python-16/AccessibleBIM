from django.views.generic import TemplateView


class InvalidVerificationLinkView(TemplateView):
    template_name = 'front/accounts/email/invalid_verification_link.html'
