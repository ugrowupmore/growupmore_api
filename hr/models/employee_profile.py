# hr/models/employee.py

from django.db import models
from authuser.models.employee import Employee
from hr.models.branch import Branch
from master.models.city import City
from master.models.country import Country
from master.models.department import Department
from master.models.designation import Designation
from master.models.state import State
from utils.basemodel import BaseModel
from utils.image_utils import generate_image_path, delete_old_image_on_save, register_image_delete_signal
from utils.enums import EmployeeType, EmployeeBadge


def image_path(instance, filename):    
    return generate_image_path(instance, filename, 'employees_photos', 'id')


class EmployeeProfile(BaseModel):        
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees_branch')    
    gender = models.CharField(max_length=1, blank=True, null=True)
    nationality = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees_nationality')
    marital_status = models.BooleanField(default=False)
    address = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees_country')
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees_state')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees_city')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees_department')
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees_designation')
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees_manager')
    hire_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    employee_type = models.CharField(max_length=10, choices=EmployeeType.choices, default=EmployeeType.FULL)
    photo = models.ImageField(upload_to=image_path, max_length=200, default="na.png")
    is_training_completed = models.BooleanField(default=False)
    willing_to_travel = models.BooleanField(default=False)
    badge = models.CharField(max_length=10, choices=EmployeeBadge.choices, default=EmployeeBadge.SILVER)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = '"hr"."employees"'
        indexes = [            
            models.Index(fields=['nationality']),
            models.Index(fields=['country', 'state', 'city']),
            models.Index(fields=['department', 'designation']),
            models.Index(fields=['department']),
            models.Index(fields=['designation']),
            models.Index(fields=['manager']),            
        ]

    def save(self, *args, **kwargs):
        delete_old_image_on_save(self, 'photo')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name}"



# Register the image delete signal for the Employee model
register_image_delete_signal(Employee, 'photo')
