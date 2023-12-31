from http import HTTPStatus

from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from quiz_bim.tests.utils import CustomTestCase, login_superuser, login_user, get_txt_file
from step.models import FileModel
from step.tests.factories import FileFactory


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


class TestFileDetailView(CustomTestCase):
    def setUp(self):
        self.file = FileFactory.create()
        self.url = reverse("step:filemodel_detail", kwargs={"pk": self.file.pk})

    @login_superuser
    def test_file_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['file'], self.file)
        self.assertTemplateUsed(response, 'steps/file/file_detail.html')
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    @login_superuser
    def test_not_found(self):
        response = self.client.get(reverse("step:filemodel_detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    @login_user
    def test_no_permissions(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestFileCreateView(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.correct_data = {
            "file_title": "Test file",
            "lesson_file": get_txt_file()
        }
        cls.url = reverse("step:filemodel_create")
        super().setUpTestData()

    @login_superuser
    def test_file_create_view(self):
        previous_count = FileModel.objects.count()
        response = self.client.post(self.url, self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(FileModel.objects.count() - previous_count, 1)
        file = FileModel.objects.latest('create_at')
        self.assertRedirects(response, reverse("step:filemodel_list"))
        self.assertEqual(file.file_title, self.correct_data['file_title'])

    def test_anonymous(self):
        previous_count = FileModel.objects.count()
        response = self.client.post(self.url, self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(FileModel.objects.count() - previous_count, 0)

    @login_user
    def test_no_permissions(self):
        previous_count = FileModel.objects.count()
        response = self.client.post(self.url, self.correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(FileModel.objects.count() - previous_count, 0)

    @login_superuser
    def test_empty_title(self):
        invalid_data = {
            "file_title": "",
            "lesson_file": get_txt_file()
        }
        previous_count = FileModel.objects.count()
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response.context['form'], field=None,
                             errors=[_("For uploading attachment you should both enter file title and upload a file")])
        self.assertEqual(FileModel.objects.count() - previous_count, 0)

    @login_superuser
    def test_no_file(self):
        invalid_data = {
            "file_title": "Test file"
        }
        previous_count = FileModel.objects.count()
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response.context['form'], field=None,
                             errors=[_("For uploading attachment you should both enter file title and upload a file")])
        self.assertEqual(FileModel.objects.count() - previous_count, 0)


class TestFileUpdateView(CustomTestCase):
    def setUp(self):
        self.file = FileFactory.create()
        self.url = reverse("step:filemodel_update", kwargs={"pk": self.file.pk})

    @login_superuser
    def test_file_update_view(self):
        correct_data = {
            "file_title": "New title",
            "lesson_file": get_txt_file()
        }
        response = self.client.post(self.url, correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.file.refresh_from_db()
        self.assertEqual(self.file.file_title, correct_data['file_title'])
        self.assertRedirects(response, reverse("step:filemodel_list"))

    def test_anonymous(self):
        correct_data = {
            "file_title": "New title",
            "lesson_file": get_txt_file()
        }
        response = self.client.post(self.url, correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.file.refresh_from_db()
        self.assertNotEqual(self.file.file_title, correct_data['file_title'])

    @login_user
    def test_no_permissions(self):
        correct_data = {
            "file_title": "New title",
            "lesson_file": get_txt_file()
        }
        response = self.client.post(self.url, correct_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.file.refresh_from_db()
        self.assertNotEqual(self.file.file_title, correct_data['file_title'])

    @login_superuser
    def test_not_found(self):
        invalid_data = {
            "file_title": "New title",
            "lesson_file": get_txt_file()
        }
        response = self.client.post(reverse("step:filemodel_update", kwargs={"pk": 999}), invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    @login_superuser
    def test_empty_title(self):
        invalid_data = {
            "file_title": "",
            "lesson_file": get_txt_file()
        }
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response.context['form'], field=None,
                             errors=[_("For uploading attachment you should both enter file title and upload a file")])
        self.file.refresh_from_db()
        self.assertNotEqual(self.file.file_title, invalid_data['file_title'])

    @login_superuser
    def test_no_file(self):
        invalid_data = {
            "file_title": "New title",
        }
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.file.refresh_from_db()
        self.assertIsNotNone(self.file.file_title)


class TestFileDeleteView(CustomTestCase):
    def setUp(self):
        self.file = FileFactory.create()
        self.url = reverse("step:filemodel_delete", kwargs={"pk": self.file.pk})

    @login_superuser
    def test_file_delete_view(self):
        previous_count = FileModel.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(previous_count - FileModel.objects.count(), 1)
        self.assertRedirects(response, reverse("step:filemodel_list"))

    def test_anonymous(self):
        previous_count = FileModel.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(previous_count - FileModel.objects.count(), 0)

    @login_user
    def test_no_permissions(self):
        previous_count = FileModel.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(previous_count - FileModel.objects.count(), 0)

    @login_superuser
    def test_not_found(self):
        response = self.client.post(reverse("step:filemodel_delete", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
