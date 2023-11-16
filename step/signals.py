from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from step.models import VideoModel


@receiver(pre_delete, sender=VideoModel)
def image_model_delete(sender, instance, **kwargs):
    if instance.video_file.name:
        instance.video_file.delete(False)