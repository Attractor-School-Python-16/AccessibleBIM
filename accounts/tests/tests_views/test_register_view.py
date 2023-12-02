from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser


class TestRegisterView(TestCase):
    # fixtures = ['fixtures/08_sites.json', 'fixtures/09_socialaccount.json']

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
        response = self.client.post(reverse('accounts:register'), data=self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('accounts:verification_sent')+'?email=my_user@bimtest.com')
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.first().first_name, self.correct_data['first_name'])
        self.assertEqual(CustomUser.objects.first().last_name, self.correct_data['last_name'])
        self.assertEqual(CustomUser.objects.first().username, self.correct_data['email'])
        self.assertEqual(CustomUser.objects.first().email_verified, False)

    # def test_register_fail(self):
    #     data = self.correct_data.copy()
    #     data['email'] = 'abc.com'
    #     response = self.client.post(reverse('accounts:register'), data=data)
    #     self.assertEqual(response.status_code, HTTPStatus.OK)
    #     self.assertEqual(CustomUser.objects.count(), 0)
