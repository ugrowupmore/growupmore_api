# master/models/bank.py

from django.db import models
from master.models.country import Country
from utils.basemodel import BaseModel

class Bank(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, blank=True, null=True)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL, related_name='banks')
    swift_code = models.CharField(max_length=11, blank=True, null=True)
    iban_code = models.CharField(max_length=34, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = '"master"."banks"'
        indexes = [
            models.Index(fields=['name']),            
            models.Index(fields=['status', 'is_active']),            
            models.Index(fields=['swift_code']),
            models.Index(fields=['iban_code']),      
            models.Index(fields=['country_id']),      
        ]

    def __str__(self):
        return self.name