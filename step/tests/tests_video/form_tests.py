from unittest import TestCase

from quiz_bim.tests.utils import get_video_file
from step.forms.video_form import VideoForm


class TestVideoForm(TestCase):
    def test_video_model(self):
        correct_data = {
            "video_title": "Video",
            "video_description": "Description",
        }
        files = {"video_file": get_video_file()}
        form = VideoForm(correct_data, files)
        self.assertTrue(form.is_valid())

    def test_empty_title(self):
        invalid_data = {
            "video_title": "",
            "video_description": "Description",
        }
        files = {"video_file": get_video_file()}
        form = VideoForm(invalid_data, files)
        self.assertFalse(form.is_valid())

    def test_empty_description(self):
        invalid_data = {
            "video_title": "Video",
            "video_description": "",
        }
        files = {"video_file": get_video_file()}
        form = VideoForm(invalid_data, files)
        self.assertTrue(form.is_valid())

    def test_no_video_file(self):
        invalid_data = {
            "video_title": "Video",
            "video_description": "Description",
        }
        form = VideoForm(invalid_data)
        self.assertFalse(form.is_valid())
