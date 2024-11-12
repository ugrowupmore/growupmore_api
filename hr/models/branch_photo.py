# hr/models/branch_photo.py

from django.db import models
from hr.models.branch import Branch
from utils.basemodel import BaseModel
from utils.image_utils import generate_image_path, delete_old_image_on_save, register_image_delete_signal


def image_path(instance, filename):    
    return generate_image_path(instance, filename, 'branch_photos', 'id')


class BranchPhoto(BaseModel):
    id = models.AutoField(primary_key=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='branch_photos')
    image = models.ImageField(upload_to=image_path, max_length=200, default="na.png")
    title = models.CharField(max_length=100, blank=True, null=True)
    alt_text = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = '"hr"."branch_photos"'
        indexes = [
            models.Index(fields=['branch']),
            models.Index(fields=['title']),
            models.Index(fields=['status', 'is_active']),
        ]

    def save(self, *args, **kwargs):
        delete_old_image_on_save(self, 'image')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Photo {self.title} for {self.branch.name}"


# Register the image delete signal for the BranchPhoto model
register_image_delete_signal(BranchPhoto, 'image')
