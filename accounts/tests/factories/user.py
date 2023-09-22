import factory
from factory.django import DjangoModelFactory

from accounts.models import CustomUser


class UserFactory(DjangoModelFactory):
    first_name = factory.Sequence(lambda t: f"User{t}")
    last_name = factory.Sequence(lambda t: f"User{t}")
    father_name = ""
    password1 = '123'
    password2 = '123'
    phone_number = '+996555555555'
    job_title = ''
    company = ''
    type_corp = '7'
    email = factory.Sequence(lambda t: f"user{t}@bimtest.com")
    captcha_0 = 'dummy-value'
    captcha_1 = 'PASSED'

    class Meta:
        model = CustomUser
