from functools import wraps
from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files import File
from django.test import TestCase


class CustomTestCase(TestCase):
    """
    Такой же, как и обычный TestCase от Django.
    Но в него встроен объект суперпользователя, и обычного пользователя.
    """

    user = None
    superuser = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(email="test@test.com", password="test")
        cls.superuser = get_user_model().objects.create_superuser(email="admin@admin.com", password="admin")
        super().setUpTestData()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.superuser.delete()
        super().tearDownClass()


def login_superuser(test_func):
    """
    Декоратор для функций тестов, который логинит объект клиента как суперпользователя (если он есть)
    """

    @wraps(test_func)
    def wrapper(self, *args, **kwargs):
        # Log the client in
        self.client.force_login(self.superuser)

        try:
            # Execute the test function
            test_func(self, *args, **kwargs)
        finally:
            # Log the client out
            self.client.logout()

    return wrapper


def get_image_file(name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
    file_obj = BytesIO()
    image = Image.new("RGB", size=size, color=color)
    image.save(file_obj, ext)
    file_obj.seek(0)
    return File(file_obj, name=name)
