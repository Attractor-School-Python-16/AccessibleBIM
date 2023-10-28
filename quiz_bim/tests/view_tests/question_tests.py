from http import HTTPStatus

from django.urls import reverse

from quiz_bim.models import QuestionBim
from quiz_bim.tests.factories import QuestionBimFactory, QuizBimFactory
from quiz_bim.tests.utils import login_superuser, CustomTestCase


class TestQuestionBimDetailView(CustomTestCase):

    @login_superuser
    def test_detail_view(self):
        question = QuestionBimFactory.create()
        response = self.client.get(
            reverse("quiz_bim:questionbim_htmx_detail", kwargs={"tpk": question.test_bim.pk, "qpk": question.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['question'], question)
        self.assertTemplateUsed(response, 'quiz_bim/question_bim/question_bim_detail.html')
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_anonymous(self):
        question = QuestionBimFactory.create()
        response = self.client.get(
            reverse("quiz_bim:questionbim_htmx_detail", kwargs={"tpk": question.test_bim.pk, "qpk": question.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_no_permissions(self):
        self.client.force_login(self.user)
        question = QuestionBimFactory.create()
        response = self.client.get(
            reverse("quiz_bim:questionbim_htmx_detail", kwargs={"tpk": question.test_bim.pk, "qpk": question.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    @login_superuser
    def test_not_found(self):
        response = self.client.get(reverse("quiz_bim:questionbim_htmx_detail", kwargs={"tpk": 999, "qpk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class TestQuestionBimCreateView(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.correct_form_data = {
            "title": "Question"
        }
        quiz = QuizBimFactory.create()
        cls.url = reverse("quiz_bim:questionbim_htmx_create", kwargs={"tpk": quiz.pk})
        super().setUpTestData()

    @login_superuser
    def test_create_view(self):
        previous_count = QuestionBim.objects.count()
        response = self.client.post(self.url, data=self.correct_form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(QuestionBim.objects.count() - previous_count, 1)
        question = QuestionBim.objects.latest('create_at')
        self.assertRedirects(response, reverse("quiz_bim:quizbim_detail", kwargs={"tpk": question.test_bim.pk}))

    def test_anonymous(self):
        response = self.client.post(self.url, data=self.correct_form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_no_permissions(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, data=self.correct_form_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    @login_superuser
    def test_invalid_data(self):
        invalid_data = {
            "title": ""
        }
        previous_count = QuestionBim.objects.count()
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(previous_count, QuestionBim.objects.count())


class TestQuestionBimUpdateView(CustomTestCase):
    question = None

    def setUp(self) -> None:
        self.question = QuestionBimFactory.create()
        self.url = reverse("quiz_bim:questionbim_htmx_update",
                           kwargs={"tpk": self.question.test_bim.pk, "qpk": self.question.pk})

    @login_superuser
    def test_update_view(self):
        new_data = {
            "title": "New title"
        }
        response = self.client.post(self.url, data=new_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.question.refresh_from_db()
        self.assertEqual(self.question.title, "New title")
        # self.assertRedirects(response, reverse("quiz_bim:tests_list"))

    def test_anonymous(self):
        new_data = {
            "title": "New title"
        }
        response = self.client.post(self.url, data=new_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_no_permissions(self):
        self.client.force_login(self.user)
        new_data = {
            "title": "New title"
        }
        response = self.client.post(self.url, data=new_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    @login_superuser
    def test_invalid_data(self):
        invalid_data = {
            "title": ""
        }
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @login_superuser
    def test_not_found(self):
        response = self.client.get(reverse("quiz_bim:questionbim_htmx_update", kwargs={"tpk": 999, "qpk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class TestQuestionBimDeleteView(CustomTestCase):

    def setUp(self) -> None:
        self.question = QuestionBimFactory.create()
        self.url = reverse("quiz_bim:questionbim_htmx_delete",
                           kwargs={"tpk": self.question.test_bim.pk, "qpk": self.question.pk})

    @login_superuser
    def test_delete_view(self):
        previous_count = QuestionBim.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(previous_count - QuestionBim.objects.count(), 1)
        # self.assertRedirects(response, reverse("quiz_bim:tests_list"))

    def test_anonymous(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_no_permissions(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    @login_superuser
    def test_not_found(self):
        previous_count = QuestionBim.objects.count()
        response = self.client.post(reverse("quiz_bim:questionbim_htmx_delete", kwargs={"tpk": 999, "qpk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(previous_count, QuestionBim.objects.count())
