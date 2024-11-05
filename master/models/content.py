# master/models/content.py

from django.db import models
from utils.basemodel import BaseModel


class Content(BaseModel):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=40, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = '"master"."contents"'
        indexes = [
            models.Index(fields=['content']),
            models.Index(fields=['status', 'is_active']),
        ]

    def __str__(self):
        return self.content
