# curriculum/models/subject.py

from django.db import models
from utils.basemodel import BaseModel
from utils.image_utils import generate_image_path, delete_old_image_on_save, register_image_delete_signal


def image_path(instance, filename):    
    return generate_image_path(instance, filename, 'subjects_images', 'id')


def yt_thumb_image_path(instance, filename):    
    return generate_image_path(instance, filename, 'subjects_yt_thumbnails', 'id')


class Subject(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    short_name = models.CharField(max_length=60, blank=True, null=True)
    subject_code = models.CharField(max_length=10, blank=True, null=True)
    image = models.ImageField(upload_to=image_path, max_length=200, default="na.png")
    image_alt = models.CharField(max_length=30, blank=True, null=True)
    short_intro = models.CharField(max_length=255, blank=True, null=True)
    long_intro = models.TextField(blank=True, null=True)
    yt_thumb_image = models.ImageField(upload_to=yt_thumb_image_path, max_length=200, default="na.png")
    yt_thumb_image_alt = models.CharField(max_length=30, blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    video_title = models.CharField(max_length=70, blank=True, null=True)
    video_description = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = '"curriculum"."subjects"'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['short_name']),
            models.Index(fields=['subject_code']),
            models.Index(fields=['status', 'is_active']),
        ]

    def save(self, *args, **kwargs):
        delete_old_image_on_save(self, 'image')
        delete_old_image_on_save(self, 'yt_thumb_image')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.subject_code})"
    

# Register the image delete signals for the Subject model
register_image_delete_signal(Subject, 'image')
register_image_delete_signal(Subject, 'yt_thumb_image')