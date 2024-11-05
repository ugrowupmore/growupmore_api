# master/models/faq_category.py

from django.db import models
from utils.basemodel import BaseModel


class FAQCategory(BaseModel):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=40, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = '"master"."faq_categories"'
        indexes = [
            models.Index(fields=['category']),            
            models.Index(fields=['status', 'is_active']),            
        ]

    def __str__(self):
        return self.category
