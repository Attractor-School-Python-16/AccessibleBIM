from http import HTTPStatus
from django.test import TestCase

from accounts.models import CustomUser


class TestCustomUser(TestCase):
    def setUp(self) -> None:
        # self.user = UserFactory.create(amount=1)
        self.correct_data = {
            'first_name': 'my_name',
            'last_name': 'my_surname',
            'email': 'my_user@bimtest.com',
            'phone_number': '+996555555555',
        }

    def test_register(self):
        response = self.client.post("/register/", data=self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.first().first_name, self.correct_data['first_name'])
        self.assertEqual(CustomUser.objects.first().last_name, self.correct_data['last_name'])
        self.assertEqual(CustomUser.objects.first().username, self.correct_data['email'])
        self.assertEqual(CustomUser.objects.first().email_verified, False)
