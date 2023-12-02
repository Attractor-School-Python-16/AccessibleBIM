import random
from http import HTTPStatus

from django.urls import reverse

from modules.tests import ModuleFactory, CourseTargetFactory, CourseFactory
from subscription.tests.factories import SubscriptionFactory
from subscription.tests.utils import login_superuser, CustomTestCase, login_user
from subscription.models import SubscriptionModel


class TestSubscriptionListView(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("subscription:subscriptionmodel_list")
        super().setUpTestData()

    @login_superuser
    def test_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertQuerysetEqual(response.context['subscriptions'], SubscriptionModel.objects.all(), ordered=False)
        self.assertTemplateUsed(response, 'subscription/subscription_list.html')
        self.assertFalse(response.context['is_paginated'])
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    @login_user
    def test_no_permissions(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestSubscriptionDetailView(CustomTestCase):
    def setUp(self):
        self.subscription = SubscriptionFactory.create()
        self.url = reverse("subscription:subscriptionmodel_detail", kwargs={"pk": self.subscription.pk})

    @login_superuser
    def test_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['subscription'], self.subscription)
        self.assertTemplateUsed(response, 'subscription/subscription_detail.html')
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    @login_superuser
    def test_not_found(self):
        response = self.client.get(reverse("subscription:subscriptionmodel_detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    @login_user
    def test_no_permissions(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestSubscriptionCreateView(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.module = ModuleFactory.create()
        cls.target = CourseTargetFactory.create()
        cls.course = CourseFactory.create(title="Course", description="Description", module_id=cls.module,
                                      courseTarget_id=cls.target, language="RU", learnTime=10)
        cls.correct_form_data = {"course": cls.course.id, "price": random.randint(1, 1000)}
        cls.url = reverse("subscription:subscriptionmodel_create")
        super().setUpTestData()

    @login_superuser
    def test_create_view(self):
        previous_count = SubscriptionModel.objects.count()
        response = self.client.post(self.url, data=self.correct_form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(SubscriptionModel.objects.count() - previous_count, 1)
        subscription = SubscriptionModel.objects.latest('create_at')
        self.assertRedirects(response, reverse("subscription:subscriptionmodel_list"))
        self.assertEqual(subscription.course.id, self.correct_form_data['course'])
        self.assertEqual(subscription.price, self.correct_form_data['price'])

    def test_anonymous(self):
        previous_count = SubscriptionModel.objects.count()
        response = self.client.post(self.url, data=self.correct_form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(SubscriptionModel.objects.count() - previous_count, 0)

    @login_user
    def test_no_permissions(self):
        previous_count = SubscriptionModel.objects.count()
        response = self.client.post(self.url, data=self.correct_form_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(SubscriptionModel.objects.count() - previous_count, 0)

    @login_superuser
    def test_invalid_empty_data_field(self):
        invalid_data = {"course": "", "price": ""}
        previous_count = SubscriptionModel.objects.count()
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(SubscriptionModel.objects.count() - previous_count, 0)
        self.assertFormError(response, 'form', 'course', 'Это поле обязательно для заполнения.')
        self.assertFormError(response, 'form', 'price', 'Это поле обязательно для заполнения.')


class TestSubscriptionUpdateView(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.module = ModuleFactory.create()
        cls.target = CourseTargetFactory.create()
        cls.course = CourseFactory.create(title="Course", description="Description", module_id=cls.module,
                                          courseTarget_id=cls.target, language="RU", learnTime=10)
        cls.new_data = {"course": cls.course.id, "price": random.randint(1, 1000)}
        super().setUpTestData()


    def setUp(self) -> None:
        self.subscription = SubscriptionFactory.create()
        self.url = reverse("subscription:subscriptionmodel_update", kwargs={"pk": self.subscription.pk})

    @login_superuser
    def test_update_view(self):
        response = self.client.post(self.url, data=self.new_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.subscription.refresh_from_db()
        self.assertEqual(self.subscription.course.id, self.new_data['course'])
        self.assertEqual(self.subscription.price, self.new_data['price'])
        self.assertRedirects(response, reverse("subscription:subscriptionmodel_list"))

    def test_anonymous(self):
        response = self.client.post(self.url, data=self.new_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.subscription.refresh_from_db()
        self.assertNotEqual(self.subscription.course.id, self.new_data['course'])
        self.assertNotEqual(self.subscription.price, self.new_data['price'])

    @login_user
    def test_no_permissions(self):
        response = self.client.post(self.url, data=self.new_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.subscription.refresh_from_db()
        self.assertNotEqual(self.subscription.course.id, self.new_data['course'])
        self.assertNotEqual(self.subscription.price, self.new_data['price'])

    # @login_superuser
    # def test_invalid_empty_data_field(self):
    #     invalid_data = {"course": "", "price": ""}
    #     response = self.client.post(self.url, data=invalid_data)
    #     self.assertEqual(response.status_code, HTTPStatus.OK)
    #     self.subscription.refresh_from_db()
    #     self.assertNotEqual(self.subscription.course, None)
    #     self.assertNotEqual(self.subscription.price, None)

    @login_superuser
    def test_not_found(self):
        response = self.client.get(reverse("subscription:subscriptionmodel_update", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class TestSubscriptionDeleteView(CustomTestCase):

    def setUp(self) -> None:
        self.subscription = SubscriptionFactory.create()
        self.url = reverse("subscription:subscriptionmodel_delete", kwargs={"pk": self.subscription.pk})

    @login_superuser
    def test_delete_view(self):
        previous_count = SubscriptionModel.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(previous_count - SubscriptionModel.objects.count(), 1)
        self.assertRedirects(response, reverse("subscription:subscriptionmodel_list"))

    def test_anonymous(self):
        previous_count = SubscriptionModel.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(previous_count, SubscriptionModel.objects.count())

    @login_user
    def test_no_permissions(self):
        previous_count = SubscriptionModel.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(previous_count, SubscriptionModel.objects.count())

    @login_superuser
    def test_not_found(self):
        previous_count = SubscriptionModel.objects.count()
        response = self.client.post(reverse("subscription:subscriptionmodel_delete", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(previous_count, SubscriptionModel.objects.count())
