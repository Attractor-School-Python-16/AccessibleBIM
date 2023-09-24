from http import HTTPStatus

from django.test import *
from django.urls import reverse

from quiz_bim.models import QuestionBim
from quiz_bim.tests.factories import QuestionBimFactory, QuizBimFactory


class TestQuestionBimDetailView(TestCase):

    def test_detail_view(self):
        question = QuestionBimFactory.create()
        response = self.client.get(reverse("quiz_bim:question_detail", kwargs={"pk": question.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['question'], question)
        self.assertTemplateUsed(response, 'quiz_bim/question_bim/question_bim_detail.html')
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_not_found(self):
        response = self.client.get(reverse("quiz_bim:question_detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class TestQuestionBimCreateView(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.correct_form_data = {
            "title": "Question"
        }
        quiz = QuizBimFactory.create()
        cls.url = reverse("quiz_bim:question_create", kwargs={"pk": quiz.pk})
        super().setUpClass()

    def test_create_view(self):
        previous_count = QuestionBim.objects.count()
        response = self.client.post(self.url, data=self.correct_form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(QuestionBim.objects.count() - previous_count, 1)

    def test_invalid_data(self):
        invalid_data = {
            "title": ""
        }
        previous_count = QuestionBim.objects.count()
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(previous_count, QuestionBim.objects.count())


class TestQuestionBimUpdateView(TestCase):
    question = None

    def setUp(self) -> None:
        self.question = QuestionBimFactory.create()
        self.url = reverse("quiz_bim:question_update", kwargs={"pk": self.question.pk})

    def test_update_view(self):
        new_data = {
            "title": "New title"
        }
        response = self.client.post(self.url, data=new_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.question.refresh_from_db()
        self.assertEqual(self.question.title, "New title")

    def test_invalid_data(self):
        invalid_data = {
            "title": ""
        }
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_not_found(self):
        response = self.client.get(reverse("quiz_bim:question_update", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class TestQuestionBimDeleteView(TestCase):

    def setUp(self) -> None:
        self.question = QuestionBimFactory.create()
        self.url = reverse("quiz_bim:question_delete", kwargs={"pk": self.question.pk})

    def test_delete_view(self):
        previous_count = QuestionBim.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(previous_count - QuestionBim.objects.count(), 1)

    def test_not_found(self):
        previous_count = QuestionBim.objects.count()
        response = self.client.post(reverse("quiz_bim:question_delete", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(previous_count, QuestionBim.objects.count())
