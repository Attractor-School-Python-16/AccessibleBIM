from django.test import TestCase

from quiz_bim.forms.question_bim_form import QuestionBimForm
from quiz_bim.tests.factories import QuizBimFactory


class TestQuestionBimForm(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.correct_form_data = {
            "title": "Question",
            "test_bim": QuizBimFactory.create()
        }
        super().setUpClass()

    def test_question_form(self):
        form = QuestionBimForm(data=self.correct_form_data)
        self.assertTrue(form.is_valid())

    def test_question_form_invalid(self):
        invalid_data = {
            "title": "",
            "test_bim": "string"
        }
        form = QuestionBimForm(data=invalid_data)
        self.assertFalse(form.is_valid())
