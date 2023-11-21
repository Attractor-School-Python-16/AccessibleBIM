import factory


class FileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "step.FileModel"

    file_title = factory.sequence(lambda n: f'File {n}')
    lesson_file = factory.django.FileField(filename='file.txt', content_type='text/plain')


class VideoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "step.VideoModel"

    video_title = factory.sequence(lambda n: f'Video {n}')
    video_description = factory.Faker('sentence')
    video_file = factory.django.FileField(filename='video.mp4', content_type='video/mp4')
