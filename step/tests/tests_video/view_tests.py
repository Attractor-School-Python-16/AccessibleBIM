from http import HTTPStatus

from django.urls import reverse
from django.utils.translation import gettext_lazy as _


from quiz_bim.tests.utils import CustomTestCase, login_superuser, login_user, get_video_file
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


class TestVideoCreateView(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.correct_data = {
            "video_title": "Test video",
            "video_description": "Test video description",
            "video_file": get_video_file()
        }
        cls.url = reverse("step:videomodel_create")
        super().setUpTestData()

    @login_superuser
    def test_video_create_view(self):
        previous_count = VideoModel.objects.count()
        response = self.client.post(self.url, self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(VideoModel.objects.count() - previous_count, 1)
        video = VideoModel.objects.latest('create_at')
        self.assertRedirects(response, reverse("step:videomodel_list"))
        self.assertEqual(video.video_title, self.correct_data['video_title'])
        self.assertEqual(video.video_description, self.correct_data['video_description'])

    def test_anonymous(self):
        previous_count = VideoModel.objects.count()
        response = self.client.post(self.url, self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(VideoModel.objects.count() - previous_count, 0)

    @login_user
    def test_no_permissions(self):
        previous_count = VideoModel.objects.count()
        response = self.client.post(self.url, self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(VideoModel.objects.count() - previous_count, 0)

    @login_superuser
    def test_empty_title(self):
        invalid_data = {
            "video_title": "",
            "video_description": "Test video description",
            "video_file": get_video_file()
        }
        previous_count = VideoModel.objects.count()
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response.context['form'], field="video_title", errors=[_('Please enter video title')])
        self.assertEqual(VideoModel.objects.count() - previous_count, 0)

    @login_superuser
    def test_empty_description(self):
        correct_data = {
            "video_title": "Test video",
            "video_description": "",
            "video_file": get_video_file()
        }
        previous_count = VideoModel.objects.count()
        response = self.client.post(self.url, correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(VideoModel.objects.count() - previous_count, 1)
        video = VideoModel.objects.latest('create_at')
        self.assertIsNone(video.video_description)

    @login_superuser
    def test_no_file(self):
        invalid_data = {
            "video_title": "Test video",
            "video_description": "Test video description",
        }
        previous_count = VideoModel.objects.count()
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response.context['form'], field="video_file", errors=[_('Please upload video file')])
        self.assertEqual(VideoModel.objects.count() - previous_count, 0)


class TestVideoUpdateView(CustomTestCase):
    def setUp(self):
        self.video = VideoFactory.create()
        self.url = reverse("step:videomodel_update", kwargs={"pk": self.video.pk})

    @login_superuser
    def test_video_update_view(self):
        correct_data = {
            "video_title": "New title",
            "video_description": "New description",
            "video_file": get_video_file()
        }
        response = self.client.post(self.url, correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.video.refresh_from_db()
        self.assertEqual(self.video.video_title, correct_data['video_title'])
        self.assertEqual(self.video.video_description, correct_data['video_description'])
        self.assertRedirects(response, reverse("step:videomodel_list"))

    def test_anonymous(self):
        correct_data = {
            "video_title": "New title",
            "video_description": "New description",
            "video_file": get_video_file()
        }
        response = self.client.post(self.url, correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.video.refresh_from_db()
        self.assertNotEqual(self.video.video_title, correct_data['video_title'])
        self.assertNotEqual(self.video.video_description, correct_data['video_description'])

    @login_user
    def test_no_permissions(self):
        correct_data = {
            "video_title": "New title",
            "video_description": "New description",
            "video_file": get_video_file()
        }
        response = self.client.post(self.url, correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.video.refresh_from_db()
        self.assertNotEqual(self.video.video_title, correct_data['video_title'])
        self.assertNotEqual(self.video.video_description, correct_data['video_description'])

    @login_superuser
    def test_not_found(self):
        correct_data = {
            "video_title": "New title",
            "video_description": "New description",
            "video_file": get_video_file()
        }
        response = self.client.post(reverse("step:videomodel_update", kwargs={"pk": 999}), correct_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    @login_superuser
    def test_empty_title(self):
        invalid_data = {
            "video_title": "",
            "video_description": "New description",
            "video_file": get_video_file()
        }
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response.context['form'], field="video_title", errors=[_('Please enter video title')])
        self.video.refresh_from_db()
        self.assertNotEqual(self.video.video_title, invalid_data['video_title'])

    @login_superuser
    def test_empty_description(self):
        correct_data = {
            "video_title": "New title",
            "video_description": "",
            "video_file": get_video_file()
        }
        response = self.client.post(self.url, correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.video.refresh_from_db()
        self.assertEqual(self.video.video_title, correct_data['video_title'])
        self.assertIsNone(self.video.video_description)

    @login_superuser
    def test_no_file(self):
        correct_data = {
            "video_title": "New title",
            "video_description": "New description",
        }
        response = self.client.post(self.url, correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.video.refresh_from_db()
        self.assertEqual(self.video.video_title, correct_data['video_title'])
        self.assertEqual(self.video.video_description, correct_data['video_description'])
