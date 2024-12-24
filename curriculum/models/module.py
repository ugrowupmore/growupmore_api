# curriculum/models/module.py

from django.db import models
from curriculum.models.course import Course
from utils.basemodel import BaseModel


class Module(BaseModel):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    module_name = models.CharField(max_length=255, blank=True, null=True)
    short_intro = models.CharField(max_length=255, blank=True, null=True)
    long_intro = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = '"curriculum"."modules"'
        indexes = [
            models.Index(fields=['module_name']),
            models.Index(fields=['course']),
            models.Index(fields=['status', 'is_active']),
        ]

    def __str__(self):
        return f"{self.module_name} (Course: {self.course.name})"  # Corrected
