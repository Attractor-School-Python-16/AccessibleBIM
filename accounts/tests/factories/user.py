import factory
from factory.django import DjangoModelFactory

from accounts.models import CustomUser


class UserFactory(DjangoModelFactory):
    first_name = factory.Sequence(lambda t: f"user{t}")
    last_name = factory.Sequence(lambda t: f"user{t}")
    father_name = ""
    email = factory.Sequence(lambda t: f"user{t}@bimtest.com")
    # password = '123'
    country = 'KG'
    phone_number = '+996555555555'
    job_title = ''
    company = ''
    type_corp = '7'

    class Meta:
        model = CustomUser
