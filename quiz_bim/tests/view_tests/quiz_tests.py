from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import *
from django.urls import reverse

from quiz_bim.models import QuizBim
from quiz_bim.tests.factories import QuizBimFactory
from quiz_bim.tests.urils import login_superuser_test


class TestQuizBimListView(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = reverse("quiz_bim:quizbim_list")
        cls.superuser, _ = get_user_model().objects.get_or_create(email="admin@admin.com", password="admin",
                                                                  is_superuser=True)
        super().setUpClass()

    @login_superuser_test
    def test_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertQuerysetEqual(response.context['tests'], QuizBim.objects.all(), ordered=False)
        self.assertTemplateUsed(response, 'quiz_bim/quiz_bim/quiz_bim_list.html')
        self.assertFalse(response.context['is_paginated'])
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')


class TestQuizBimDetailView(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.superuser, _ = get_user_model().objects.get_or_create(email="admin@admin.com", password="admin", is_superuser=True)
        super().setUpClass()

    @login_superuser_test
    def test_detail_view(self):
        quiz = QuizBimFactory.create()
        response = self.client.get(reverse("quiz_bim:quizbim_detail", kwargs={"pk": quiz.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['test'], quiz)
        self.assertTemplateUsed(response, 'quiz_bim/quiz_bim/quiz_bim_detail.html')
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    @login_superuser_test
    def test_not_found(self):
        response = self.client.get(reverse("quiz_bim:quizbim_detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class TestQuizBimCreateView(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.correct_form_data = {
            "title": "Quiz",
            "questions_qty": 5,
        }
        cls.url = reverse("quiz_bim:quizbim_create")
        cls.superuser, _ = get_user_model().objects.get_or_create(email="admin@admin.com", password="admin", is_superuser=True)
        super().setUpClass()

    @login_superuser_test
    def test_create_view(self):
        previous_count = QuizBim.objects.count()
        response = self.client.post(self.url, data=self.correct_form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(QuizBim.objects.count() - previous_count, 1)
        quiz = QuizBim.objects.latest('create_at')
        self.assertRedirects(response, reverse("quiz_bim:quizbim_list"))

    @login_superuser_test
    def test_invalid_data(self):
        invalid_data = {
            "title": "",
            "questions_qty": "string",
        }
        previous_count = QuizBim.objects.count()
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(previous_count, QuizBim.objects.count())


class TestQuizBimUpdateView(TestCase):
    quiz = None

    @classmethod
    def setUpClass(cls):
        cls.superuser, _ = get_user_model().objects.get_or_create(email="admin@admin.com", password="admin", is_superuser=True)
        super().setUpClass()

    def setUp(self) -> None:
        self.quiz = QuizBimFactory.create()
        self.url = reverse("quiz_bim:quizbim_update", kwargs={"pk": self.quiz.pk})

    @login_superuser_test
    def test_update_view(self):
        new_data = {
            "title": "New title",
            "questions_qty": 1,
        }
        response = self.client.post(self.url, data=new_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.quiz.refresh_from_db()
        self.assertEqual(self.quiz.title, "New title")
        self.assertEqual(self.quiz.questions_qty, 1)
        # self.assertRedirects(response, reverse("quiz_bim:tests_list"))

    @login_superuser_test
    def test_invalid_data(self):
        invalid_data = {
            "title": "",
            "questions_qty": "string"
        }
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @login_superuser_test
    def test_not_found(self):
        response = self.client.get(reverse("quiz_bim:quizbim_update", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class TestQuizBimDeleteView(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.superuser, _ = get_user_model().objects.get_or_create(email="admin@admin.com", password="admin", is_superuser=True)
        super().setUpClass()

    def setUp(self) -> None:
        self.quiz = QuizBimFactory.create()
        self.url = reverse("quiz_bim:quizbim_delete", kwargs={"pk": self.quiz.pk})

    @login_superuser_test
    def test_delete_view(self):
        previous_count = QuizBim.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(previous_count - QuizBim.objects.count(), 1)
        self.assertRedirects(response, reverse("quiz_bim:quizbim_list"))

    @login_superuser_test
    def test_not_found(self):
        previous_count = QuizBim.objects.count()
        response = self.client.post(reverse("quiz_bim:quizbim_delete", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(previous_count, QuizBim.objects.count())
