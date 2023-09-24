from http import HTTPStatus

from django.test import *
from django.urls import reverse

from quiz_bim.models import QuizBim
from quiz_bim.tests.factories import QuizBimFactory


class TestQuizBimListView(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = reverse("quiz_bim:tests_list")
        super().setUpClass()

    def test_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertQuerysetEqual(response.context['tests'], QuizBim.objects.all())
        self.assertTemplateUsed(response, 'quiz_bim/quiz_bim/quiz_bim_list.html')
        self.assertFalse(response.context['is_paginated'])
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')


class TestQuizBimDetailView(TestCase):

    def test_detail_view(self):
        quiz = QuizBimFactory.create()
        response = self.client.get(reverse("quiz_bim:test_detail", kwargs={"pk": quiz.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['test'], quiz)
        self.assertTemplateUsed(response, 'quiz_bim/quiz_bim/quiz_bim_detail.html')
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_not_found(self):
        response = self.client.get(reverse("quiz_bim:test_detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
