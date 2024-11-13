# product/models/course_syllabus.py

from django.db import models
from learn.models.chapter import Chapter
from learn.models.subject import Subject
from learn.models.topic import Topic
from product.models.course import Course
from product.models.course_module import CourseModule
from utils.basemodel import BaseModel
from django.db.models import UniqueConstraint

class CourseSyllabus(BaseModel):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='course_syllabuses')
    module = models.ForeignKey(CourseModule, on_delete=models.SET_NULL, null=True, blank=True, related_name='course_syllabuses')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='course_syllabuses')
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True, blank=True, related_name='course_syllabuses')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='course_syllabuses')

    class Meta:
        db_table = '"product"."course_syllabus"'
        indexes = [
            models.Index(fields=['course']),
            models.Index(fields=['module']),
            models.Index(fields=['subject']),
            models.Index(fields=['chapter']),
            models.Index(fields=['topic']),
            models.Index(fields=['status', 'is_active']),
        ]
        constraints = [
            UniqueConstraint(
                fields=['course', 'module', 'subject', 'chapter', 'topic'],
                name='unique_course_syllabus'
            ),
        ]

    def __str__(self):
        return f"Syllabus for {self.course.title} - {self.module.module_name}"
