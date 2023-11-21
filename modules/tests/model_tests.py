from django.test import TestCase

from modules.tests.factories import ChapterFactory, CourseTargetFactory, CourseFactory, ModuleFactory, TeacherFactory


class TestModuleModel(TestCase):
    def test_module_factory_no_exception(self):
        try:
            module = ModuleFactory.create()
        except Exception:
            self.fail("Exception was raised")

    def test_module_factory(self):
        module = ModuleFactory.create(title="Module", description="Description")
        self.assertEqual(module.title, "Module")
        self.assertEqual(module.description, "Description")


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


class TestChapterModel(TestCase):
    def test_chapter_factory_no_exception(self):
        try:
            chapter = ChapterFactory.create()
        except Exception:
            self.fail("Exception was raised")

    def test_chapter_factory(self):
        course = CourseFactory.create()
        chapter = ChapterFactory.create(title="Chapter", description="Description", course=course)
        self.assertEqual(chapter.title, "Chapter")
        self.assertEqual(chapter.description, "Description")
        self.assertEqual(chapter.course, course)


class TestTeacherModel(TestCase):
    def test_teacher_factory_no_exception(self):
        try:
            teacher = TeacherFactory.create()
        except Exception:
            self.fail("Exception was raised")

    def test_teacher_factory(self):
        teacher = TeacherFactory.create(first_name="First", last_name="Last", father_name="Father name",
                                        job_title="Job", corp="Corp", experience="Experience", description="Description")
        self.assertEqual(teacher.first_name, "First")
        self.assertEqual(teacher.last_name, "Last")
        self.assertEqual(teacher.father_name, "Father name")
        self.assertEqual(teacher.job_title, "Job")
        self.assertEqual(teacher.corp, "Corp")
        self.assertEqual(teacher.description, "Description")
