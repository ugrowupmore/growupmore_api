# master/models/document.py

from django.db import models
from master.models.document_type import DocumentType
from utils.basemodel import BaseModel
from utils.image_utils import generate_image_path, delete_old_image_on_save, register_image_delete_signal

def image_path(instance, filename):    
    return generate_image_path(instance, filename, 'documents', 'name')

class Document(BaseModel):
    id = models.AutoField(primary_key=True)
    document_type = models.ForeignKey(DocumentType, null=True, blank=True, on_delete=models.SET_NULL, related_name='documents')
    name = models.CharField(max_length=40, blank=True, null=True)    
    image = models.ImageField(upload_to=image_path, max_length=200, default="na.png")
    description = models.CharField(max_length=100, blank=True, null=True) 
    
    class Meta:
        db_table = '"master"."documents"'
        indexes = [
            models.Index(fields=['name']),            
            models.Index(fields=['status', 'is_active']),   
            models.Index(fields=['document_type_id']),         
        ]    
    
    def save(self, *args, **kwargs):        
        delete_old_image_on_save(self, 'image')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Register the image delete signal for the Country model
register_image_delete_signal(Document, 'image')