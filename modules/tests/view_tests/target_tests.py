from http import HTTPStatus

from django.urls import reverse

from modules.models import CourseTargetModel
from modules.tests.factories import CourseTargetFactory
from quiz_bim.tests.utils import CustomTestCase, login_superuser, login_user


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

    @login_user
    def test_no_permissions(self):
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

    @login_user
    def test_no_permissions(self):
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
        previous_count = CourseTargetModel.objects.count()
        response = self.client.post(self.url, self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(CourseTargetModel.objects.count() - previous_count, 0)

    @login_user
    def test_no_permissions(self):
        previous_count = CourseTargetModel.objects.count()
        response = self.client.post(self.url, self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(CourseTargetModel.objects.count() - previous_count, 0)

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


class TestCourseTargetUpdateView(CustomTestCase):

    def setUp(self):
        self.course_target = CourseTargetFactory.create()
        self.url = reverse("modules:coursetargetmodel_update", kwargs={"pk": self.course_target.pk})

    @login_superuser
    def test_update_view(self):
        new_data = {
            "title": "New title",
            "description": "New description"
        }
        response = self.client.post(self.url, data=new_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.course_target.refresh_from_db()
        self.assertEqual(self.course_target.title, new_data['title'])
        self.assertEqual(self.course_target.description, new_data['description'])
        self.assertRedirects(response, reverse("modules:coursetargetmodel_list"))

    def test_anonymous(self):
        new_data = {
            "title": "New title",
            "description": "New description"
        }
        response = self.client.post(self.url, data=new_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.course_target.refresh_from_db()
        self.assertNotEqual(self.course_target.title, new_data['title'])

    @login_user
    def test_no_permissions(self):
        new_data = {
            "title": "New title",
            "description": "New description"
        }
        response = self.client.post(self.url, data=new_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.course_target.refresh_from_db()
        self.assertNotEqual(self.course_target.title, new_data['title'])

    @login_superuser
    def test_empty_title(self):
        invalid_data = {
            "title": "",
            "description": "Description",
        }
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response, 'form', 'title', 'Это поле обязательно для заполнения.')
        self.course_target.refresh_from_db()
        self.assertNotEqual(self.course_target.title, invalid_data['title'])

    @login_superuser
    def test_empty_description(self):
        correct_data = {
            "title": "Course Target",
            "description": "",
        }
        response = self.client.post(self.url, data=correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.course_target.refresh_from_db()
        self.assertEqual(self.course_target.title, correct_data['title'])
        self.assertEqual(self.course_target.description, correct_data['description'])


class TestCourseTargetDeleteView(CustomTestCase):
    def setUp(self):
        self.course_target = CourseTargetFactory.create()
        self.url = reverse("modules:coursetargetmodel_delete", kwargs={"pk": self.course_target.pk})

    @login_superuser
    def test_delete_view(self):
        previous_count = CourseTargetModel.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("modules:coursetargetmodel_list"))
        self.assertEqual(previous_count - CourseTargetModel.objects.count(), 1)

    def test_anonymous(self):
        previous_count = CourseTargetModel.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(CourseTargetModel.objects.count() - previous_count, 0)

    @login_user
    def test_no_permissions(self):
        previous_count = CourseTargetModel.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(CourseTargetModel.objects.count() - previous_count, 0)
