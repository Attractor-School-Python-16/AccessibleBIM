import factory
from factory.django import DjangoModelFactory


class AnswerBimFactory(DjangoModelFactory):
    class Meta:
        model = 'quiz_bim.AnswerBim'

    answer = factory.Sequence(lambda n: f"Answer {n}")
    is_correct = factory.Faker('boolean')
    question_bim = factory.SubFactory('quiz_bim.tests.factories.QuestionBimFactory')
