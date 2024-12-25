# master/models/country.py

from django.db import models
from utils.basemodel import BaseModel
from utils.image_utils import generate_image_path, delete_old_image_on_save, register_image_delete_signal


def image_path(instance, filename):
    # Use the utility function to define the file path
    return generate_image_path(instance, filename, 'countries_flags', 'iso3')

class Country(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    numeric_code = models.IntegerField(default=0)
    iso2 = models.CharField(max_length=2, blank=True, null=True)
    iso3 = models.CharField(max_length=3, blank=True, null=True)
    phone_code = models.CharField(max_length=10, blank=True, null=True)
    currency = models.CharField(max_length=10, blank=True, null=True)
    currency_name = models.CharField(max_length=30, blank=True, null=True)
    currency_symbol = models.CharField(max_length=5, blank=True, null=True)
    national_language = models.CharField(max_length=20, blank=True, null=True)
    nationality = models.CharField(max_length=20, blank=True, null=True)
    languages = models.CharField(max_length=255, blank=True, null=True)    
    tld = models.CharField(max_length=5, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    founded_date = models.DateField(null=True, blank=True)
    flag_image = models.ImageField(upload_to=image_path, max_length=200, default="na.png")

    class Meta:
        db_table = '"master"."countries"'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['iso2']),
            models.Index(fields=['iso3']),
            models.Index(fields=['status', 'is_active']),
            models.Index(fields=['currency']),
            models.Index(fields=['national_language']),
            models.Index(fields=['nationality']),
            models.Index(fields=['languages']),
        ]

    def save(self, *args, **kwargs):
        # Call the utility function to delete the old image before saving
        delete_old_image_on_save(self, 'flag_image')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Register the image delete signal for the Country model
register_image_delete_signal(Country, 'flag_image')