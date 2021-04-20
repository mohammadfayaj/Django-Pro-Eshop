from swapper import swappable_setting
from django.db import models
from notifications.base.models import AbstractNotification
# from .base.models import AbstractNotification, notify_handler  # noqa
from django.contrib.auth.models import Group, User
import os
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import uuid


def get_directory(instance, filename):
    return instance.get_file_directory(filename)

class Notification(AbstractNotification):
    FILE_DIRECTORY = 'notifications'
    image = models.ImageField(upload_to=get_directory, null=True, blank=True)
    notification_slug = models.CharField(max_length=250, blank=True, null=True, editable=True, unique=True, default=uuid.uuid4)
    attach_url = models.URLField(max_length=400, null=True, blank=True, help_text='Enter Your Destination Url')

    def save(self):
        super(Notification,self).save()

        if self.image:
            #Opening the uploaded image
            img = Image.open(self.image) # Open Image On The Fly

            if img.height > 1140 or img.width > 1140:
                # output = BytesIO() 

                #Resize/modify the image
                output_size = (1140, 1140)
                img.thumbnail(output_size)
                img = img.convert('RGB')

                output = BytesIO()
                #after modifications, save it to the output
                img.save(output, format='JPEG' ,quality=100)
                output.seek(0)

                #change the imagefield value to be the newley modifed image value
                self.image = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

            super(Notification,self).save()



    class Meta(AbstractNotification.Meta):
        abstract = False
        swappable = swappable_setting('notifications', 'Notification')

    @staticmethod
    def get_file_directory(filename):
        return os.path.join(Notification.FILE_DIRECTORY, filename)