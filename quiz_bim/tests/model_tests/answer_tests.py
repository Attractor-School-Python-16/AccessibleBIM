from django.test import TestCase

from quiz_bim.tests.factories import AnswerBimFactory, QuestionBimFactory, QuizBimFactory


class TestAnswerBimModel(TestCase):
    def test_quiz_factory_no_exception(self):
        try:
            answer = AnswerBimFactory.create()
        except ValueError:
            self.fail("ValueError exception was raised")

    def test_quiz_factory(self):
        quiz = QuizBimFactory.create()
        question = QuestionBimFactory.create(test_bim=quiz)
        answer = AnswerBimFactory.create(answer="Answer", is_correct=True, question_bim=question)
        self.assertEqual(answer.answer, "Answer")
        self.assertEqual(answer.is_correct, True)
        self.assertEqual(answer.question_bim, question)
        self.assertEqual(answer.question_bim.test_bim, quiz)
