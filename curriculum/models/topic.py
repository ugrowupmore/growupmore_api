# curriculum/models/topic.py
    
from django.db import models
from curriculum.models.chapter import Chapter
from utils.basemodel import BaseModel
from utils.image_utils import generate_image_path, delete_old_image_on_save, register_image_delete_signal


def yt_thumb_image_path(instance, filename):    
    return generate_image_path(instance, filename, 'topic_yt_thumbnails', 'id')


class Topic(BaseModel):
    id = models.AutoField(primary_key=True)
    chapter = models.ForeignKey(Chapter, related_name='topics', on_delete=models.CASCADE)    
    name = models.CharField(max_length=100, blank=True, null=True)
    short_intro = models.CharField(max_length=255, blank=True, null=True)
    long_intro = models.TextField(blank=True, null=True)
    yt_thumb_image = models.ImageField(upload_to=yt_thumb_image_path, max_length=200, default="na.png")
    yt_thumb_image_alt = models.CharField(max_length=30, blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    video_title = models.CharField(max_length=70, blank=True, null=True)
    video_description = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = '"curriculum"."topics"'
        indexes = [
            models.Index(fields=['name']),            
            models.Index(fields=['chapter']),
            models.Index(fields=['status', 'is_active']),
        ]

    def save(self, *args, **kwargs):
        delete_old_image_on_save(self, 'yt_thumb_image')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (Chapter: {self.chapter.name})"  # Corrected


# Register the image delete signal for the Topic model
register_image_delete_signal(Topic, 'yt_thumb_image')