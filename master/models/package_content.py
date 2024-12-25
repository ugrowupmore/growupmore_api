# master/models/package_content.py

from django.db import models
from utils.basemodel import BaseModel
from master.models.package import Package
from master.models.content import Content


class PackageContent(BaseModel):
    id = models.AutoField(primary_key=True)
    package = models.ForeignKey(Package, null=True, blank=True, on_delete=models.SET_NULL, related_name='package_contents')
    content = models.ForeignKey(Content, null=True, blank=True, on_delete=models.SET_NULL, related_name='package_contents')    
    
    class Meta:
        db_table = '"master"."package_contents"'
        indexes = [
            models.Index(fields=['package_id']),
            models.Index(fields=['content_id']),            
            models.Index(fields=['status', 'is_active']),            
        ]        
    
    def __str__(self):
        return self.package.name + ' - ' + self.content.content
