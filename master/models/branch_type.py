# master/models/branch_type.py

from django.db import models
from utils.basemodel import BaseModel
from utils.image_utils import generate_image_path, delete_old_image_on_save, register_image_delete_signal

def image_path(instance, filename):    
    return generate_image_path(instance, filename, 'branch_types', 'type')

class BranchType(BaseModel):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=40, blank=True, null=True)        
    image = models.ImageField(upload_to=image_path, max_length=200, default="na.png")
    description = models.CharField(max_length=100, blank=True, null=True) 
    
    class Meta:
        db_table = '"master"."branch_types"'
        indexes = [
            models.Index(fields=['type']),            
            models.Index(fields=['status', 'is_active']),            
        ]
    
    def save(self, *args, **kwargs):        
        delete_old_image_on_save(self, 'image')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.type


# Register the image delete signal for the Country model
register_image_delete_signal(BranchType, 'image')