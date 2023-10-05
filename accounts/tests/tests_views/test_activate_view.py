from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.tests.factories.user import UserFactory
from accounts.tokens import account_activation_token


class TestRegisterView(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory.create()
        self.user.set_password('123')
        self.user.save()
        # методы, применяемые в функции activate_email для генерации ссылки
        self.uidb = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = account_activation_token.make_token(self.user)

    def test_activate_user(self):
        self.assertFalse(self.user.email_verified)
        response = self.client.get(reverse('accounts:activate', kwargs={
            'uidb64': self.uidb,
            'token': self.token,
        }))
        self.user.refresh_from_db()
        self.assertRedirects(response, reverse('accounts:profile'))
        self.assertTrue(self.user.email_verified)

    def test_invalid_verification_link(self):
        self.assertFalse(self.user.email_verified)
        response = self.client.get(reverse('accounts:activate', kwargs={
            # invalid uidb64 and token
            'uidb64': 'AB',
            'token': 'bv9df1-87f396b36d4fa7t8125ba5033bb8a49b',
        }))
        self.user.refresh_from_db()
        self.assertRedirects(response, reverse('accounts:invalid_verification_link'))
        self.assertFalse(self.user.email_verified)

    def test_activate_user_twice(self):
        """
        Email verification done twice. At first time it activates account and redirects user to the profile.
        At second time it does nothing and redirects to 'invalid verification link' page.
        """
        self.test_activate_user()
        self.assertTrue(self.user.email_verified)
        response = self.client.get(reverse('accounts:activate', kwargs={
            'uidb64': self.uidb,
            'token': self.token,
        }))
        self.user.refresh_from_db()
        self.assertRedirects(response, reverse('accounts:invalid_verification_link'))
        self.assertTrue(self.user.email_verified)
