from django.test import TestCase

from quiz_bim.tests.utils import get_txt_file
from step.forms.file_form import FileForm


class TestFileForm(TestCase):
    def test_file_form(self):
        correct_data = {
            "file_title": "File"
        }
        files = {"lesson_file": get_txt_file()}
        form = FileForm(correct_data, files)
        self.assertTrue(form.is_valid())

    def test_empty_title(self):
        invalid_data = {
            "file_title": ""
        }
        files = {"lesson_file": get_txt_file()}
        form = FileForm(invalid_data, files)
        self.assertFalse(form.is_valid())

    def test_no_lesson_file(self):
        invalid_data = {
            "file_title": "File"
        }
        form = FileForm(invalid_data)
        self.assertFalse(form.is_valid())
