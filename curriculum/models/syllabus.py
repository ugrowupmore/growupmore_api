# curriculum/models/syllabus.py

from django.db import models
from curriculum.models.chapter import Chapter
from curriculum.models.subject import Subject
from curriculum.models.topic import Topic
from curriculum.models.course import Course
from curriculum.models.module import Module
from utils.basemodel import BaseModel
from django.db.models import UniqueConstraint

class Syllabus(BaseModel):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    class Meta:
        db_table = '"curriculum"."course_syllabus"'
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
        return f"{self.course.name} - {self.module.name} - {self.subject.name} - {self.chapter.name} - {self.topic.name}"