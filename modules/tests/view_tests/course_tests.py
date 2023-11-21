from http import HTTPStatus

from django.urls import reverse

from modules.models import CourseModel
from modules.tests import CourseFactory, CourseTargetFactory, TeacherFactory, ModuleFactory
from quiz_bim.tests.utils import login_superuser, CustomTestCase, login_user, get_image_file


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

    @login_user
    def test_no_permissions(self):
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

    @login_user
    def test_no_permissions(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestCourseCreateView(CustomTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.module = ModuleFactory.create()
        cls.courseTarget_id = CourseTargetFactory.create()
        cls.teacher = TeacherFactory.create()
        cls.url = f'{reverse("modules:coursemodel_create")}?module_pk={cls.module.pk}'
        cls.correct_form_data = {
            "title": "Course",
            "description": "Description",
            "image": get_image_file(),
            "learnTime": 10,
            "courseTarget_id": cls.courseTarget_id.id,
            "language": "RU",
            "teachers": [cls.teacher.id]
        }
        super().setUpTestData()

    @login_superuser
    def test_create_by_module_view(self):
        previous_count = CourseModel.objects.count()
        response = self.client.post(self.url, self.correct_form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(CourseModel.objects.count() - previous_count, 1)
        course = CourseModel.objects.latest('create_at')
        self.assertRedirects(response, reverse("modules:modulemodel_detail", kwargs={"pk": course.module_id.pk}))
        self.assertEqual(course.title, self.correct_form_data['title'])
        self.assertEqual(course.description, self.correct_form_data['description'])
        self.assertEqual(course.learnTime, self.correct_form_data['learnTime'])
        self.assertEqual(course.courseTarget_id.id, self.correct_form_data['courseTarget_id'])
        self.assertEqual(course.language, self.correct_form_data['language'])

    @login_superuser
    def test_create_view(self):
        previous_count = CourseModel.objects.count()
        correct_form_data = {
            "module_id": self.module.id,
            "title": "Course",
            "description": "Description",
            "image": get_image_file(),
            "learnTime": 10,
            "courseTarget_id": self.courseTarget_id.id,
            "language": "RU",
            "teachers": [self.teacher.id]
        }
        response = self.client.post(reverse("modules:coursemodel_create"), correct_form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(CourseModel.objects.count() - previous_count, 1)
        course = CourseModel.objects.latest('create_at')
        self.assertRedirects(response, reverse("modules:modulemodel_detail", kwargs={"pk": course.module_id.pk}))
        self.assertEqual(course.module_id.id, correct_form_data['module_id'])
        self.assertEqual(course.title, correct_form_data['title'])
        self.assertEqual(course.description, correct_form_data['description'])
        self.assertEqual(course.learnTime, correct_form_data['learnTime'])
        self.assertEqual(course.courseTarget_id.id, correct_form_data['courseTarget_id'])
        self.assertEqual(course.language, correct_form_data['language'])

    def test_anonymous(self):
        response = self.client.post(self.url, self.correct_form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    @login_user
    def test_no_permissions(self):
        response = self.client.post(self.url, self.correct_form_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    @login_superuser
    def test_standalone_empty_module_id(self):
        invalid_data = {
            "module_id": "",
            "title": "Course",
            "description": "Description",
            "image": get_image_file(),
            "learnTime": 10,
            "courseTarget_id": self.courseTarget_id.id,
            "language": "RU",
            "teachers": [self.teacher.id]
        }
        previous_count = CourseModel.objects.count()
        response = self.client.post(reverse("modules:coursemodel_create"), invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response, 'form', 'module_id', 'Это поле обязательно для заполнения.')
        self.assertEqual(CourseModel.objects.count() - previous_count, 0)

    @login_superuser
    def test_empty_title(self):
        invalid_data = {
            "title": "",
            "description": "Description",
            "image": get_image_file(),
            "learnTime": 10,
            "courseTarget_id": self.courseTarget_id.id,
            "language": "RU",
            "teachers": [self.teacher.id]
        }
        previous_count = CourseModel.objects.count()
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response, 'form', 'title', 'Это поле обязательно для заполнения.')
        self.assertEqual(CourseModel.objects.count() - previous_count, 0)

    @login_superuser
    def test_empty_description(self):
        invalid_data = {
            "title": "Course",
            "description": "",
            "image": get_image_file(),
            "learnTime": 10,
            "courseTarget_id": self.courseTarget_id.id,
            "language": "RU",
            "teachers": [self.teacher.id]
        }
        previous_count = CourseModel.objects.count()
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response, 'form', 'description', 'Это поле обязательно для заполнения.')
        self.assertEqual(CourseModel.objects.count() - previous_count, 0)

    @login_superuser
    def test_empty_image(self):
        invalid_data = {
            "title": "Course",
            "description": "Description",
            "image": "",
            "learnTime": 10,
            "courseTarget_id": self.courseTarget_id.id,
            "language": "RU",
            "teachers": [self.teacher.id]
        }
        previous_count = CourseModel.objects.count()
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response, 'form', 'image', 'Это поле обязательно для заполнения.')
        self.assertEqual(CourseModel.objects.count() - previous_count, 0)

    @login_superuser
    def test_empty_learnTime(self):
        invalid_data = {
            "title": "Course",
            "description": "Description",
            "image": get_image_file(),
            "learnTime": "",
            "courseTarget_id": self.courseTarget_id.id,
            "language": "RU",
            "teachers": [self.teacher.id]
        }
        previous_count = CourseModel.objects.count()
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response, 'form', 'learnTime', 'Это поле обязательно для заполнения.')
        self.assertEqual(CourseModel.objects.count() - previous_count, 0)

    @login_superuser
    def test_empty_courseTarget_id(self):
        invalid_data = {
            "title": "Course",
            "description": "Description",
            "image": get_image_file(),
            "learnTime": 10,
            "courseTarget_id": "",
            "language": "RU",
            "teachers": [self.teacher.id]
        }
        previous_count = CourseModel.objects.count()
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response, 'form', 'courseTarget_id', 'Это поле обязательно для заполнения.')
        self.assertEqual(CourseModel.objects.count() - previous_count, 0)

    @login_superuser
    def test_empty_language(self):
        invalid_data = {
            "title": "Course",
            "description": "Description",
            "image": get_image_file(),
            "learnTime": 10,
            "courseTarget_id": self.courseTarget_id.id,
            "language": "",
            "teachers": [self.teacher.id]
        }
        previous_count = CourseModel.objects.count()
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response, 'form', 'language', 'Это поле обязательно для заполнения.')
        self.assertEqual(CourseModel.objects.count() - previous_count, 0)

    @login_superuser
    def test_no_teachers(self):
        invalid_data = {
            "title": "Course",
            "description": "Description",
            "image": get_image_file(),
            "learnTime": 10,
            "courseTarget_id": self.courseTarget_id.id,
            "language": "RU",
            "teachers": []
        }
        previous_count = CourseModel.objects.count()
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response, 'form', 'teachers', 'Это поле обязательно для заполнения.')
        self.assertEqual(CourseModel.objects.count() - previous_count, 0)


