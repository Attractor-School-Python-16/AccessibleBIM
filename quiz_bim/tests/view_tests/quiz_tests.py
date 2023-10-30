from http import HTTPStatus

from django.urls import reverse

from quiz_bim.models import QuizBim
from quiz_bim.tests.factories import QuizBimFactory
from quiz_bim.tests.utils import login_superuser, CustomTestCase


class TestQuizBimListView(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("quiz_bim:quizbim_list")
        super().setUpTestData()

    @login_superuser
    def test_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertQuerysetEqual(response.context['tests'], QuizBim.objects.all(), ordered=False)
        self.assertTemplateUsed(response, 'quiz_bim/quiz_bim/quiz_bim_list.html')
        self.assertFalse(response.context['is_paginated'])
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_no_permissions(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestQuizBimDetailView(CustomTestCase):

    @login_superuser
    def test_detail_view(self):
        quiz = QuizBimFactory.create()
        response = self.client.get(reverse("quiz_bim:quizbim_detail", kwargs={"pk": quiz.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['test'], quiz)
        self.assertTemplateUsed(response, 'quiz_bim/quiz_bim/quiz_bim_detail.html')
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    @login_superuser
    def test_not_found(self):
        response = self.client.get(reverse("quiz_bim:quizbim_detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_anonymous(self):
        quiz = QuizBimFactory.create()
        response = self.client.get(reverse("quiz_bim:quizbim_detail", kwargs={"pk": quiz.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_no_permissions(self):
        self.client.force_login(self.user)
        quiz = QuizBimFactory.create()
        response = self.client.get(reverse("quiz_bim:quizbim_detail", kwargs={"pk": quiz.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestQuizBimCreateView(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.correct_form_data = {"title": "Quiz"}
        cls.url = reverse("quiz_bim:quizbim_create")
        super().setUpTestData()

    @login_superuser
    def test_create_view(self):
        previous_count = QuizBim.objects.count()
        response = self.client.post(self.url, data=self.correct_form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(QuizBim.objects.count() - previous_count, 1)
        quiz = QuizBim.objects.latest('create_at')
        self.assertRedirects(response, reverse("quiz_bim:quizbim_detail", kwargs={"pk": quiz.pk}))
        self.assertEqual(quiz.title, self.correct_form_data['title'])

    def test_anonymous(self):
        response = self.client.post(self.url, data=self.correct_form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_no_permissions(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, data=self.correct_form_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    @login_superuser
    def test_invalid_empty_title_field(self):
        invalid_data = {"title": ""}
        previous_count = QuizBim.objects.count()
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(QuizBim.objects.count() - previous_count, 1)
        quiz = QuizBim.objects.latest('create_at')
        self.assertEqual(quiz.title, None)


class TestQuizBimUpdateView(CustomTestCase):
    quiz = None

    def setUp(self) -> None:
        self.quiz = QuizBimFactory.create()
        self.url = reverse("quiz_bim:quizbim_update", kwargs={"pk": self.quiz.pk})

    @login_superuser
    def test_update_view(self):
        new_data = {"title": "New title"}
        response = self.client.post(self.url, data=new_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.quiz.refresh_from_db()
        self.assertEqual(self.quiz.title, new_data['title'])
        self.assertEqual(list(self.quiz.question_bim.all()), [])
        self.assertRedirects(response, reverse("quiz_bim:quizbim_list"))

    def test_anonymous(self):
        new_data = {"title": "New title"}
        response = self.client.post(self.url, data=new_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_no_permissions(self):
        new_data = {"title": "New title"}
        self.client.force_login(self.user)
        response = self.client.post(self.url, data=new_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    @login_superuser
    def test_invalid_empty_title_field(self):
        invalid_data = {"title": ""}
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.quiz.refresh_from_db()
        self.assertEqual(self.quiz.title, None)

    @login_superuser
    def test_not_found(self):
        response = self.client.get(reverse("quiz_bim:quizbim_update", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class TestQuizBimDeleteView(CustomTestCase):

    def setUp(self) -> None:
        self.quiz = QuizBimFactory.create()
        self.url = reverse("quiz_bim:quizbim_delete", kwargs={"pk": self.quiz.pk})

    @login_superuser
    def test_delete_view(self):
        previous_count = QuizBim.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(previous_count - QuizBim.objects.count(), 1)
        self.assertRedirects(response, reverse("quiz_bim:quizbim_list"))

    def test_anonymous(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_no_permissions(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    @login_superuser
    def test_not_found(self):
        previous_count = QuizBim.objects.count()
        response = self.client.post(reverse("quiz_bim:quizbim_delete", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(previous_count, QuizBim.objects.count())
