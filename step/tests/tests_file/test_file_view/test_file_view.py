# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth.models import User, Permission
# from django.core.files.uploadedfile import SimpleUploadedFile
# import tempfile
# import os
#
# from step.forms.file_form import FileForm
# from step.models import FileModel
#
#
# class FileModelTestCase(TestCase):
#     def setUp(self):
#         self.temp_file = SimpleUploadedFile("file.txt", b"file_content")
#         self.user = User.objects.create_user(username='testuser', password='testpass')
#         self.file = FileModel.objects.create(file_title="Test File", lesson_file=self.temp_file)
#
#     def test_file_model(self):
#         self.assertEqual(self.file.file_title, "Test File")
#         self.assertEqual(str(self.file), f'Файл {self.file.id} Test File')
#
#     def test_file_create_view(self):
#         self.client.login(username='testuser', password='testpass')
#         response = self.client.get(reverse('step:file_create'))
#         self.assertEqual(response.status_code, 200)
#
#     def test_file_create_form_valid(self):
#         self.client.login(username='testuser', password='testpass')
#         data = {'file_title': 'Test File 2'}
#         form = FileForm(data, files={'lesson_file': self.temp_file})
#         self.assertTrue(form.is_valid())
#         response = self.client.post(reverse('step:file_create'), data)
#         self.assertEqual(response.status_code, 302)
#         self.assertTrue(FileModel.objects.filter(file_title='Test File 2').exists())
#
#     def test_file_create_form_invalid(self):
#         self.client.login(username='testuser', password='testpass')
#         form = FileForm({}, files={'lesson_file': self.temp_file})
#         self.assertFalse(form.is_valid())
#         response = self.client.post(reverse('step:file_create'), {})
#         self.assertEqual(response.status_code, 200)
#         self.assertFalse(FileModel.objects.filter(file_title='').exists())
#
#     def test_file_update_view(self):
#         self.client.login(username='testuser', password='testpass')
#         response = self.client.get(reverse('step:file_update', args=[self.file.id]))
#         self.assertEqual(response.status_code, 200)
#
#     def test_file_update_form_valid(self):
#         self.client.login(username='testuser', password='testpass')
#         data = {'file_title': 'Updated Test File'}
#         form = FileForm(data, files={'lesson_file': self.temp_file})
#         self.assertTrue(form.is_valid())
#         response = self.client.post(reverse('step:file_update', args=[self.file.id]), data)
#         self.assertEqual(response.status_code, 302)
#         self.file.refresh_from_db()
#         self.assertEqual(self.file.file_title, 'Updated Test File')
#
#     def test_file_update_form_invalid(self):
#         self.client.login(username='testuser', password='testpass')
#         form = FileForm({}, files={'lesson_file': self.temp_file})
#         self.assertFalse(form.is_valid())
#         response = self.client.post(reverse('step:file_update', args=[self.file.id]), {})
#         self.assertEqual(response.status_code, 200)
#         self.file.refresh_from_db()
#         self.assertNotEqual(self.file.file_title, '')
#
#     def test_file_delete_view(self):
#         self.client.login(username='testuser', password='testpass')
#         response = self.client.get(reverse('step:file_delete', args=[self.file.id]))
#         self.assertEqual(response.status_code, 200)
#
#     def test_file_delete(self):
#         self.client.login(username='testuser', password='testpass')
#         response = self.client.post(reverse('step:file_delete', args=[self.file.id]))
#         self.assertEqual(response.status_code, 302)
#         self.assertFalse(FileModel.objects.filter(id=self.file.id).exists())
#
#     def test_file_permissions(self):
#         self.client.login(username='testuser', password='testpass')
#         response = self.client.get(reverse('step:file_create'))
#         self.assertEqual(response.status_code, 403)
#         response = self.client.get(reverse('step:file_update', args=[self.file.id]))
#         self.assertEqual(response.status_code, 403)
#         response = self.client.get(reverse('step:file_delete', args=[self.file.id]))
#         self.assertEqual(response.status_code, 403)
