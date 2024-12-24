# master/models/department.py

from django.db import models
from utils.basemodel import BaseModel

class Department(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
   
    class Meta:
        db_table = '"master"."departments"'
        indexes = [
            models.Index(fields=['name']),            
            models.Index(fields=['status', 'is_active']),            
        ]

    def __str__(self):
        return self.name