from django.test import TestCase

from modules.forms.course_target_form import CourseTargetForm


class TestCourseTargetForm(TestCase):
    def test_course_target_form(self):
        correct_data = {
            "title": "Target",
            "description": "Description"
        }
        form = CourseTargetForm(correct_data)
        self.assertTrue(form.is_valid())

    def test_empty_title(self):
        invalid_data = {
            "title": "",
            "description": "Description"
        }
        form = CourseTargetForm(invalid_data)
        self.assertFalse(form.is_valid())

    def test_empty_description(self):
        invalid_data = {
            "title": "Target",
            "description": ""
        }
        form = CourseTargetForm(invalid_data)
        self.assertTrue(form.is_valid())
