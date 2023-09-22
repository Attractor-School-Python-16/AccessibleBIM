from django.shortcuts import render
from django.views import View


class InvalidVerificationLinkView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/email/invalid_verification_link.html')
