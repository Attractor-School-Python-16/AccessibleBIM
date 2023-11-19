from django.test import TestCase

from modules.tests import CourseFactory, ModuleFactory, CourseTargetFactory
from subscription.tests.factories import SubscriptionFactory


class TestSubscriptionModel(TestCase):
    def test_subscription_factory_no_exception(self):
        try:
            subscription = SubscriptionFactory.create()
        except ValueError:
            self.fail("ValueError exception was raised")

    def test_subscription_factory(self):
        module = ModuleFactory.create()
        target = CourseTargetFactory.create()
        course = CourseFactory.create(title="Course", description="Description", module_id=module,
                                      courseTarget_id=target, language="RU", learnTime=10)
        subscription = SubscriptionFactory.create(course=course)
        self.assertEqual(subscription.course, course)
        self.assertGreater(subscription.price, 0)
        self.assertIsNotNone(subscription.is_published)
