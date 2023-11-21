from django.test import TestCase
from django.urls import reverse

from step.tests.factories import VideoFactory


class TestVideoModel(TestCase):
    def test_video_factory_no_exception(self):
        try:
            video = VideoFactory.create()
        except Exception:
            self.fail("Exception was raised")

    def test_video_factory(self):
        video = VideoFactory.create(video_title="Video")
        self.assertEqual(video.video_title, "Video")

    def test_video_functions(self):
        video = VideoFactory.create(video_title="Video")
        self.assertEqual(str(video), f'Видео {video.id} Video')
        self.assertEqual(video.get_absolute_url(), reverse('step:videomodel_list'))
