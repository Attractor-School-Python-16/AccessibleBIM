from http import HTTPStatus

from django.test import *
from django.urls import reverse

from quiz_bim.tests.factories import QuestionBimFactory


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
