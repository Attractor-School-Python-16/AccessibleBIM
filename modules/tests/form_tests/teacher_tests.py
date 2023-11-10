from django.test import TestCase

from modules.forms.teachers_form import TeacherForm


class TestTeacherForm(TestCase):

    def test_teacher_form(self):
        correct_data = {
            "first_name": "Иван",
            "last_name": "Иванов",
            "father_name": "Иванович",
            "job_title": "Преподаватель",
            "corp": "Корпорация",
            "experience": "10 лет",
            "description": "О себе"
        }
        form = TeacherForm(correct_data)
        self.assertTrue(form.is_valid())

    def test_null_fields(self):
        invalid_data = {
            "first_name": "Иван",
            "last_name": "Иванов",
            "father_name": "",
            "job_title": "",
            "corp": "",
            "experience": "",
            "description": ""
        }
        form = TeacherForm(invalid_data)
        self.assertTrue(form.is_valid())

    def test_empty_first_name(self):
        invalid_data = {
            "first_name": "",
            "last_name": "Иванов",
            "father_name": "Иванович",
            "job_title": "Преподаватель",
            "corp": "Корпорация",
            "experience": "10 лет",
            "description": "О себе"
        }
        form = TeacherForm(invalid_data)
        self.assertFalse(form.is_valid())

    def test_empty_last_name(self):
        invalid_data = {
            "first_name": "Иван",
            "last_name": "",
            "father_name": "Иванович",
            "job_title": "Преподаватель",
            "corp": "Корпорация",
            "experience": "10 лет",
            "description": "О себе"
        }
        form = TeacherForm(invalid_data)
        self.assertFalse(form.is_valid())
