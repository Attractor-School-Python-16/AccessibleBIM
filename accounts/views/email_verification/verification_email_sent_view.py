from django.shortcuts import render
from django.views import View


class VerificationEmailSentView(View):
    def get(self, request, *args, **kwargs):
        email = request.GET.get('email')
        return render(request, 'accounts/email/verification-email-sent.html', context={'email': email})
