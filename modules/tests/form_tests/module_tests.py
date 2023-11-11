from django.test import TestCase

from modules.forms.modules_form import ModulesForm
from quiz_bim.tests.utils import get_image_file


class TestModuleForm(TestCase):
    def test_module_form(self):
        correct_data = {
            "title": "Module",
            "description": "Description"
        }
        files = {"image": get_image_file()}
        form = ModulesForm(correct_data, files)
        self.assertTrue(form.is_valid())

    def test_empty_title(self):
        invalid_data = {
            "title": "",
            "description": "Description"
        }
        files = {"image": get_image_file()}
        form = ModulesForm(invalid_data, files)
        self.assertFalse(form.is_valid())

    def test_empty_description(self):
        invalid_data = {
            "title": "Module",
            "description": ""
        }
        files = {"image": get_image_file()}
        form = ModulesForm(invalid_data, files)
        self.assertFalse(form.is_valid())

    def test_no_image(self):
        correct_data = {
            "title": "Module",
            "description": "Description"
        }
        form = ModulesForm(correct_data)
        self.assertFalse(form.is_valid())
