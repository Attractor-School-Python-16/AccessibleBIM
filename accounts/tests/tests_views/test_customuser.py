from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from accounts.forms import RegisterForm
from accounts.models import CustomUser


class TestCustomUser(TestCase):
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

    def test_register(self):
        form = RegisterForm(self.correct_data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse('accounts:register'), data=self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('accounts:verification_sent')+'?email=my_user@bimtest.com')
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.first().first_name, self.correct_data['first_name'])
        self.assertEqual(CustomUser.objects.first().last_name, self.correct_data['last_name'])
        self.assertEqual(CustomUser.objects.first().username, self.correct_data['email'])
        self.assertEqual(CustomUser.objects.first().email_verified, False)

    def test_change_password(self):
        self.client.post(reverse('accounts:register'), data=self.correct_data)
        logged_in = self.client.login(email='my_user@bimtest.com', password='123')
        self.assertTrue(logged_in)
        data = {
            'old_password': '123',
            'new_password1': '000',
            'new_password2': '000'
        }
        response = self.client.post(reverse('accounts:change_password'), data=data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.client.logout()
        self.assertFalse(self.client.login(email='my_user@bimtest.com', password='123'))
        self.assertTrue(self.client.login(email='my_user@bimtest.com', password='000'))

