from unittest import TestCase

from modules.tests.factories import ModuleFactory


class TestModuleModel(TestCase):
    def test_module_factory_no_exception(self):
        try:
            module = ModuleFactory.create()
        except Exception:
            self.fail("Exception was raised")

    def test_module_factory(self):
        module = ModuleFactory.create(title="Module", description="Description")
        self.assertEqual(module.title, "Module")
        self.assertEqual(module.description, "Description")
