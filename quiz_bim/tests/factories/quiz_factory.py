import factory
from factory.django import DjangoModelFactory


class QuizBimFactory(DjangoModelFactory):
    class Meta:
        model = 'quiz_bim.QuizBim'

    title = factory.Sequence(lambda n: f"Quiz {n}")
    questions_qty = factory.Faker('random_int', min=0, max=1000, step=1)
