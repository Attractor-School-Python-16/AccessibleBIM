from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from quiz_bim.models import AnswerBim
from quiz_bim.tests.factories import QuestionBimFactory, AnswerBimFactory


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


class TestAnswerBimUpdateView(TestCase):
    answer = None

    def setUp(self) -> None:
        self.answer = AnswerBimFactory.create()
        self.url = reverse("quiz_bim:answer_update", kwargs={"pk": self.answer.pk})

    def test_update_view(self):
        new_data = {
            "answer": "New title",
            "is_correct": False
        }
        response = self.client.post(self.url, data=new_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.answer.refresh_from_db()
        self.assertEqual(self.answer.answer, "New title")
        self.assertEqual(self.answer.is_correct, False)

    def test_invalid_data(self):
        invalid_data = {
            "title": "",
            "is_correct": "string"
        }
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_not_found(self):
        response = self.client.get(reverse("quiz_bim:answer_update", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class TestAnswerBimDeleteView(TestCase):

    def setUp(self) -> None:
        self.answer = AnswerBimFactory.create()
        self.url = reverse("quiz_bim:answer_delete", kwargs={"pk": self.answer.pk})

    def test_delete_view(self):
        previous_count = AnswerBim.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(previous_count - AnswerBim.objects.count(), 1)

    def test_not_found(self):
        previous_count = AnswerBim.objects.count()
        response = self.client.post(reverse("quiz_bim:answer_delete", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(previous_count, AnswerBim.objects.count())
