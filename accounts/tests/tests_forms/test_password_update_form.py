from django.contrib.auth.forms import PasswordChangeForm
from django.test import TestCase

from accounts.tests.factories.user import UserFactory


class TestPasswordUpdateForm(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory.create()
        self.user.set_password('123')
        self.user.save()
        self.correct_passwords = {
            'old_password': '123',
            'new_password1': '000',
            'new_password2': '000'
        }

    def test_password_update_form_valid(self):
        form = PasswordChangeForm(self.user, data=self.correct_passwords)
        self.assertTrue(form.is_valid())

    def test_password_update_form_invalid_old_pass(self):
        incorrect_passwords = self.correct_passwords.copy()
        incorrect_passwords['old_password'] = '999'
        form = PasswordChangeForm(self.user, data=incorrect_passwords)
        self.assertFalse(form.is_valid())

    def test_password_update_form_invalid_new_pass(self):
        incorrect_passwords = self.correct_passwords.copy()
        incorrect_passwords['new_password2'] = '999'
        form = PasswordChangeForm(self.user, data=incorrect_passwords)
        self.assertFalse(form.is_valid())

    def test_password_update_form_empty(self):
        incorrect_passwords = {
            'old_password': '',
            'new_password1': '',
            'new_password2': ''
        }
        form = PasswordChangeForm(self.user, data=incorrect_passwords)
        self.assertFalse(form.is_valid())
