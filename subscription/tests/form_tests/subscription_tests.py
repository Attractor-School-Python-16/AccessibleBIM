import random

from django.test import TestCase

from modules.tests import CourseFactory
from subscription.forms.subscription_form import SubscriptionForm


class TestSubscriptionForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.correct_form_data = {
            "course": "",
            "price": random.randint(1, 100),
            "is_published": random.choice([True, False])
        }
        super().setUpTestData()

    def test_question_form(self):
        form = SubscriptionForm(data=self.correct_form_data)
        self.assertFalse(form.is_valid())

    def test_question_form_invalid(self):
        invalid_data = {
            "course": CourseFactory.create(),
            "price": "",
            "is_published": random.choice([True, False])
        }
        form = SubscriptionForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_invalid_is_published_field(self):
        invalid_data = {
            "course": CourseFactory.create(),
            "price": random.randint(1, 100),
            "is_published": ""
        }
        form = SubscriptionForm(data=invalid_data)
        self.assertTrue(form.is_valid())
