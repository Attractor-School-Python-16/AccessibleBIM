from django.test import TestCase

from quiz_bim.forms.quiz_bim_form import QuizBimForm


class TestQuizBimForm(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.correct_form_data = {
            "title": "Quiz",
            "questions_qty": 5,
        }
        super().setUpClass()

    def test_quiz_form(self):
        form = QuizBimForm(data=self.correct_form_data)
        self.assertTrue(form.is_valid())

    def test_quiz_form_invalid(self):
        invalid_data = {
            "title": "",
            "questions_qty": "string",
        }
        form = QuizBimForm(data=invalid_data)
        self.assertFalse(form.is_valid())
