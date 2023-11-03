from http import HTTPStatus

from django.urls import reverse

from quiz_bim.models import AnswerBim
from quiz_bim.tests.factories import QuestionBimFactory, AnswerBimFactory
from quiz_bim.tests.utils import login_superuser, CustomTestCase, login_user


class TestAnswerBimCreateView(CustomTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.correct_form_data = {
            "answer": "Answer",
            "is_correct": True
        }
        cls.question = QuestionBimFactory.create()
        cls.url = reverse("quiz_bim:quizbim_detail", kwargs={"pk": cls.question.test_bim.pk}) + f"?question_pk={cls.question.pk}"
        super().setUpTestData()

    @login_superuser
    def test_get_form(self):
        url = reverse("quiz_bim:answerbim_htmx_create", kwargs={"pk": self.question.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @login_superuser
    def test_create_view(self):
        previous_count = AnswerBim.objects.count()
        response = self.client.post(self.url, data=self.correct_form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(AnswerBim.objects.count() - previous_count, 1)
        answer = AnswerBim.objects.latest('create_at')
        self.assertRedirects(response, reverse("quiz_bim:answerbim_htmx_detail", kwargs={"qpk": answer.question_bim.pk, "apk": answer.pk}))
        self.assertEqual(answer.answer, self.correct_form_data['answer'])
        self.assertEqual(answer.is_correct, self.correct_form_data['is_correct'])

    def test_anonymous(self):
        previous_count = AnswerBim.objects.count()
        response = self.client.post(self.url, data=self.correct_form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(AnswerBim.objects.count() - previous_count, 0)

    @login_user
    def test_no_permissions(self):
        previous_count = AnswerBim.objects.count()
        response = self.client.post(self.url, data=self.correct_form_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(AnswerBim.objects.count() - previous_count, 0)

    @login_superuser
    def test_invalid_data(self):
        invalid_data = {
            "answer": "",
            "is_correct": "string"
        }
        previous_count = AnswerBim.objects.count()
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(previous_count, AnswerBim.objects.count())


class TestAnswerBimUpdateView(CustomTestCase):

    def setUp(self) -> None:
        self.answer = AnswerBimFactory.create()
        self.url = reverse("quiz_bim:answerbim_htmx_update", kwargs={"qpk": self.answer.question_bim.pk, "apk": self.answer.pk})

    @login_superuser
    def test_update_view(self):
        new_data = {
            "answer": "New title",
            "is_correct": False
        }
        response = self.client.post(self.url, data=new_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.answer.refresh_from_db()
        self.assertEqual(self.answer.answer, new_data['answer'])
        self.assertEqual(self.answer.is_correct, new_data['is_correct'])

    def test_anonymous(self):
        new_data = {
            "answer": "New title",
            "is_correct": False
        }
        response = self.client.post(self.url, data=new_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.answer.refresh_from_db()
        self.assertNotEqual(self.answer.answer, new_data['answer'])

    @login_user
    def test_no_permissions(self):
        new_data = {
            "answer": "New title",
            "is_correct": False
        }
        response = self.client.post(self.url, data=new_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.answer.refresh_from_db()
        self.assertNotEqual(self.answer.answer, new_data['answer'])

    @login_superuser
    def test_invalid_data(self):
        invalid_data = {
            "answer": "",
            "is_correct": "string"
        }
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.answer.refresh_from_db()
        self.assertNotEqual(self.answer.answer, invalid_data['answer'])
        self.assertNotEqual(self.answer.is_correct, invalid_data['is_correct'])

    @login_superuser
    def test_not_found(self):
        response = self.client.get(reverse("quiz_bim:answerbim_htmx_update", kwargs={"qpk": 999, "apk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class TestAnswerBimDeleteView(CustomTestCase):

    def setUp(self) -> None:
        self.answer = AnswerBimFactory.create()
        self.url = reverse("quiz_bim:answerbim_htmx_delete", kwargs={"qpk": self.answer.question_bim.pk, "apk": self.answer.pk})

    @login_superuser
    def test_delete_view(self):
        previous_count = AnswerBim.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(previous_count - AnswerBim.objects.count(), 1)

    def test_anonymous(self):
        previous_count = AnswerBim.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(previous_count, AnswerBim.objects.count())

    @login_user
    def test_no_permissions(self):
        previous_count = AnswerBim.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(previous_count, AnswerBim.objects.count())

    @login_superuser
    def test_not_found(self):
        previous_count = AnswerBim.objects.count()
        response = self.client.post(reverse("quiz_bim:answerbim_htmx_delete", kwargs={"qpk": 999, "apk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(previous_count, AnswerBim.objects.count())
