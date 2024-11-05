# master/models/designation.py

from django.db import models
from utils.basemodel import BaseModel
from utils.enums import DesignationLevel

class Designation(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, blank=True, null=True)
    level = models.CharField(max_length=10, choices=DesignationLevel.choices, default=DesignationLevel.OTHER)    
    travel_required = models.BooleanField(default=False)
    training_required = models.BooleanField(default=False)   
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = '"master"."designations"'
        indexes = [
            models.Index(fields=['name']),            
            models.Index(fields=['status', 'is_active']),            
        ]

    def __str__(self):
        return self.name