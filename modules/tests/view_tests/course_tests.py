from http import HTTPStatus

from django.urls import reverse

from modules.models import CourseModel
from modules.tests import CourseFactory
from quiz_bim.tests.utils import login_superuser, CustomTestCase


class TestCourseListView(CustomTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("modules:coursemodel_list")
        super().setUpTestData()

    @login_superuser
    def test_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertQuerysetEqual(response.context['courses'], CourseModel.objects.order_by('-create_at'))
        self.assertTemplateUsed(response, 'courses/courses_list.html')
        self.assertFalse(response.context['is_paginated'])
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_no_permissions(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestCourseDetailView(CustomTestCase):

    def setUp(self):
        self.course = CourseFactory.create()
        self.url = reverse("modules:coursemodel_detail", kwargs={"pk": self.course.pk})

    @login_superuser
    def test_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['course'], self.course)
        self.assertTemplateUsed(response, 'courses/course_detail.html')
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    @login_superuser
    def test_not_found(self):
        response = self.client.get(reverse("modules:coursemodel_detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_no_permissions(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
