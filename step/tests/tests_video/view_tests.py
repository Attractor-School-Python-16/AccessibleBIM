from http import HTTPStatus

from django.urls import reverse

from quiz_bim.tests.utils import CustomTestCase, login_superuser, login_user
from step.models import VideoModel
from step.tests.factories import VideoFactory


class TestVideoListView(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("step:videomodel_list")
        super().setUpTestData()

    @login_superuser
    def test_list_view(self):
        response = self.client.get(reverse("step:videomodel_list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertQuerysetEqual(response.context['videos'], VideoModel.objects.all(), ordered=False)
        self.assertTemplateUsed(response, 'steps/video/video_list.html')
        self.assertFalse(response.context['is_paginated'])
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    @login_user
    def test_no_permissions(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestVideoDetailView(CustomTestCase):
    def setUp(self):
        self.video = VideoFactory.create()
        self.url = reverse("step:videomodel_detail", kwargs={"pk": self.video.pk})

    @login_superuser
    def test_video_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['video'], self.video)
        self.assertTemplateUsed(response, 'steps/video/video_detail.html')
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    @login_superuser
    def test_not_found(self):
        response = self.client.get(reverse("step:videomodel_detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    @login_user
    def test_no_permissions(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
