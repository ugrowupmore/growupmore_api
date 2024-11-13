# product/models/course_module.py

from django.db import models
from product.models.course import Course
from utils.basemodel import BaseModel


class CourseModule(BaseModel):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='course_modules')
    module_name = models.CharField(max_length=255, blank=True, null=True)
    short_intro = models.CharField(max_length=255, blank=True, null=True)
    long_intro = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = '"product"."course_modules"'
        indexes = [
            models.Index(fields=['module_name']),
            models.Index(fields=['course']),
            models.Index(fields=['status', 'is_active']),
        ]

    def __str__(self):
        return f"{self.module_name} (Course: {self.course.title})"
