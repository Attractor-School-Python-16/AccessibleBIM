from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from quiz_bim.models import AnswerBim
from quiz_bim.tests.factories import QuestionBimFactory


class TestAnswerBimCreateView(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.correct_form_data = {
            "answer": "Answer",
            "is_correct": True
        }
        question = QuestionBimFactory.create()
        cls.url = reverse("quiz_bim:answer_create", kwargs={"pk": question.pk})
        super().setUpClass()

    def test_create_view(self):
        previous_count = AnswerBim.objects.count()
        response = self.client.post(self.url, data=self.correct_form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(AnswerBim.objects.count() - previous_count, 1)

    def test_invalid_data(self):
        invalid_data = {
            "answer": "",
            "is_correct": -1
        }
        previous_count = AnswerBim.objects.count()
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(previous_count, AnswerBim.objects.count())
