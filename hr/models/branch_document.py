# hr/models/branch_document.py

from django.db import models
from hr.models.branch import Branch
from master.models.city import City
from master.models.country import Country
from master.models.document import Document
from master.models.document_type import DocumentType
from master.models.state import State
from utils.basemodel import BaseModel


class BranchDocument(BaseModel):
    id = models.AutoField(primary_key=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    document_type = models.ForeignKey(DocumentType, on_delete=models.SET_NULL, null=True, blank=True, related_name='branch_document_type')
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name='branch_documents')
    document_number = models.CharField(max_length=50, blank=True, null=True)
    issue_date = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    issue_country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, related_name='branch_documents_issue_country')
    issue_state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True, related_name='branch_documents_issue_state')
    issue_city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='branch_documents_issue_city')
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = '"hr"."branch_documents"'
        indexes = [
            models.Index(fields=['branch']),
            models.Index(fields=['document_type']),
            models.Index(fields=['issue_country', 'issue_state', 'issue_city']),
            models.Index(fields=['status', 'is_active']),
        ]

    def __str__(self):
        return f"Document {self.document_number} for {self.branch.name}"
