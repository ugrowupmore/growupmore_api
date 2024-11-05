# master/models/package.py

from django.db import models
from utils.basemodel import BaseModel
from utils.image_utils import generate_image_path, delete_old_image_on_save, register_image_delete_signal


def image_path(instance, filename):
    # Use the utility function to define the file path
    return generate_image_path(instance, filename, 'packages', 'name')


class Package(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, blank=True, null=True)
    image = models.ImageField(upload_to=image_path, max_length=200, default="na.png")
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = '"master"."packages"'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['status', 'is_active']),
        ]

    def save(self, *args, **kwargs):
        # Call the utility function to delete the old image before saving
        delete_old_image_on_save(self, 'image')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Register the image delete signal for the Package model
register_image_delete_signal(Package, 'image')
