from datetime import datetime

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


def upload_image_path(instance, filename):
    date = datetime.today().strftime('%Y-%m-%d')
    return f'{str(instance)}/{date}/{filename}'


class Image(models.Model):
    url = models.ImageField(upload_to=upload_image_path)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey()

    def __str__(self):
        return f'Image'


class Video(models.Model):
    url = models.ImageField(null=True, upload_to=upload_image_path)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey()

    def __str__(self):
        return f'Video'
