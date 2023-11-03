from http import HTTPStatus

from django.urls import reverse

from modules.models import ChapterModel
from modules.tests import ChapterFactory, CourseFactory
from quiz_bim.tests.utils import CustomTestCase, login_superuser, login_user


class TestChapterDetailView(CustomTestCase):

    def setUp(self):
        self.chapter = ChapterFactory.create()
        self.url = reverse("modules:chaptermodel_detail", kwargs={"pk": self.chapter.pk})

    @login_superuser
    def test_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['chapter'], self.chapter)
        self.assertTemplateUsed(response, 'chapters/chapter_detail.html')
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    @login_user
    def test_no_permissions(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    @login_superuser
    def test_not_found(self):
        response = self.client.get(reverse("modules:chaptermodel_detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class TestChapterCreateView(CustomTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.course = CourseFactory.create()
        cls.correct_data = {
            "title": "Chapter",
            "description": "Chapter description"
        }
        cls.url = f'{reverse("modules:chaptermodel_create")}?course_pk={cls.course.id}'
        super().setUpTestData()

    @login_superuser
    def test_create_view(self):
        previous_count = ChapterModel.objects.count()
        response = self.client.post(self.url, data=self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(ChapterModel.objects.count() - previous_count, 1)
        chapter = ChapterModel.objects.latest('create_at')
        self.assertEqual(chapter.title, self.correct_data['title'])
        self.assertEqual(chapter.description, self.correct_data['description'])
        self.assertRedirects(response, reverse("modules:coursemodel_detail", kwargs={"pk": chapter.course.pk}))

    def test_anonymous(self):
        response = self.client.post(self.url, data=self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    @login_user
    def test_no_permissions(self):
        response = self.client.post(self.url, data=self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    @login_superuser
    def test_empty_title(self):
        invalid_data = {
            "title": "",
            "description": "Chapter description"
        }
        previous_count = ChapterModel.objects.count()
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(ChapterModel.objects.count() - previous_count, 0)
        self.assertFormError(response, 'form', 'title', 'Это поле обязательно для заполнения.')

    @login_superuser
    def test_empty_description(self):
        invalid_data = {
            "title": "Chapter",
            "description": ""
        }
        previous_count = ChapterModel.objects.count()
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(ChapterModel.objects.count() - previous_count, 0)
        self.assertFormError(response, 'form', 'description', 'Это поле обязательно для заполнения.')
