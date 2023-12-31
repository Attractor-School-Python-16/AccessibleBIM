from http import HTTPStatus

from django.urls import reverse

from quiz_bim.models import QuestionBim
from quiz_bim.tests.factories import QuestionBimFactory, QuizBimFactory
from quiz_bim.tests.utils import login_superuser, CustomTestCase, login_user


class TestQuestionBimDetailView(CustomTestCase):
    def setUp(self):
        self.question = QuestionBimFactory.create()
        self.url = reverse("quiz_bim:questionbim_htmx_detail", kwargs={"tpk": self.question.test_bim.pk, "qpk": self.question.pk})

    @login_superuser
    def test_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['question'], self.question)
        self.assertTemplateUsed(response, 'quiz_bim/question_bim/question_bim_detail.html')
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    @login_user
    def test_no_permissions(self):
        response = self.client.get(self.url)
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
        cls.url = reverse("quiz_bim:quizbim_detail", kwargs={"pk": quiz.pk})
        super().setUpTestData()

    @login_superuser
    def test_get_form(self):
        url = reverse("quiz_bim:questionbim_htmx_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @login_superuser
    def test_create_view(self):
        previous_count = QuestionBim.objects.count()
        response = self.client.post(self.url, data=self.correct_form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(QuestionBim.objects.count() - previous_count, 1)
        question = QuestionBim.objects.latest('create_at')
        self.assertEqual(question.title, self.correct_form_data['title'])
        self.assertRedirects(response, reverse("quiz_bim:questionbim_htmx_detail", kwargs={"tpk": question.test_bim.pk, "qpk": question.pk}))
        self.assertEqual(question.title, self.correct_form_data['title'])

    def test_anonymous(self):
        previous_count = QuestionBim.objects.count()
        response = self.client.post(self.url, data=self.correct_form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(QuestionBim.objects.count() - previous_count, 0)

    @login_user
    def test_no_permissions(self):
        previous_count = QuestionBim.objects.count()
        response = self.client.post(self.url, data=self.correct_form_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(QuestionBim.objects.count() - previous_count, 0)

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
        self.assertEqual(self.question.title, new_data['title'])

    def test_anonymous(self):
        new_data = {
            "title": "New title"
        }
        response = self.client.post(self.url, data=new_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.question.refresh_from_db()
        self.assertNotEqual(self.question.title, new_data['title'])

    @login_user
    def test_no_permissions(self):
        new_data = {
            "title": "New title"
        }
        response = self.client.post(self.url, data=new_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.question.refresh_from_db()
        self.assertNotEqual(self.question.title, new_data['title'])

    @login_superuser
    def test_invalid_data(self):
        invalid_data = {
            "title": ""
        }
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.question.refresh_from_db()
        self.assertNotEqual(self.question.title, invalid_data['title'])

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
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(previous_count - QuestionBim.objects.count(), 1)

    def test_anonymous(self):
        previous_count = QuestionBim.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(previous_count, QuestionBim.objects.count())

    @login_user
    def test_no_permissions(self):
        previous_count = QuestionBim.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(previous_count, QuestionBim.objects.count())

    @login_superuser
    def test_not_found(self):
        previous_count = QuestionBim.objects.count()
        response = self.client.post(reverse("quiz_bim:questionbim_htmx_delete", kwargs={"tpk": 999, "qpk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(previous_count, QuestionBim.objects.count())
