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
