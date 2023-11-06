from django.test import TestCase

from modules.forms.chapters_form import ChaptersForm


class TestChapterForm(TestCase):
    def test_chapter_form(self):
        correct_data = {
            "title": "Chapter",
            "description": "Description"
        }
        form = ChaptersForm(correct_data)
        self.assertTrue(form.is_valid())

    def test_empty_title(self):
        invalid_data = {
            "title": "",
            "description": "Description"
        }
        form = ChaptersForm(invalid_data)
        self.assertFalse(form.is_valid())

    def test_empty_description(self):
        invalid_data = {
            "title": "Chapter",
            "description": ""
        }
        form = ChaptersForm(invalid_data)
        self.assertFalse(form.is_valid())
