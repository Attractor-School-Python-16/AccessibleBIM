from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


class VerificationEmailSentView(TemplateView):
    template_name = 'accounts/email/verification-email-sent.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['email'] = self.request.GET.get('email')
        return context
