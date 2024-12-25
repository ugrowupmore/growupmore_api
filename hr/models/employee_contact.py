# hr/models/employee_contact.py

from django.db import models
from authuser.models.employee import Employee
from utils.basemodel import BaseModel
from utils.enums import ContactType, Relationship


class EmployeeContact(BaseModel):    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name='contacts')
    name = models.CharField(max_length=40, blank=True, null=True)
    contact_type = models.CharField(max_length=10, choices=ContactType.choices, default=ContactType.PERSONAL)
    relationship = models.CharField(max_length=10, choices=Relationship.choices, default=Relationship.SELF)
    contact_number = models.BigIntegerField(default=0)
    email = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        db_table = '"hr"."employee_contacts"'
        indexes = [
            models.Index(fields=['employee', 'contact_type']),
        ]        

    def __str__(self):
        return f"{self.employee.id} - {self.name} - {self.contact_type} - {self.contact_number}"
