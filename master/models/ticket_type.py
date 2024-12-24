# master/models/ticket_type.py

from django.db import models
from utils.basemodel import BaseModel


class TicketType(BaseModel):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = '"master"."ticket_types"'
        indexes = [
            models.Index(fields=['type']),            
            models.Index(fields=['status', 'is_active']),            
        ]

    def __str__(self):
        return f"{self.type}"
