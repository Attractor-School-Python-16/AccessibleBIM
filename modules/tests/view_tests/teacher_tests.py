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


class TestTeacherCreateView(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.correct_data = {
            "first_name": "First",
            "last_name": "Last",
            "father_name": "Father",
            "job_title": "Job",
            "corp": "Corp",
            "experience": "Experience",
            "description": "Description"
        }
        cls.url = reverse("modules:teachermodel_create")
        super().setUpTestData()

    @login_superuser
    def test_create_view(self):
        previous_count = TeacherModel.objects.count()
        response = self.client.post(self.url, data=self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(TeacherModel.objects.count() - previous_count, 1)
        teacher = TeacherModel.objects.latest('create_at')
        self.assertRedirects(response, reverse("modules:teachermodel_detail", kwargs={"pk": teacher.pk}))
        self.assertEqual(teacher.first_name, self.correct_data['first_name'])
        self.assertEqual(teacher.last_name, self.correct_data['last_name'])
        self.assertEqual(teacher.father_name, self.correct_data['father_name'])
        self.assertEqual(teacher.job_title, self.correct_data['job_title'])
        self.assertEqual(teacher.corp, self.correct_data['corp'])
        self.assertEqual(teacher.experience, self.correct_data['experience'])
        self.assertEqual(teacher.description, self.correct_data['description'])

    def test_anonymous(self):
        previous_count = TeacherModel.objects.count()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(TeacherModel.objects.count() - previous_count, 0)

    @login_user
    def test_no_permissions(self):
        previous_count = TeacherModel.objects.count()
        response = self.client.post(self.url, data=self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(TeacherModel.objects.count() - previous_count, 0)

    @login_superuser
    def test_empty_first_name(self):
        invalid_data = {
            "first_name": "",
            "last_name": "Last",
            "father_name": "Father",
            "job_title": "Job",
            "corp": "Corp",
            "experience": "Experience",
            "description": "Description"
        }
        previous_count = TeacherModel.objects.count()
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response, 'form', 'first_name', 'Это поле обязательно для заполнения.')
        self.assertEqual(TeacherModel.objects.count() - previous_count, 0)

    @login_superuser
    def test_empty_last_name(self):
        invalid_data = {
            "first_name": "First",
            "last_name": "",
            "father_name": "Father",
            "job_title": "Job",
            "corp": "Corp",
            "experience": "Experience",
            "description": "Description"
        }
        previous_count = TeacherModel.objects.count()
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response, 'form', 'last_name', 'Это поле обязательно для заполнения.')
        self.assertEqual(TeacherModel.objects.count() - previous_count, 0)

    @login_superuser
    def test_null_fields(self):
        correct_data = {
            "first_name": "First",
            "last_name": "Last",
            "father_name": "",
            "job_title": "",
            "corp": "",
            "experience": "",
            "description": ""
        }
        previous_count = TeacherModel.objects.count()
        response = self.client.post(self.url, data=correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(TeacherModel.objects.count() - previous_count, 1)
