from http import HTTPStatus

from django.urls import reverse

from modules.models import ModuleModel
from modules.tests import ModuleFactory
from quiz_bim.tests.utils import CustomTestCase, login_superuser, get_image_file, login_user


class TestAccessibleBIMView(CustomTestCase):

    def test_home_page(self):
        response = self.client.get(reverse("front:accessible_bim"))
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

    @login_user
    def test_no_permissions(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestModuleDetailView(CustomTestCase):
    def setUp(self):
        self.module = ModuleFactory.create()
        self.url = reverse("modules:modulemodel_detail", kwargs={"pk": self.module.pk})

    @login_superuser
    def test_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['module'], self.module)
        self.assertTemplateUsed(response, 'modules/module_detail.html')
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    @login_superuser
    def test_not_found(self):
        response = self.client.get(reverse("modules:modulemodel_detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    @login_user
    def test_no_permissions(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestModuleCreateView(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.correct_form_data = {
            "title": "Module",
            "description": "Description",
            "image": get_image_file(),
        }
        cls.url = reverse("modules:modulemodel_create")
        super().setUpTestData()

    @login_superuser
    def test_create_view(self):
        previous_count = ModuleModel.objects.count()
        response = self.client.post(self.url, data=self.correct_form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(ModuleModel.objects.count() - previous_count, 1)
        module = ModuleModel.objects.latest('create_at')
        self.assertRedirects(response, reverse("modules:modulemodel_list"))
        self.assertEqual(module.title, self.correct_form_data['title'])
        self.assertEqual(module.description, self.correct_form_data['description'])

    def test_anonymous(self):
        previous_count = ModuleModel.objects.count()
        response = self.client.post(self.url, data=self.correct_form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(ModuleModel.objects.count() - previous_count, 0)

    @login_user
    def test_no_permissions(self):
        previous_count = ModuleModel.objects.count()
        response = self.client.post(self.url, data=self.correct_form_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(ModuleModel.objects.count() - previous_count, 0)

    @login_superuser
    def test_empty_title(self):
        invalid_data = {
            "title": "",
            "description": "Description",
            "image": get_image_file(),
        }
        previous_count = ModuleModel.objects.count()
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response, 'form', 'title', 'Это поле обязательно для заполнения.')
        self.assertEqual(ModuleModel.objects.count() - previous_count, 0)

    @login_superuser
    def test_empty_description(self):
        invalid_data = {
            "title": "Module",
            "description": "",
            "image": get_image_file(),
        }
        previous_count = ModuleModel.objects.count()
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response, 'form', 'description', 'Это поле обязательно для заполнения.')
        self.assertEqual(ModuleModel.objects.count() - previous_count, 0)

    @login_superuser
    def test_no_image(self):
        invalid_data = {
            "title": "Module",
            "description": "Description",
        }
        previous_count = ModuleModel.objects.count()
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response, 'form', 'image', 'Это поле обязательно для заполнения.')
        self.assertEqual(ModuleModel.objects.count() - previous_count, 0)


class TestModuleUpdateView(CustomTestCase):

    def setUp(self):
        self.module = ModuleFactory.create()
        self.url = reverse("modules:modulemodel_update", kwargs={"pk": self.module.pk})

    @login_superuser
    def test_update_view(self):
        new_data = {
            "title": "New title",
            "description": "New description",
            "image": get_image_file(),
        }
        response = self.client.post(self.url, data=new_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.module.refresh_from_db()
        self.assertEqual(self.module.title, new_data['title'])
        self.assertEqual(self.module.description, new_data['description'])
        self.assertRedirects(response, reverse("modules:modulemodel_list"))

    def test_anonymous(self):
        new_data = {
            "title": "New title",
            "description": "New description",
            "image": get_image_file(),
        }
        response = self.client.post(self.url, data=new_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.module.refresh_from_db()
        self.assertNotEqual(self.module.title, new_data['title'])

    @login_user
    def test_no_permissions(self):
        new_data = {
            "title": "New title",
            "description": "New description",
            "image": get_image_file(),
        }
        response = self.client.post(self.url, data=new_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.module.refresh_from_db()
        self.assertNotEqual(self.module.title, new_data['title'])

    @login_superuser
    def test_not_found(self):
        invalid_data = {
            "title": "New title",
            "description": "New description",
            "image": get_image_file(),
        }
        response = self.client.post(reverse("modules:modulemodel_update", kwargs={"pk": 999}), data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    @login_superuser
    def test_empty_title(self):
        invalid_data = {
            "title": "",
            "description": "Description",
            "image": get_image_file(),
        }
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response, 'form', 'title', 'Это поле обязательно для заполнения.')
        self.module.refresh_from_db()
        self.assertNotEqual(self.module.title, invalid_data['title'])

    @login_superuser
    def test_empty_description(self):
        invalid_data = {
            "title": "Module",
            "description": "",
            "image": get_image_file(),
        }
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response, 'form', 'description', 'Это поле обязательно для заполнения.')
        self.module.refresh_from_db()
        self.assertNotEqual(self.module.description, invalid_data['description'])


class TestModuleDeleteView(CustomTestCase):

    def setUp(self):
        self.module = ModuleFactory.create()
        self.url = reverse("modules:modulemodel_delete", kwargs={"pk": self.module.pk})

    @login_superuser
    def test_delete_view(self):
        previous_count = ModuleModel.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("modules:modulemodel_list"))
        self.assertEqual(previous_count - ModuleModel.objects.count(), 1)

    def test_anonymous(self):
        previous_count = ModuleModel.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(ModuleModel.objects.count() - previous_count, 0)

    @login_user
    def test_no_permissions(self):
        previous_count = ModuleModel.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(ModuleModel.objects.count() - previous_count, 0)

    @login_superuser
    def test_not_found(self):
        response = self.client.post(reverse("modules:modulemodel_delete", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
