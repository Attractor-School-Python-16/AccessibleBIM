from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class TestRegisterView(TestCase):
    def setUp(self) -> None:
        self.correct_data = {
            'first_name': 'my_name',
            'last_name': 'my_surname',
            'father_name': '',
            'email': 'my_user@bimtest.com',
            'password1': '123',
            'password2': '123',
            'country': 'KG',
            'phone_number': '+996555555555',
            'job_title': '',
            'type_corp': '7',
            'company': '',
            'captcha_0': 'dummy-value',
            'captcha_1': 'PASSED',
        }

    def change_password(self):
        self.client.post(reverse('accounts:register'), data=self.correct_data)
        logged_in = self.client.login(email='my_user@bimtest.com', password='123')
        self.assertTrue(logged_in)
        data = {
            'old_password': '123',
            'new_password1': '000',
            'new_password2': '000'
        }
        return data

    def test_change_password(self):
        data = self.change_password()
        response = self.client.post(reverse('accounts:change_password'), data=data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_login_after_changing_password(self):
        data = self.change_password()
        self.client.post(reverse('accounts:change_password'), data=data)
        self.client.logout()
        self.assertFalse(self.client.login(email='my_user@bimtest.com', password='123'))

    def test_login_after_changing_password_fail(self):
        data = self.change_password()
        self.client.post(reverse('accounts:change_password'), data=data)
        self.client.logout()
        self.assertTrue(self.client.login(email='my_user@bimtest.com', password='000'))
