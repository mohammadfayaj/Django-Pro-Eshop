from swapper import swappable_setting

from django.db import models
from notifications.base.models import AbstractNotification
# from .base.models import AbstractNotification, notify_handler  # noqa
from django.contrib.auth.models import Group
import os
from django.conf import settings
from PIL import Image


def get_directory(instance, filename):
    return instance.get_file_directory(filename)

class Notification(AbstractNotification):
    FILE_DIRECTORY = 'notifications'
    image = models.ImageField(upload_to=get_directory, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (400, 400)
            img.thumbnail(output_size)
            img.save(self.image.path)


    class Meta(AbstractNotification.Meta):
        abstract = False
        swappable = swappable_setting('notifications', 'Notification')

    @staticmethod
    def get_file_directory(filename):
        return os.path.join(Notification.FILE_DIRECTORY, filename)