import factory
from factory.django import DjangoModelFactory


class QuestionBimFactory(DjangoModelFactory):
    class Meta:
        model = 'quiz_bim.QuestionBim'

    title = factory.Sequence(lambda n: f"Question {n}")
    test_bim = factory.SubFactory('quiz_bim.tests.factories.QuizBimFactory')
