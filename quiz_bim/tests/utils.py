import base64
from functools import wraps
from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
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


def get_image_file():
    image_content = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAUA" + "AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO" + "9TXL0Y4OHwAAAABJRU5ErkJggg==")
    image = SimpleUploadedFile("image.jpg", image_content, content_type="image/jpeg")
    return image
