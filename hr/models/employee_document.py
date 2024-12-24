# hr/models/employee_document.py

from django.db import models
from authuser.models.employee import Employee
from utils.basemodel import BaseModel
from utils.image_utils import generate_image_path, delete_old_image_on_save, register_image_delete_signal


def image_path(instance, filename):    
    return generate_image_path(instance, filename, 'employees_documents', 'id')


class EmployeeDocument(BaseModel):    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name='documents')
    document_type = models.ForeignKey('master.DocumentType', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees_document_type')
    document = models.ForeignKey('master.Document', on_delete=models.SET_NULL, null=True, blank=True, related_name='employee_documents')
    document_number = models.CharField(max_length=24, blank=True, null=True)
    document_image = models.ImageField(upload_to=image_path, max_length=200, default="na.png")
    issue_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    issue_country = models.ForeignKey('master.Country', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees_document_issue_country')
    issue_state = models.ForeignKey('master.State', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees_document_issue_state')
    issue_city = models.ForeignKey('master.City', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees_document_issue_city')

    class Meta:
        db_table = '"hr"."employee_documents"'
        indexes = [
            models.Index(fields=['employee', 'document_type']),
        ]

    def save(self, *args, **kwargs):
        delete_old_image_on_save(self, 'document_image')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.id} - {self.document_type} - {self.document_number}"


# Register the image delete signal for the EmployeeDocument model
register_image_delete_signal(EmployeeDocument, 'document_image')
