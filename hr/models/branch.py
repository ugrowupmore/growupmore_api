# hr/models/branch.py

from django.db import models
from authuser.models.employee import Employee
from master.models.branch_type import BranchType
from master.models.city import City
from master.models.country import Country
from master.models.state import State
from utils.basemodel import BaseModel
from utils.image_utils import generate_image_path, delete_old_image_on_save, register_image_delete_signal


def image_path(instance, filename):    
    return generate_image_path(instance, filename, 'branch_logos', 'id')


class Branch(BaseModel):
    id = models.AutoField(primary_key=True)
    branch_type = models.ForeignKey(BranchType, on_delete=models.SET_NULL, null=True, blank=True, related_name='branches')
    name = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    logo = models.ImageField(upload_to=image_path, max_length=200, default="na.png")    
    address = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, related_name='branches')
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True, related_name='branches')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='branches')
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    contact1 = models.BigIntegerField(default=0)
    contact2 = models.BigIntegerField(default=0)
    email = models.EmailField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    location_url = models.URLField(blank=True, null=True)
    reports_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='reporting_branches')
    manager = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_branch',
        help_text="Employee managing this branch."
    )
    opening_hour = models.TimeField()
    closing_hour = models.TimeField()
    establishment_year = models.IntegerField(default=0)
    last_audit_date = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = '"hr"."branches"'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['code']),
            models.Index(fields=['branch_type']),
            models.Index(fields=['country', 'state', 'city']),
            models.Index(fields=['status', 'is_active']),
        ]

    def save(self, *args, **kwargs):
        delete_old_image_on_save(self, 'logo')      # logo is a field name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.name}"


# Register the image delete signal for the Branch model
register_image_delete_signal(Branch, 'logo')
