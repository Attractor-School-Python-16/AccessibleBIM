# import factory
#
# from django.core.files.uploadedfile import SimpleUploadedFile
#
# from step.models import FileModel
#
#
# class FileModelFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = FileModel
#
#     file_title = factory.Faker('text', max_nb_chars=50)
#     lesson_file = SimpleUploadedFile("file.txt", b"file_content")
#
