from http import HTTPStatus

from django.contrib.auth.tokens import default_token_generator
from django.test import TestCase

from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.tests.factories.user import UserFactory


class TestResetPasswordView(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory.create()
        self.user.set_password('123')
        self.user.save()
        self.tokens = {
            'uidb64': urlsafe_base64_encode(force_bytes(self.user.pk)),
            'token': default_token_generator.make_token(self.user),
        }
        self.hidden_tokens = {
            'uidb64': self.tokens.get('uidb64'),
            'token': 'set-password',
        }

    def test_get_email_for_resetting_password(self):
        response = self.client.post(reverse('accounts:password_reset'), data={'email': self.user.email})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('accounts:password_reset_done'))

    def test_get_reset_password_form(self):
        response = self.client.post(reverse('accounts:password_reset_confirm', kwargs=self.tokens))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('accounts:password_reset_confirm', kwargs=self.hidden_tokens))

    def reset_password_for_test(self, passwords=None):
        self.test_get_reset_password_form()
        if passwords is None:
            passwords = {
                'new_password1': '456',
                'new_password2': '456',
            }
        response = self.client.post(reverse('accounts:password_reset_confirm', kwargs=self.hidden_tokens),
                                    data=passwords)
        return response

    def test_reset_password(self):
        response = self.reset_password_for_test()
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('accounts:password_reset_complete'))

    def test_login_new_password(self):
        self.reset_password_for_test()
        logged_in = self.client.login(email=self.user.email, password='456')
        self.assertTrue(logged_in)

    def test_login_new_password_fail(self):
        """
        In this test user tries to log in with old password that has already been reset
        """
        self.reset_password_for_test()
        logged_in = self.client.login(email=self.user.email, password='123')
        self.assertFalse(logged_in)

    def test_reset_forgot_password_fail(self):
        incorrect_passwords = {
            'new_password1': '789',
            'new_password2': '456',
        }
        response = self.reset_password_for_test(passwords=incorrect_passwords)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.client.logout()
        logged_in = self.client.login(email=self.user.email, password='123')
        self.assertTrue(logged_in)
