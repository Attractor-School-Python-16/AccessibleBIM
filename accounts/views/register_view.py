from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import login, get_user_model
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode, urlencode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.utils.translation import gettext_lazy as _

from accounts.tokens import account_activation_token

from accounts.forms import RegisterForm
from accounts.models import CustomUser


def activate_email(request, user, to_email):
    mail_subject = _('Activate your user account')
    message = render_to_string('accounts/email/verification_email.html', {
        'user': user.get_full_name(),
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        return redirect(reverse('accounts:verification_sent') + '?' + urlencode({'email': to_email}))
    else:
        return redirect('accounts:verification_sending_error')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.email_verified = True
        user.save()
        login(request, user, backend='accounts.backends.EmailBackend')
        return redirect('accounts:profile')
    else:
        return redirect('accounts:invalid_verification_link')


class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    model = CustomUser
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = user.email
        user.email_verified = False
        user.save()
        return activate_email(self.request, user, form.cleaned_data.get('email'))


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = CustomUser.objects.get(email=sociallogin.user.email)
        if user and not sociallogin.is_existing:
            sociallogin.connect(request, user)
