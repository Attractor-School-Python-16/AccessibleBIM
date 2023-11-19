import factory
from factory.django import DjangoModelFactory


class SubscriptionFactory(DjangoModelFactory):
    class Meta:
        model = 'subscription.SubscriptionModel'

    course = factory.SubFactory('modules.tests.factories.CourseFactory')
    price = factory.Faker('random_int', min=100, max=1000)
    is_published = factory.Faker('boolean')
