from django.test import TestCase

from quiz_bim.forms.quiz_bim_form import QuizBimForm


class TestQuizBimForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.correct_form_data = {"title": "Quiz"}
        super().setUpTestData()

    def test_quiz_form(self):
        form = QuizBimForm(data=self.correct_form_data)
        self.assertTrue(form.is_valid())

    # def test_invalid_title_field(self):
    #     invalid_data = {"title": ""}
    #     form = QuizBimForm(data=invalid_data)
    #     self.assertFalse(form.is_valid())
