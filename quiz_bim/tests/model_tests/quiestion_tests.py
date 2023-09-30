from django.test import TestCase

from quiz_bim.tests.factories import QuestionBimFactory, QuizBimFactory


class TestQuestionBimModel(TestCase):
    def test_quiz_factory_no_exception(self):
        try:
            question = QuestionBimFactory.create()
        except ValueError:
            self.fail("ValueError exception was raised")

    def test_quiz_factory(self):
        quiz = QuizBimFactory.create()
        question = QuestionBimFactory.create(title="Question", test_bim=quiz)
        self.assertEqual(question.title, "Question")
        self.assertEqual(question.test_bim, quiz)
