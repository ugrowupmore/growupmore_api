
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
from hr.models.employee_document import EmployeeDocument
from hr.serializers import EmployeeDocumentSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List Employee Documents",
        description="Retrieve a list of all employee documents.",
        responses={
            200: OpenApiResponse(
                response=EmployeeDocumentSerializer(many=True),
                description="A list of employee documents."
            )
        },
        tags=["Employee Document"],
        examples=[
            OpenApiExample(
                name="Employee Document List Response",
                summary="Successful retrieval of employee document list",
                description="Returns a list of all employee documents with their details.",
                value=[
                    {
                        "id": 1,
                        "employee": 1,
                        "employee_name": "John Doe",
                        "document_type": 2,
                        "document_type_name": "Passport",
                        "document": 5,
                        "document_name": "International Passport",
                        "document_number": "P123456789",
                        "document_image": "http://localhost:8000/media/employees_documents/jdoe_passport.png",
                        "issue_date": "2018-06-15",
                        "expiry_date": "2028-06-14",
                        "issue_country": 1,
                        "issue_country_name": "Countryland",
                        "issue_state": 5,
                        "issue_state_name": "Stateland",
                        "issue_city": 10,
                        "issue_city_name": "Cityville",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-08-15T10:00:00Z",
                        "last_update_date": "2024-09-15T11:10:00Z",
                        "updated_by": None
                    },
                    # ... more employee documents
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Employee Document Details",
        description="Retrieve detailed information about a specific employee document by its ID.",
        responses={
            200: OpenApiResponse(
                response=EmployeeDocumentSerializer,
                description="Detailed information about the employee document."
            ),
            404: OpenApiResponse(description="Employee document not found.")
        },
        tags=["Employee Document"],
        examples=[
            OpenApiExample(
                name="Employee Document Detail Response",
                summary="Successful retrieval of employee document details",
                description="Returns detailed information about a specific employee document.",
                value={
                    "id": 1,
                    "employee": 1,
                    "employee_name": "John Doe",
                    "document_type": 2,
                    "document_type_name": "Passport",
                    "document": 5,
                    "document_name": "International Passport",
                    "document_number": "P123456789",
                    "document_image": "http://localhost:8000/media/employees_documents/jdoe_passport.png",
                    "issue_date": "2018-06-15",
                    "expiry_date": "2028-06-14",
                    "issue_country": 1,
                    "issue_country_name": "Countryland",
                    "issue_state": 5,
                    "issue_state_name": "Stateland",
                    "issue_city": 10,
                    "issue_city_name": "Cityville",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-08-15T10:00:00Z",
                    "last_update_date": "2024-09-15T11:10:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Employee Document",
        description="Add a new employee document to the system by providing necessary details.",
        request=EmployeeDocumentSerializer,
        responses={
            201: OpenApiResponse(
                response=EmployeeDocumentSerializer,
                description="Employee document created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Employee Document"],
        examples=[
            OpenApiExample(
                name="Employee Document Creation Request",
                summary="Request body for creating a new employee document",
                description="Provide necessary fields to create a new employee document.",
                value={
                    "employee": 2,
                    "document_type": 3,
                    "document": 6,
                    "document_number": "ID987654321",
                    "document_image": "http://localhost:8000/media/employees_documents/asmith_id.png",
                    "issue_date": "2022-03-20",
                    "expiry_date": "2032-03-19",
                    "issue_country": 1,
                    "issue_state": 5,
                    "issue_city": 12,
                    "description": "National ID for Alice Smith.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Employee Document Creation Success Response",
                summary="Successful employee document creation",
                description="Returns the created employee document details.",
                value={
                    "id": 2,
                    "employee": 2,
                    "employee_name": "Alice Smith",
                    "document_type": 3,
                    "document_type_name": "National ID",
                    "document": 6,
                    "document_name": "Government Issued ID",
                    "document_number": "ID987654321",
                    "document_image": "http://localhost:8000/media/employees_documents/asmith_id.png",
                    "issue_date": "2022-03-20",
                    "expiry_date": "2032-03-19",
                    "issue_country": 1,
                    "issue_country_name": "Countryland",
                    "issue_state": 5,
                    "issue_state_name": "Stateland",
                    "issue_city": 12,
                    "issue_city_name": "Uptown City",
                    "description": "National ID for Alice Smith.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-09-12T14:30:00Z",
                    "last_update_date": "2024-09-12T14:30:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Employee Document Details",
        description="Update information of an existing employee document by its ID.",
        request=EmployeeDocumentSerializer,
        responses={
            200: OpenApiResponse(
                response=EmployeeDocumentSerializer,
                description="Employee document updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Employee document not found.")
        },
        tags=["Employee Document"],
        examples=[
            OpenApiExample(
                name="Employee Document Update Request",
                summary="Request body for updating an employee document",
                description="Provide fields to update for the employee document.",
                value={
                    "description": "Updated description for Passport.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Employee Document Update Success Response",
                summary="Successful employee document update",
                description="Returns the updated employee document details.",
                value={
                    "id": 1,
                    "employee": 1,
                    "employee_name": "John Doe",
                    "document_type": 2,
                    "document_type_name": "Passport",
                    "document": 5,
                    "document_name": "International Passport",
                    "document_number": "P123456789",
                    "document_image": "http://localhost:8000/media/employees_documents/jdoe_passport.png",
                    "issue_date": "2018-06-15",
                    "expiry_date": "2028-06-14",
                    "issue_country": 1,
                    "issue_country_name": "Countryland",
                    "issue_state": 5,
                    "issue_state_name": "Stateland",
                    "issue_city": 10,
                    "issue_city_name": "Cityville",
                    "description": "Updated description for Passport.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-08-15T10:00:00Z",
                    "last_update_date": "2024-09-13T16:20:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete an Employee Document",
        description="Remove an employee document from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Employee document deleted successfully."),
            404: OpenApiResponse(description="Employee document not found.")
        },
        tags=["Employee Document"],
        examples=[
            OpenApiExample(
                name="Employee Document Deletion Success Response",
                summary="Successful employee document deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class EmployeeDocumentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing employee document instances.
    """
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
    filterset_fields = [
        'employee', 'document_type', 'issue_country', 
        'issue_state', 'issue_city', 'status', 'is_active'
    ]
    search_fields = ['document_number', 'document_name']
    ordering_fields = ['document_number', 'employee', 'document_type', 'status', 'is_active']
    ordering = ['document_number']
    permission_classes = [IsAuthenticated, IsEmployee]