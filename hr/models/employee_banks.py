# hr/models/employee_banks.py

from django.db import models
from authuser.models.employee import Employee
from master.models.bank import Bank
from master.models.country import Country
from utils.basemodel import BaseModel


class EmployeeBanks(BaseModel):        
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name='banks')
    bank_country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, related_name='employee_bank_country')
    bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees_banks')
    bank_ac_no = models.CharField(max_length=24, blank=True, null=True)
    bank_ac_IFSC = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        db_table = '"hr"."employee_banks"'
        indexes = [
            models.Index(fields=['bank_country', 'bank']),
        ]

    def __str__(self):
        return f"Bank Info for {self.employee.first_name} {self.employee.last_name}"
