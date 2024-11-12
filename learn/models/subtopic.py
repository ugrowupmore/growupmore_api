# learn/models/subtopic.py

from django.db import models
from learn.models.chapter import Chapter
from learn.models.subject import Subject
from learn.models.topic import Topic
from utils.basemodel import BaseModel
from utils.image_utils import generate_image_path, delete_old_image_on_save, register_image_delete_signal


def image_path(instance, filename):    
    return generate_image_path(instance, filename, 'subtopics_images', 'id')


def yt_thumb_image_path(instance, filename):    
    return generate_image_path(instance, filename, 'subtopics_yt_thumbnails', 'id')


class SubTopic(BaseModel):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='subtopics')
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True, blank=True, related_name='subtopics')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='subtopics')
    title = models.CharField(max_length=100, blank=True, null=True)
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
        db_table = '"learn"."sub_topics"'
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['subject']),
            models.Index(fields=['chapter']),
            models.Index(fields=['topic']),
            models.Index(fields=['status', 'is_active']),
        ]

    def save(self, *args, **kwargs):
        delete_old_image_on_save(self, 'image')
        delete_old_image_on_save(self, 'yt_thumb_image')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} (Topic: {self.topic.title})"


# Register the image delete signals for the SubTopic model
register_image_delete_signal(SubTopic, 'image')
register_image_delete_signal(SubTopic, 'yt_thumb_image')
