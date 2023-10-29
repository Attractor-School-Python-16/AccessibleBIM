from unittest import TestCase

from modules.tests.factories import ChapterFactory, CourseFactory


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
