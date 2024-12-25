# hr/models/branch_department.py

from django.db import models
from authuser.models.employee import Employee  # Import Employee model
from hr.models.branch import Branch
from master.models.city import City
from master.models.country import Country
from master.models.department import Department
from master.models.state import State
from utils.basemodel import BaseModel


class BranchDepartment(BaseModel):
    id = models.AutoField(primary_key=True)
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='departments'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='branch_departments'
    )
    manager = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_branch_departments',
        help_text="Employee managing this branch department."
    )
    code = models.CharField(max_length=50, blank=True, null=True)    
    address = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='branch_departments'
    )
    state = models.ForeignKey(
        State,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='branch_departments'
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='branch_departments'
    )
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    contact1 = models.BigIntegerField(default=0)
    contact2 = models.BigIntegerField(default=0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    opening_hour = models.TimeField()
    closing_hour = models.TimeField()
    establishment_year = models.IntegerField(default=0)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = '"hr"."branch_departments"'
        indexes = [
            models.Index(fields=['branch']),
            models.Index(fields=['department']),
            models.Index(fields=['code']),
            models.Index(fields=['country', 'state', 'city']),
            models.Index(fields=['status', 'is_active']),
            models.Index(fields=['manager']),  # Added index for manager
        ]

    def __str__(self):
        return f"{self.branch.name} - {self.department.name} - {self.manager.first_name if self.manager else 'No Manager'}"
