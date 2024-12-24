# utils/basemodel.py

from django.db import models
from utils.enums import StatusType

class BaseModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(null=True)
    status = models.CharField(max_length=10, choices=StatusType.choices, default=StatusType.DRAFT)
    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True
