from unittest import TestCase

from modules.tests.factories import CourseFactory, ModuleFactory, CourseTargetFactory


class TestCourseModel(TestCase):
    def test_course_factory_no_exception(self):
        try:
            course = CourseFactory.create()
        except Exception:
            self.fail("Exception was raised")

    def test_course_factory(self):
        module = ModuleFactory.create()
        target = CourseTargetFactory.create()
        course = CourseFactory.create(title="Course", description="Description", module_id=module,
                                      courseTarget_id=target, language="RU", learnTime=10)
        self.assertEqual(course.title, "Course")
        self.assertEqual(course.description, "Description")
        self.assertEqual(course.language, "RU")
        self.assertEqual(course.learnTime, 10)
        self.assertEqual(course.module_id.id, module.id)
        self.assertEqual(course.courseTarget_id.id, target.id)
