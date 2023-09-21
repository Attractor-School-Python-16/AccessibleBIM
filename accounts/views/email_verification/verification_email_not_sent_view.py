from django.shortcuts import render
from django.views import View


class VerificationEmailNotSentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/email/verification-email-not-sent.html')
