# product/models/recommended_course.py

from django.db import models
from product.models.course import Course
from utils.basemodel import BaseModel
from django.db.models import UniqueConstraint
from utils.enums import Priority
from django.core.exceptions import ValidationError


class RecommendedCourse(BaseModel):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='recommended_courses')
    recommended_course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='recommended_for_courses')
    priority = models.CharField(max_length=20, choices=Priority.choices, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = '"course"."recommended_courses"'
        indexes = [
            models.Index(fields=['course']),
            models.Index(fields=['recommended_course']),
            models.Index(fields=['priority']),
            models.Index(fields=['status', 'is_active']),
        ]
        constraints = [
            UniqueConstraint(
                fields=['course', 'recommended_course'],
                name='unique_course_recommendation'
            ),
        ]

    def clean(self):
        # Ensure that course and recommended_course are not the same
        if self.course == self.recommended_course:
            raise ValidationError("Course and recommended course cannot be the same.")

    def save(self, *args, **kwargs):
        # Call clean method to enforce the validation before saving
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Recommended: {self.recommended_course.title} for {self.course.title}"
