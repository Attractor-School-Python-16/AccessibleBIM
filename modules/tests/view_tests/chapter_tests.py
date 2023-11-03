from http import HTTPStatus

from django.urls import reverse

from modules.tests import ChapterFactory
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
