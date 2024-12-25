
# hr/views/employee_contact.py

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from authuser.permissions import IsEmployee
from hr.models.employee_contact import EmployeeContact
from hr.serializers import EmployeeContactSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List Employee Contacts",
        description="Retrieve a list of all employee contacts.",
        responses={
            200: OpenApiResponse(
                response=EmployeeContactSerializer(many=True),
                description="A list of employee contacts."
            )
        },
        tags=["Employee Contact"],
        examples=[
            OpenApiExample(
                name="Employee Contact List Response",
                summary="Successful retrieval of employee contact list",
                description="Returns a list of all employee contacts with their details.",
                value=[
                    {
                        "id": 1,
                        "employee": 1,
                        "employee_name": "John Doe",
                        "name": "Jane Doe",
                        "contact_type": "PERSONAL",
                        "relationship": "SPOUSE",
                        "contact_number": 1122334455,
                        "email": "janedoe@example.com",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-08-10T09:00:00Z",
                        "last_update_date": "2024-09-10T10:10:00Z",
                        "updated_by": None
                    },
                    # ... more employee contacts
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Employee Contact Details",
        description="Retrieve detailed information about a specific employee contact by its ID.",
        responses={
            200: OpenApiResponse(
                response=EmployeeContactSerializer,
                description="Detailed information about the employee contact."
            ),
            404: OpenApiResponse(description="Employee contact not found.")
        },
        tags=["Employee Contact"],
        examples=[
            OpenApiExample(
                name="Employee Contact Detail Response",
                summary="Successful retrieval of employee contact details",
                description="Returns detailed information about a specific employee contact.",
                value={
                    "id": 1,
                    "employee": 1,
                    "employee_name": "John Doe",
                    "name": "Jane Doe",
                    "contact_type": "PERSONAL",
                    "relationship": "SPOUSE",
                    "contact_number": 1122334455,
                    "email": "janedoe@example.com",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-08-10T09:00:00Z",
                    "last_update_date": "2024-09-10T10:10:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Employee Contact",
        description="Add a new employee contact to the system by providing necessary details.",
        request=EmployeeContactSerializer,
        responses={
            201: OpenApiResponse(
                response=EmployeeContactSerializer,
                description="Employee contact created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Employee Contact"],
        examples=[
            OpenApiExample(
                name="Employee Contact Creation Request",
                summary="Request body for creating a new employee contact",
                description="Provide necessary fields to create a new employee contact.",
                value={
                    "employee": 2,
                    "name": "Robert Smith",
                    "contact_type": "WORK",
                    "relationship": "COLLEAGUE",
                    "contact_number": 2233445566,
                    "email": "robertsmith@example.com",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Employee Contact Creation Success Response",
                summary="Successful employee contact creation",
                description="Returns the created employee contact details.",
                value={
                    "id": 2,
                    "employee": 2,
                    "employee_name": "Alice Smith",
                    "name": "Robert Smith",
                    "contact_type": "WORK",
                    "relationship": "COLLEAGUE",
                    "contact_number": 2233445566,
                    "email": "robertsmith@example.com",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-09-11T14:00:00Z",
                    "last_update_date": "2024-09-11T14:00:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Employee Contact Details",
        description="Update information of an existing employee contact by its ID.",
        request=EmployeeContactSerializer,
        responses={
            200: OpenApiResponse(
                response=EmployeeContactSerializer,
                description="Employee contact updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Employee contact not found.")
        },
        tags=["Employee Contact"],
        examples=[
            OpenApiExample(
                name="Employee Contact Update Request",
                summary="Request body for updating an employee contact",
                description="Provide fields to update for the employee contact.",
                value={
                    "relationship": "FRIEND",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Employee Contact Update Success Response",
                summary="Successful employee contact update",
                description="Returns the updated employee contact details.",
                value={
                    "id": 1,
                    "employee": 1,
                    "employee_name": "John Doe",
                    "name": "Jane Doe",
                    "contact_type": "PERSONAL",
                    "relationship": "FRIEND",
                    "contact_number": 1122334455,
                    "email": "janedoe@example.com",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-08-10T09:00:00Z",
                    "last_update_date": "2024-09-12T16:20:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete an Employee Contact",
        description="Remove an employee contact from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Employee contact deleted successfully."),
            404: OpenApiResponse(description="Employee contact not found.")
        },
        tags=["Employee Contact"],
        examples=[
            OpenApiExample(
                name="Employee Contact Deletion Success Response",
                summary="Successful employee contact deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class EmployeeContactViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing employee contact instances.
    """
    queryset = EmployeeContact.objects.select_related('employee').all()
    serializer_class = EmployeeContactSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'contact_type', 'relationship', 'status', 'is_active']
    search_fields = ['name', 'email', 'contact_number']
    ordering_fields = ['name', 'contact_type', 'relationship', 'status', 'is_active']
    ordering = ['name']
    permission_classes = [IsAuthenticated, IsEmployee]