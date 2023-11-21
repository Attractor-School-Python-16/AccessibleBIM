from django.contrib.auth.forms import SetPasswordForm
from django.test import TestCase

from accounts.tests.factories.user import UserFactory


class TestResetPasswordForm(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory.create()
        self.user.set_password('123')
        self.user.save()
        self.passwords = {
            'new_password1': '456',
            'new_password2': '456',
        }

    def test_reset_password_form_valid(self):
        form = SetPasswordForm(self.user, self.passwords)
        self.assertTrue(form.is_valid())

    def test_reset_password_form_invalid(self):
        self.passwords['new_password2'] = '789'
        form = SetPasswordForm(self.user, self.passwords)
        self.assertFalse(form.is_valid())
