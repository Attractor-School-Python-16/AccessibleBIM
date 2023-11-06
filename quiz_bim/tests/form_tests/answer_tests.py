from django.test import TestCase

from quiz_bim.forms.answer_bim_form import AnswerBimForm
from quiz_bim.tests.factories import QuestionBimFactory


class TestAnswerBimForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.correct_form_data = {
            "answer": "Answer",
            "is_correct": True,
            "question_bim": QuestionBimFactory.create()
        }
        super().setUpTestData()

    def test_answer_form(self):
        form = AnswerBimForm(data=self.correct_form_data)
        self.assertTrue(form.is_valid())

    def test_answer_form_invalid(self):
        invalid_data = {
            "answer": "",
            "is_correct": None,
            "question_bim": "string"
        }
        form = AnswerBimForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_invalid_answer_field(self):
        invalid_data = {
            "answer": "",
            "is_correct": True,
            "question_bim": QuestionBimFactory.create()
        }
        form = AnswerBimForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_invalid_is_correct_field(self):
        invalid_data = {
            "answer": "Answer",
            "is_correct": None,
            "question_bim": QuestionBimFactory.create()
        }
        form = AnswerBimForm(data=invalid_data)
        self.assertFalse(form.is_valid())
