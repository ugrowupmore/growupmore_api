# master/models/course_sub_category.py

from django.db import models
from utils.basemodel import BaseModel
from master.models.course_category import CourseCategory


class CourseSubCategory(BaseModel):
    id = models.AutoField(primary_key=True)
    course_category = models.ForeignKey(CourseCategory, null=True, blank=True, on_delete=models.SET_NULL, related_name='sub_categories')
    sub_category = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = '"master"."course_sub_categories"'
        indexes = [
            models.Index(fields=['course_category_id']),
            models.Index(fields=['sub_category']),            
            models.Index(fields=['status', 'is_active']),            
        ]

    def __str__(self):
        return self.sub_category if self.sub_category else "No Subcategory"

