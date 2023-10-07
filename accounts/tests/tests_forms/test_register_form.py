from django.test import TestCase
from accounts.forms import RegisterForm


class TestRegisterForm(TestCase):
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

    def test_register_form_valid(self):
        form = RegisterForm(self.correct_data)
        self.assertTrue(form.is_valid())

    def test_register_form_not_matching_passwords(self):
        incorrect_data = self.correct_data.copy()
        incorrect_data['password2'] = '456'
        form = RegisterForm(incorrect_data)
        self.assertFalse(form.is_valid())

    def test_register_form_incorrect_phone(self):
        incorrect_data = self.correct_data.copy()
        incorrect_data['phone_number'] = '123'
        form = RegisterForm(incorrect_data)
        self.assertFalse(form.is_valid())

    def test_register_form_missing_name(self):
        incorrect_data = self.correct_data.copy()
        incorrect_data['first_name'] = ''
        form = RegisterForm(incorrect_data)
        self.assertFalse(form.is_valid())

    def test_register_form_missing_surname(self):
        incorrect_data = self.correct_data.copy()
        incorrect_data['last_name'] = ''
        form = RegisterForm(incorrect_data)
        self.assertFalse(form.is_valid())

    def test_register_form_incorrect_email(self):
        incorrect_data = self.correct_data.copy()
        incorrect_data['email'] = 'ab.com'
        form = RegisterForm(incorrect_data)
        self.assertFalse(form.is_valid())