class TestCourseUpdateView(CustomTestCase):

    def setUp(self):
        self.course = CourseFactory.create()
        self.url = reverse("modules:coursemodel_update", kwargs={"pk": self.course.pk})

    @login_superuser
    def test_update_view(self):
        module = ModuleFactory.create()
        course_target = CourseTargetFactory.create()
        teacher = TeacherFactory.create()
        new_data = {
            "module_id": module.id,
            "title": "New title",
            "description": "New description",
            "image": get_image_file(),
            "learnTime": 15,
            "courseTarget_id": course_target.id,
            "language": "RU",
            "teachers": [teacher.id]
        }
        response = self.client.post(self.url, data=new_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, new_data['title'])
        self.assertEqual(self.course.description, new_data['description'])
        self.assertEqual(self.course.learnTime, new_data['learnTime'])
        self.assertEqual(self.course.courseTarget_id.id, new_data['courseTarget_id'])
        self.assertEqual(self.course.language, new_data['language'])

    def test_anonymous(self):
        module = ModuleFactory.create()
        course_target = CourseTargetFactory.create()
        teacher = TeacherFactory.create()
        new_data = {
            "module_id": module.id,
            "title": "New title",
            "description": "New description",
            "image": get_image_file(),
            "learnTime": 15,
            "courseTarget_id": course_target.id,
            "language": "RU",
            "teachers": [teacher.id]
        }
        response = self.client.post(self.url, data=new_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.course.refresh_from_db()
        self.assertNotEqual(self.course.title, new_data['title'])
        self.assertNotEqual(self.course.description, new_data['description'])

    @login_user
    def test_no_permissions(self):
        module = ModuleFactory.create()
        course_target = CourseTargetFactory.create()
        teacher = TeacherFactory.create()
        new_data = {
            "module_id": module.id,
            "title": "New title",
            "description": "New description",
            "image": get_image_file(),
            "learnTime": 15,
            "courseTarget_id": course_target.id,
            "language": "RU",
            "teachers": [teacher.id]
        }
        response = self.client.post(self.url, data=new_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.course.refresh_from_db()
        self.assertNotEqual(self.course.title, new_data['title'])
        self.assertNotEqual(self.course.description, new_data['description'])

    @login_superuser
    def test_not_found(self):
        module = ModuleFactory.create()
        course_target = CourseTargetFactory.create()
        teacher = TeacherFactory.create()
        new_data = {
            "module_id": module.id,
            "title": "New title",
            "description": "New description",
            "image": get_image_file(),
            "learnTime": 15,
            "courseTarget_id": course_target.id,
            "language": "RU",
            "teachers": [teacher.id]
        }
        response = self.client.post(reverse("modules:coursemodel_update", kwargs={"pk": 999}), data=new_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    @login_superuser
    def test_invalid_module_id(self):
        course_target = CourseTargetFactory.create()
        teacher = TeacherFactory.create()
        invalid_data = {
            "module_id": "",
            "title": "New title",
            "description": "New description",
            "image": get_image_file(),
            "learnTime": 15,
            "courseTarget_id": course_target.id,
            "language": "RU",
            "teachers": [teacher.id]
        }
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response, 'form', 'module_id', 'Это поле обязательно для заполнения.')
        self.course.refresh_from_db()
        self.assertNotEqual(self.course.module_id.id, invalid_data['module_id'])

    @login_superuser
    def test_empty_title(self):
        module = ModuleFactory.create()
        course_target = CourseTargetFactory.create()
        teacher = TeacherFactory.create()
        invalid_data = {
            "module_id": module.id,
            "title": "",
            "description": "Description",
            "image": get_image_file(),
            "learnTime": 15,
            "courseTarget_id": course_target.id,
            "language": "RU",
            "teachers": [teacher.id]
        }
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response, 'form', 'title', 'Это поле обязательно для заполнения.')
        self.course.refresh_from_db()
        self.assertNotEqual(self.course.title, invalid_data['title'])

    @login_superuser
    def test_empty_description(self):
        module = ModuleFactory.create()
        course_target = CourseTargetFactory.create()
        teacher = TeacherFactory.create()
        invalid_data = {
            "module_id": module.id,
            "title": "Course",
            "description": "",
            "image": get_image_file(),
            "learnTime": 15,
            "courseTarget_id": course_target.id,
            "language": "RU",
            "teachers": [teacher.id]
        }
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response, 'form', 'description', 'Это поле обязательно для заполнения.')
        self.course.refresh_from_db()
        self.assertNotEqual(self.course.description, invalid_data['description'])

    @login_superuser
    def test_invalid_courseTarget_id(self):
        module = ModuleFactory.create()
        teacher = TeacherFactory.create()
        invalid_data = {
            "module_id": module.id,
            "title": "Course",
            "description": "Description",
            "image": get_image_file(),
            "learnTime": 15,
            "courseTarget_id": "",
            "language": "RU",
            "teachers": [teacher.id]
        }
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response, 'form', 'courseTarget_id', 'Это поле обязательно для заполнения.')
        self.course.refresh_from_db()
        self.assertNotEqual(self.course.courseTarget_id.id, invalid_data['courseTarget_id'])

    @login_superuser
    def test_invalid_language(self):
        module = ModuleFactory.create()
        course_target = CourseTargetFactory.create()
        teacher = TeacherFactory.create()
        invalid_data = {
            "module_id": module.id,
            "title": "Course",
            "description": "Description",
            "image": get_image_file(),
            "learnTime": 15,
            "courseTarget_id": course_target.id,
            "language": "",
            "teachers": [teacher.id]
        }
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response, 'form', 'language', 'Это поле обязательно для заполнения.')
        self.course.refresh_from_db()
        self.assertNotEqual(self.course.language, invalid_data['language'])


class TestCourseDeleteView(CustomTestCase):

    def setUp(self):
        self.course = CourseFactory.create()
        self.url = reverse("modules:coursemodel_delete", kwargs={"pk": self.course.pk})

    @login_superuser
    def test_delete_view(self):
        previous_count = CourseModel.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(previous_count - CourseModel.objects.count(), 1)
        self.assertRedirects(response, reverse("modules:modulemodel_detail", kwargs={"pk": self.course.module_id.pk}))

    def test_anonymous(self):
        previous_count = CourseModel.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(previous_count - CourseModel.objects.count(), 0)

    @login_user
    def test_no_permissions(self):
        previous_count = CourseModel.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(CourseModel.objects.count() - previous_count, 0)

    @login_superuser
    def test_not_found(self):
        response = self.client.post(reverse("modules:coursemodel_delete", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
