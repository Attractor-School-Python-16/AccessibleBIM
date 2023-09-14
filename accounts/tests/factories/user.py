import factory
from factory.django import DjangoModelFactory

from accounts.models import CustomUser


class UserFactory(DjangoModelFactory):
    first_name = factory.Sequence(lambda t: f"User{t}")
    last_name = factory.Sequence(lambda t: f"User{t}")
    email = factory.Sequence(lambda t: f"user{t}@bimtest.com")
    phone_number = '+996555555555'

    class Meta:
        model = CustomUser
