from http import HTTPStatus

from django.urls import reverse

from modules.models import CourseTargetModel
from modules.tests.factories import CourseTargetFactory
from quiz_bim.tests.utils import CustomTestCase, login_superuser


class TestCourseTargetListView(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("modules:coursetargetmodel_list")
        super().setUpTestData()

    @login_superuser
    def test_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertQuerysetEqual(response.context['course_targets'], CourseTargetModel.objects.order_by('-create_at'))
        self.assertTemplateUsed(response, 'course_target/course_target_list.html')
        self.assertFalse(response.context['is_paginated'])
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_no_permissions(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestCourseTargetDetailView(CustomTestCase):
    def setUp(self):
        self.course_target = CourseTargetFactory.create()
        self.url = reverse("modules:coursetargetmodel_detail", kwargs={"pk": self.course_target.pk})

    @login_superuser
    def test_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['course_target'], self.course_target)
        self.assertTemplateUsed(response, 'course_target/course_target_detail.html')
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    @login_superuser
    def test_not_found(self):
        response = self.client.get(reverse("modules:coursetargetmodel_detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_no_permissions(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestCourseTargetCreateView(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.correct_data = {
            "title": "Course Target",
            "description": "Description"
        }
        cls.url = reverse("modules:coursetargetmodel_create")
        super().setUpTestData()

    @login_superuser
    def test_create_view(self):
        previous_count = CourseTargetModel.objects.count()
        response = self.client.post(self.url, self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(CourseTargetModel.objects.count() - previous_count, 1)
        course_target = CourseTargetModel.objects.latest('create_at')
        self.assertRedirects(response, reverse("modules:coursetargetmodel_detail", kwargs={"pk": course_target.pk}))
        self.assertEqual(course_target.title, self.correct_data['title'])
        self.assertEqual(course_target.description, self.correct_data['description'])

    def test_anonymous(self):
        response = self.client.post(self.url, self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_no_permissions(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    @login_superuser
    def test_empty_title(self):
        invalid_data = {
            "title": "",
            "description": "Description",
        }
        previous_count = CourseTargetModel.objects.count()
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response, 'form', 'title', 'Это поле обязательно для заполнения.')
        self.assertEqual(CourseTargetModel.objects.count() - previous_count, 0)

    @login_superuser
    def test_empty_description(self):
        correct_data = {
            "title": "Course Target",
            "description": "",
        }
        previous_count = CourseTargetModel.objects.count()
        response = self.client.post(self.url, correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(CourseTargetModel.objects.count() - previous_count, 1)
