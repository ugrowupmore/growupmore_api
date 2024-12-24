# curriculum/models/course.py

from django.db import models
from curriculum.models.course_subcategory import CourseSubCategory
from utils.basemodel import BaseModel
from utils.enums import CourseLevel
from utils.image_utils import generate_image_path, delete_old_image_on_save, register_image_delete_signal


def logo_image_path(instance, filename):
    # Use the utility function to define the file path
    return generate_image_path(instance, filename, 'courses_logos', 'id')


class Course(BaseModel):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to=logo_image_path, max_length=200, default="na.png")
    level = models.CharField(max_length=20, choices=CourseLevel.choices, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    short_intro = models.CharField(max_length=255, blank=True, null=True)
    long_intro = models.TextField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    duration_days = models.IntegerField(default=0)
    course_subcategory = models.ForeignKey(CourseSubCategory, related_name='courses', on_delete=models.CASCADE)
    has_certification = models.BooleanField(default=True)    
    prerequisite = models.TextField(blank=True, null=True)
    is_for = models.TextField(blank=True, null=True)
    will_learn = models.TextField(blank=True, null=True)
    able_to = models.TextField(blank=True, null=True)
    includes = models.TextField(blank=True, null=True)
    team = models.TextField(blank=True, null=True)
    roadmap = models.URLField(blank=True, null=True)
    interview_checkpoints = models.TextField(blank=True, null=True)
    apply_for = models.TextField(blank=True, null=True)

    class Meta:
        db_table = '"curriculum"."courses"'
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['name']),
            models.Index(fields=['level']),
            models.Index(fields=['status', 'is_active']),
        ]

    def save(self, *args, **kwargs):
        # Call the utility function to delete the old image before saving
        delete_old_image_on_save(self, 'logo')
        super().save(*args, **kwargs)

    def __str__(self):
        name = self.name if self.name else "No Name"  # Corrected
        code = self.code if self.code else "No Code"
        return f"{name} ({code})"


# Register the image delete signal for the Course model
register_image_delete_signal(Course, 'logo')