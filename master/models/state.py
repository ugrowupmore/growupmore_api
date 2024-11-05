# master/models/state.py

from django.db import models
from master.models.country import Country
from utils.basemodel import BaseModel

class State(BaseModel):
    id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL, related_name='states')
    name = models.CharField(max_length=40, blank=True, null=True)              
    founded_date = models.DateField(null=True, blank=True)  
    website = models.URLField(blank=True, null=True)

    class Meta:
        db_table = '"master"."states"'
        indexes = [
            models.Index(fields=['name']),                            
            models.Index(fields=['status', 'is_active']),      
            models.Index(fields=['country_id']),      
        ]

    def __str__(self):
        return self.name