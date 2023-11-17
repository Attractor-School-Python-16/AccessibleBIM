from http import HTTPStatus

from django.urls import reverse

from quiz_bim.tests.utils import CustomTestCase, login_superuser, login_user
from step.models import FileModel


class TestFileListView(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("step:filemodel_list")
        super().setUpTestData()

    @login_superuser
    def test_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertQuerysetEqual(response.context['files'], FileModel.objects.all(), ordered=False)
        self.assertTemplateUsed(response, 'steps/file/file_list.html')
        self.assertFalse(response.context['is_paginated'])
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    @login_user
    def test_no_permissions(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
