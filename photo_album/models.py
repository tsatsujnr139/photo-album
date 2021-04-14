import os
import uuid

from django.db import models


def photo_file_path(instance, filename):
    """generate file path for new photo"""
    extension = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{extension}'

    return os.path.join('uploads/photos/', filename)


class BaseModel(models.Model):
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created']


class Photo(BaseModel):
    id = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, primary_key=True)
    image = models.ImageField(null=True, upload_to=photo_file_path)

    def __str__(self):
        return self.title


class PhotoAlbum(BaseModel):
    id = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, primary_key=True)
    photos = models.ManyToManyField('Photo')

    def __str__(self):
        return self.title
