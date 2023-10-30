from http import HTTPStatus

from django.urls import reverse

from modules.models import ModuleModel
from quiz_bim.tests.utils import CustomTestCase, login_superuser


class TestAccessibleBIMView(CustomTestCase):

    def test_home_page(self):
        response = self.client.get(reverse("modules:index"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @login_superuser
    def test_moderator_page(self):
        response = self.client.get(reverse("modules:moderator_page"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_moderator_page_anonymous(self):
        response = self.client.get(reverse("modules:moderator_page"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_moderator_page_no_permissions(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("modules:moderator_page"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestModuleListView(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("modules:modulemodel_list")
        super().setUpTestData()

    @login_superuser
    def test_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertQuerysetEqual(response.context['modules'], ModuleModel.objects.all(), ordered=False)
        self.assertTemplateUsed(response, 'modules/modules_list.html')
        self.assertFalse(response.context['is_paginated'])
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_no_permissions(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
