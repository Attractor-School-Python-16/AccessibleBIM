from unittest import TestCase

from modules.tests.factories import CourseTargetFactory


class TestCourseTargetModel(TestCase):
    def test_course_target_factory_no_exception(self):
        try:
            course_target = CourseTargetFactory.create()
        except Exception:
            self.fail("Exception was raised")

    def test_course_target_factory(self):
        course_target = CourseTargetFactory.create(title="Target", description="Description")
        self.assertEqual(course_target.title, "Target")
        self.assertEqual(course_target.description, "Description")