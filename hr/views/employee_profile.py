
# hr/views/employee_profile.py

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from authuser.models.employee import Employee
from authuser.permissions import IsEmployee
from hr.serializers import EmployeeDetailSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List Employees",
        description="Retrieve a list of all employees.",
        responses={
            200: OpenApiResponse(
                response=EmployeeDetailSerializer(many=True),
                description="A list of employees."
            )
        },
        tags=["Employee"],
        examples=[
            OpenApiExample(
                name="Employee List Response",
                summary="Successful retrieval of employee list",
                description="Returns a list of all employees with their detailed profiles.",
                value=[
                    {
                        "id": 1,
                        "username": "jdoe",
                        "email": "jdoe@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "is_active": True,
                        "is_staff": False,
                        "is_superuser": False,
                        "profile": {
                            "employee": 1,
                            "branch": 1,
                            "branch_name": "Downtown Branch",
                            "gender": "M",
                            "nationality": 1,
                            "nationality_name": "Countryland",
                            "marital_status": False,
                            "address": "123 Main St, Cityville",
                            "country": 1,
                            "country_name": "Countryland",
                            "state": 5,
                            "state_name": "Stateland",
                            "city": 10,
                            "city_name": "Cityville",
                            "zipcode": "12345",
                            "department": 3,
                            "department_name": "Sales",
                            "designation": 4,
                            "designation_name": "Sales Manager",
                            "manager": 2,
                            "manager_name": "Jane Smith",
                            "hire_date": "2020-05-15",
                            "end_date": None,
                            "salary": "75000.00",
                            "employee_type": "FULL",
                            "photo": "http://localhost:8000/media/employees_photos/jdoe.png",
                            "is_training_completed": True,
                            "willing_to_travel": False,
                            "badge": "GOLD",
                            "description": "Senior Sales Manager with 5 years of experience.",
                            "status": "ACTIVE",
                            "is_active": True,
                            "create_date": "2020-05-15T09:00:00Z",
                            "last_update_date": "2023-10-01T12:00:00Z",
                            "updated_by": None
                        }
                    },
                    # ... more employees
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Employee Details",
        description="Retrieve detailed information about a specific employee by their ID.",
        responses={
            200: OpenApiResponse(
                response=EmployeeDetailSerializer,
                description="Detailed information about the employee."
            ),
            404: OpenApiResponse(description="Employee not found.")
        },
        tags=["Employee"],
        examples=[
            OpenApiExample(
                name="Employee Detail Response",
                summary="Successful retrieval of employee details",
                description="Returns detailed information about a specific employee.",
                value={
                    "id": 1,
                    "username": "jdoe",
                    "email": "jdoe@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "is_active": True,
                    "is_staff": False,
                    "is_superuser": False,
                    "profile": {
                        "employee": 1,
                        "branch": 1,
                        "branch_name": "Downtown Branch",
                        "gender": "M",
                        "nationality": 1,
                        "nationality_name": "Countryland",
                        "marital_status": False,
                        "address": "123 Main St, Cityville",
                        "country": 1,
                        "country_name": "Countryland",
                        "state": 5,
                        "state_name": "Stateland",
                        "city": 10,
                        "city_name": "Cityville",
                        "zipcode": "12345",
                        "department": 3,
                        "department_name": "Sales",
                        "designation": 4,
                        "designation_name": "Sales Manager",
                        "manager": 2,
                        "manager_name": "Jane Smith",
                        "hire_date": "2020-05-15",
                        "end_date": None,
                        "salary": "75000.00",
                        "employee_type": "FULL",
                        "photo": "http://localhost:8000/media/employees_photos/jdoe.png",
                        "is_training_completed": True,
                        "willing_to_travel": False,
                        "badge": "GOLD",
                        "description": "Senior Sales Manager with 5 years of experience.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2020-05-15T09:00:00Z",
                        "last_update_date": "2023-10-01T12:00:00Z",
                        "updated_by": None
                    }
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Employee",
        description="Add a new employee to the system by providing necessary details.",
        request=EmployeeDetailSerializer,
        responses={
            201: OpenApiResponse(
                response=EmployeeDetailSerializer,
                description="Employee created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Employee"],
        examples=[
            OpenApiExample(
                name="Employee Creation Request",
                summary="Request body for creating a new employee",
                description="Provide necessary fields to create a new employee.",
                value={
                    "username": "asmith",
                    "email": "asmith@example.com",
                    "first_name": "Alice",
                    "last_name": "Smith",
                    "profile": {
                        "branch": 2,
                        "gender": "F",
                        "nationality": 1,
                        "marital_status": True,
                        "address": "456 Uptown Ave, Cityville",
                        "country": 1,
                        "state": 5,
                        "city": 12,
                        "zipcode": "67890",
                        "department": 4,
                        "designation": 5,
                        "manager": 1,
                        "hire_date": "2023-01-10",
                        "end_date": None,
                        "salary": "65000.00",
                        "employee_type": "PART",
                        "photo": "http://localhost:8000/media/employees_photos/asmith.png",
                        "is_training_completed": False,
                        "willing_to_travel": True,
                        "badge": "SILVER",
                        "description": "Junior Sales Representative.",
                        "status": "ACTIVE",
                        "is_active": True
                    }
                }
            ),
            OpenApiExample(
                name="Employee Creation Success Response",
                summary="Successful employee creation",
                description="Returns the created employee details.",
                value={
                    "id": 2,
                    "username": "asmith",
                    "email": "asmith@example.com",
                    "first_name": "Alice",
                    "last_name": "Smith",
                    "is_active": True,
                    "is_staff": False,
                    "is_superuser": False,
                    "profile": {
                        "employee": 2,
                        "branch": 2,
                        "branch_name": "Uptown Branch",
                        "gender": "F",
                        "nationality": 1,
                        "nationality_name": "Countryland",
                        "marital_status": True,
                        "address": "456 Uptown Ave, Cityville",
                        "country": 1,
                        "country_name": "Countryland",
                        "state": 5,
                        "state_name": "Stateland",
                        "city": 12,
                        "city_name": "Uptown City",
                        "zipcode": "67890",
                        "department": 4,
                        "department_name": "Human Resources",
                        "designation": 5,
                        "designation_name": "HR Coordinator",
                        "manager": 1,
                        "manager_name": "John Doe",
                        "hire_date": "2023-01-10",
                        "end_date": None,
                        "salary": "65000.00",
                        "employee_type": "PART",
                        "photo": "http://localhost:8000/media/employees_photos/asmith.png",
                        "is_training_completed": False,
                        "willing_to_travel": True,
                        "badge": "SILVER",
                        "description": "Junior Sales Representative.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2023-01-10T08:30:00Z",
                        "last_update_date": "2023-01-10T08:30:00Z",
                        "updated_by": None
                    }
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Employee Details",
        description="Update information of an existing employee by their ID.",
        request=EmployeeDetailSerializer,
        responses={
            200: OpenApiResponse(
                response=EmployeeDetailSerializer,
                description="Employee updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Employee not found.")
        },
        tags=["Employee"],
        examples=[
            OpenApiExample(
                name="Employee Update Request",
                summary="Request body for updating an employee",
                description="Provide fields to update for the employee.",
                value={
                    "profile": {
                        "description": "Updated description for Sales Manager.",
                        "is_active": False
                    }
                }
            ),
            OpenApiExample(
                name="Employee Update Success Response",
                summary="Successful employee update",
                description="Returns the updated employee details.",
                value={
                    "id": 1,
                    "username": "jdoe",
                    "email": "jdoe@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "is_active": True,
                    "is_staff": False,
                    "is_superuser": False,
                    "profile": {
                        "employee": 1,
                        "branch": 1,
                        "branch_name": "Downtown Branch",
                        "gender": "M",
                        "nationality": 1,
                        "nationality_name": "Countryland",
                        "marital_status": False,
                        "address": "123 Main St, Cityville",
                        "country": 1,
                        "country_name": "Countryland",
                        "state": 5,
                        "state_name": "Stateland",
                        "city": 10,
                        "city_name": "Cityville",
                        "zipcode": "12345",
                        "department": 3,
                        "department_name": "Sales",
                        "designation": 4,
                        "designation_name": "Sales Manager",
                        "manager": 2,
                        "manager_name": "Jane Smith",
                        "hire_date": "2020-05-15",
                        "end_date": None,
                        "salary": "75000.00",
                        "employee_type": "FULL",
                        "photo": "http://localhost:8000/media/employees_photos/jdoe.png",
                        "is_training_completed": True,
                        "willing_to_travel": False,
                        "badge": "GOLD",
                        "description": "Updated description for Sales Manager.",
                        "status": "ACTIVE",
                        "is_active": False,
                        "create_date": "2020-05-15T09:00:00Z",
                        "last_update_date": "2024-09-10T16:20:00Z",
                        "updated_by": 1
                    }
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete an Employee",
        description="Remove an employee from the system by their ID.",
        responses={
            204: OpenApiResponse(description="Employee deleted successfully."),
            404: OpenApiResponse(description="Employee not found.")
        },
        tags=["Employee"],
        examples=[
            OpenApiExample(
                name="Employee Deletion Success Response",
                summary="Successful employee deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class EmployeeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing employee instances.
    """
    queryset = Employee.objects.select_related(
        'profile__nationality',
        'profile__country',
        'profile__state',
        'profile__city',
        'profile__department',
        'profile__designation',
        'profile__manager'
    ).all()
    serializer_class = EmployeeDetailSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'first_name', 'last_name', 'profile__gender', 'profile__nationality',
        'profile__marital_status', 'profile__country', 'profile__state', 'profile__city',
        'profile__department', 'profile__designation', 'profile__manager',
        'profile__hire_date', 'profile__end_date', 'profile__employee_type',
        'profile__is_training_completed', 'profile__willing_to_travel',
        'profile__badge', 'status', 'is_active'
    ]
    search_fields = ['first_name', 'last_name', 'username', 'email']
    ordering_fields = ['first_name', 'last_name', 'username', 'email', 'profile__hire_date', 'profile__salary']
    ordering = ['first_name']
    permission_classes = [IsAuthenticated, IsEmployee]