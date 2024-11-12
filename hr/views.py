from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from hr.models.branch import Branch
from hr.models.branch_department import BranchDepartment
from hr.models.branch_document import BranchDocument
from hr.models.branch_photo import BranchPhoto
from hr.models.employee import Employee
from hr.models.employee_banks import EmployeeBanks
from hr.models.employee_contact import EmployeeContact
from hr.models.employee_document import EmployeeDocument
from utils.pagination import KendoPagination

from .serializers import (
    EmployeeSerializer, EmployeeContactSerializer, EmployeeDocumentSerializer, EmployeeBanksSerializer,
    BranchSerializer, BranchDepartmentSerializer, BranchDocumentSerializer, BranchPhotoSerializer
)


# Branch ViewSet
class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.select_related(
        'branch_type',
        'manager',
        'country',
        'state',
        'city',
        'reports_to'
    ).all()
    serializer_class = BranchSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['branch_type', 'manager', 'country', 'state', 'city', 'status', 'is_active']
    search_fields = ['name', 'code']
    ordering_fields = '__all__'
    ordering = ['code']


# BranchDepartment ViewSet
class BranchDepartmentViewSet(viewsets.ModelViewSet):
    queryset = BranchDepartment.objects.select_related(
        'branch',
        'department',
        'manager',
        'country',
        'state',
        'city'
    ).all()
    serializer_class = BranchDepartmentSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['branch', 'department', 'manager', 'country', 'state', 'city', 'status', 'is_active']
    search_fields = ['code']
    ordering_fields = '__all__'
    ordering = ['code']


# BranchDocument ViewSet
class BranchDocumentViewSet(viewsets.ModelViewSet):
    queryset = BranchDocument.objects.select_related(
        'branch',
        'document_type',
        'document',
        'issue_country',
        'issue_state',
        'issue_city'
    ).all()
    serializer_class = BranchDocumentSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['branch', 'document_type', 'issue_country', 'issue_state', 'issue_city', 'status', 'is_active']
    search_fields = ['document_number']
    ordering_fields = '__all__'
    ordering = ['document_number']


# BranchPhoto ViewSet
class BranchPhotoViewSet(viewsets.ModelViewSet):
    queryset = BranchPhoto.objects.select_related('branch').all()
    serializer_class = BranchPhotoSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['branch', 'status', 'is_active']
    search_fields = ['title']
    ordering_fields = '__all__'
    ordering = ['title']


# Employee ViewSet
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related(
        'nationality',
        'country',
        'state',
        'city',
        'department',
        'designation',
        'manager'
    ).all()
    serializer_class = EmployeeSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'first_name', 'last_name', 'gender', 'nationality',
        'marital_status', 'country', 'state', 'city',
        'department', 'designation', 'manager',
        'hire_date', 'end_date', 'employee_type',
        'is_training_completed', 'willing_to_travel',
        'badge', 'status', 'is_active'
    ]
    search_fields = ['first_name', 'last_name']
    ordering_fields = '__all__'
    ordering = ['first_name']


# Employee Contacts ViewSet
class EmployeeContactViewSet(viewsets.ModelViewSet):
    queryset = EmployeeContact.objects.select_related('employee').all()
    serializer_class = EmployeeContactSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'contact_type']
    search_fields = ['name']
    ordering_fields = '__all__'
    ordering = ['name']


# Employee Documents ViewSet
class EmployeeDocumentViewSet(viewsets.ModelViewSet):
    queryset = EmployeeDocument.objects.select_related(
        'employee',
        'document_type',
        'document',
        'issue_country',
        'issue_state',
        'issue_city'
    ).all()
    serializer_class = EmployeeDocumentSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'document_type', 'issue_country', 'issue_state', 'issue_city', 'status', 'is_active']
    search_fields = ['document_number']
    ordering_fields = '__all__'
    ordering = ['document_number']


# Employee Banks ViewSet
class EmployeeBanksViewSet(viewsets.ModelViewSet):
    queryset = EmployeeBanks.objects.select_related(
        'employee',
        'bank',
        'bank_country'
    ).all()
    serializer_class = EmployeeBanksSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'bank', 'bank_country']
    search_fields = ['bank_ac_no']
    ordering_fields = '__all__'
    ordering = ['bank_ac_no']
