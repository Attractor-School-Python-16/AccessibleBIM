from django.test import TestCase
from django.urls import reverse

from step.tests.factories import FileModelFactory


class TestFileModel(TestCase):
    def test_file_factory_no_exception(self):
        try:
            file = FileModelFactory.create()
        except Exception:
            self.fail("Exception was raised")

    def test_file_factory(self):
        file = FileModelFactory.create(file_title="File")
        self.assertEqual(file.file_title, "File")

    def test_file_functions(self):
        file = FileModelFactory.create(file_title="File")
        self.assertEqual(str(file), f'Файл {file.id} File')
        self.assertEqual(file.get_absolute_url(), reverse('step:filemodel_list'))
