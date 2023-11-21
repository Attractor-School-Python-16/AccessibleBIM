from django.test import TestCase

from quiz_bim.tests.factories import QuizBimFactory


class TestQuizBimModel(TestCase):
    def test_quiz_factory_no_exception(self):
        try:
            quiz = QuizBimFactory.create()
        except ValueError:
            self.fail("ValueError exception was raised")

    def test_quiz_factory(self):
        quiz = QuizBimFactory.create(title="Quiz", questions_qty=5)
        self.assertEqual(quiz.questions_qty, 5)
        self.assertEqual(quiz.title, "Quiz")
