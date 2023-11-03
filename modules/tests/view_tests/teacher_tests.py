from http import HTTPStatus

from django.urls import reverse

from modules.models import TeacherModel
from quiz_bim.tests.utils import CustomTestCase, login_superuser, login_user


class TestTeacherListView(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("modules:teachermodel_list")
        super().setUpTestData()

    @login_superuser
    def test_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertQuerysetEqual(response.context['teachers'], TeacherModel.objects.all(), ordered=False)
        self.assertTemplateUsed(response, 'teachers/teachers_list.html')
        self.assertFalse(response.context['is_paginated'])
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    @login_user
    def test_no_permissions(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestTeacherDetailView(CustomTestCase):
    def setUp(self):
        self.teacher = TeacherModel.objects.create()
        self.url = reverse("modules:teachermodel_detail", kwargs={"pk": self.teacher.pk})

    @login_superuser
    def test_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'teachers/teacher_detail.html')
        self.assertEqual(response.context['teacher'], self.teacher)
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
        response = self.client.get(reverse("modules:teachermodel_detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
