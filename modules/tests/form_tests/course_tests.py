from django.test import TestCase

from modules.forms.courses_form import CoursesByModuleForm, CoursesStandAloneForm
from modules.tests.factories import CourseTargetFactory, TeacherFactory, ModuleFactory
from quiz_bim.tests.utils import get_image_file


class TestCourseByModuleForm(TestCase):
    def test_course_form(self):
        correct_data = {
            "title": "Course",
            "description": "Description",
            "learnTime": 10,
            "courseTarget_id": CourseTargetFactory.create(),
            "language": "RU",
            "teachers": [TeacherFactory.create()]
        }
        files = {"image": get_image_file()}
        form = CoursesByModuleForm(correct_data, files)
        self.assertTrue(form.is_valid())

    def test_empty_title(self):
        invalid_data = {
            "title": "",
            "description": "Description",
            "learnTime": 10,
            "courseTarget_id": CourseTargetFactory.create(),
            "language": "RU",
            "teachers": [TeacherFactory.create()]
        }
        files = {"image": get_image_file()}
        form = CoursesByModuleForm(invalid_data, files)
        self.assertFalse(form.is_valid())

    def test_empty_description(self):
        invalid_data = {
            "title": "Course",
            "description": "",
            "learnTime": 10,
            "courseTarget_id": CourseTargetFactory.create(),
            "language": "RU",
            "teachers": [TeacherFactory.create()]
        }
        files = {"image": get_image_file()}
        form = CoursesByModuleForm(invalid_data, files)
        self.assertFalse(form.is_valid())

    def test_invalid_learnTime(self):
        invalid_data = {
            "title": "Course",
            "description": "Description",
            "learnTime": "",
            "courseTarget_id": CourseTargetFactory.create(),
            "language": "RU",
            "teachers": [TeacherFactory.create()]
        }
        files = {"image": get_image_file()}
        form = CoursesByModuleForm(invalid_data, files)
        self.assertFalse(form.is_valid())

    def test_invalid_courseTarget_id(self):
        invalid_data = {
            "title": "Course",
            "description": "Description",
            "learnTime": 10,
            "courseTarget_id": "",
            "language": "RU",
            "teachers": [TeacherFactory.create()]
        }
        files = {"image": get_image_file()}
        form = CoursesByModuleForm(invalid_data, files)
        self.assertFalse(form.is_valid())

    def test_invalid_language(self):
        invalid_data = {
            "title": "Course",
            "description": "Description",
            "learnTime": 10,
            "courseTarget_id": CourseTargetFactory.create(),
            "language": "",
            "teachers": [TeacherFactory.create()]
        }
        files = {"image": get_image_file()}
        form = CoursesByModuleForm(invalid_data, files)
        self.assertFalse(form.is_valid())

    def test_no_teachers(self):
        invalid_data = {
            "title": "Course",
            "description": "Description",
            "learnTime": 10,
            "courseTarget_id": CourseTargetFactory.create(),
            "language": "RU",
            "teachers": []
        }
        files = {"image": get_image_file()}
        form = CoursesByModuleForm(invalid_data, files)
        self.assertFalse(form.is_valid())


class TestCourseStandAloneForm(TestCase):
    def test_course_form(self):
        correct_data = {
            "module_id": ModuleFactory.create(),
            "title": "Course",
            "description": "Description",
            "learnTime": 10,
            "courseTarget_id": CourseTargetFactory.create(),
            "language": "RU",
            "teachers": [TeacherFactory.create()]
        }
        files = {"image": get_image_file()}
        form = CoursesStandAloneForm(correct_data, files)
        self.assertTrue(form.is_valid())

    def test_invalid_module_id(self):
        invalid_data = {
            "module_id": "",
            "title": "Course",
            "description": "Description",
            "learnTime": 10,
            "courseTarget_id": CourseTargetFactory.create(),
            "language": "RU",
            "teachers": [TeacherFactory.create()]
        }
        files = {"image": get_image_file()}
        form = CoursesStandAloneForm(invalid_data, files)
        self.assertFalse(form.is_valid())

    def test_empty_title(self):
        invalid_data = {
            "module_id": ModuleFactory.create(),
            "title": "",
            "description": "Description",
            "learnTime": 10,
            "courseTarget_id": CourseTargetFactory.create(),
            "language": "RU",
            "teachers": [TeacherFactory.create()]
        }
        files = {"image": get_image_file()}
        form = CoursesStandAloneForm(invalid_data, files)
        self.assertFalse(form.is_valid())

    def test_empty_description(self):
        invalid_data = {
            "module_id": ModuleFactory.create(),
            "title": "Course",
            "description": "",
            "learnTime": 10,
            "courseTarget_id": CourseTargetFactory.create(),
            "language": "RU",
            "teachers": [TeacherFactory.create()]
        }
        files = {"image": get_image_file()}
        form = CoursesStandAloneForm(invalid_data, files)
        self.assertFalse(form.is_valid())

    def test_invalid_learnTime(self):
        invalid_data = {
            "module_id": ModuleFactory.create(),
            "title": "Course",
            "description": "Description",
            "learnTime": "",
            "courseTarget_id": CourseTargetFactory.create(),
            "language": "RU",
            "teachers": [TeacherFactory.create()]
        }
        files = {"image": get_image_file()}
        form = CoursesStandAloneForm(invalid_data, files)
        self.assertFalse(form.is_valid())

    def test_invalid_courseTarget_id(self):
        invalid_data = {
            "module_id": ModuleFactory.create(),
            "title": "Course",
            "description": "Description",
            "learnTime": 10,
            "courseTarget_id": "",
            "language": "RU",
            "teachers": [TeacherFactory.create()]
        }
        files = {"image": get_image_file()}
        form = CoursesStandAloneForm(invalid_data, files)
        self.assertFalse(form.is_valid())

    def test_invalid_language(self):
        invalid_data = {
            "module_id": ModuleFactory.create(),
            "title": "Course",
            "description": "Description",
            "learnTime": 10,
            "courseTarget_id": CourseTargetFactory.create(),
            "language": "",
            "teachers": [TeacherFactory.create()]
        }
        files = {"image": get_image_file()}
        form = CoursesStandAloneForm(invalid_data, files)
        self.assertFalse(form.is_valid())

    def test_no_teachers(self):
        invalid_data = {
            "module_id": ModuleFactory.create(),
            "title": "Course",
            "description": "Description",
            "learnTime": 10,
            "courseTarget_id": CourseTargetFactory.create(),
            "language": "RU",
            "teachers": []
        }
        files = {"image": get_image_file()}
        form = CoursesStandAloneForm(invalid_data, files)
        self.assertFalse(form.is_valid())
