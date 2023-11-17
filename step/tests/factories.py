import factory


class FileModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "step.FileModel"

    file_title = factory.sequence(lambda n: f'File {n}')
    lesson_file = factory.django.FileField(filename='file.txt', content_type='text/plain')
