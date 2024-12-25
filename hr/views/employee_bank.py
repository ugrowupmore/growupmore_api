
# hr/views/employee_bank.py

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
from hr.models.employee_banks import EmployeeBanks
from hr.serializers import EmployeeBanksSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List Employee Banks",
        description="Retrieve a list of all employee bank accounts.",
        responses={
            200: OpenApiResponse(
                response=EmployeeBanksSerializer(many=True),
                description="A list of employee bank accounts."
            )
        },
        tags=["Employee Bank"],
        examples=[
            OpenApiExample(
                name="Employee Bank List Response",
                summary="Successful retrieval of employee bank list",
                description="Returns a list of all employee bank accounts with their details.",
                value=[
                    {
                        "id": 1,
                        "employee": 1,
                        "employee_name": "John Doe",
                        "bank_country": 1,
                        "bank_country_name": "Countryland",
                        "bank": 3,
                        "bank_name": "Country Bank",
                        "bank_ac_no": "123456789012",
                        "bank_ac_IFSC": "CBIN0001234",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-08-20T10:00:00Z",
                        "last_update_date": "2024-09-20T11:10:00Z",
                        "updated_by": None
                    },
                    # ... more employee banks
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Employee Bank Details",
        description="Retrieve detailed information about a specific employee bank account by its ID.",
        responses={
            200: OpenApiResponse(
                response=EmployeeBanksSerializer,
                description="Detailed information about the employee bank account."
            ),
            404: OpenApiResponse(description="Employee bank account not found.")
        },
        tags=["Employee Bank"],
        examples=[
            OpenApiExample(
                name="Employee Bank Detail Response",
                summary="Successful retrieval of employee bank details",
                description="Returns detailed information about a specific employee bank account.",
                value={
                    "id": 1,
                    "employee": 1,
                    "employee_name": "John Doe",
                    "bank_country": 1,
                    "bank_country_name": "Countryland",
                    "bank": 3,
                    "bank_name": "Country Bank",
                    "bank_ac_no": "123456789012",
                    "bank_ac_IFSC": "CBIN0001234",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-08-20T10:00:00Z",
                    "last_update_date": "2024-09-20T11:10:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Employee Bank Account",
        description="Add a new employee bank account to the system by providing necessary details.",
        request=EmployeeBanksSerializer,
        responses={
            201: OpenApiResponse(
                response=EmployeeBanksSerializer,
                description="Employee bank account created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Employee Bank"],
        examples=[
            OpenApiExample(
                name="Employee Bank Creation Request",
                summary="Request body for creating a new employee bank account",
                description="Provide necessary fields to create a new employee bank account.",
                value={
                    "employee": 2,
                    "bank_country": 1,
                    "bank": 4,
                    "bank_ac_no": "987654321098",
                    "bank_ac_IFSC": "CBIN0005678",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Employee Bank Creation Success Response",
                summary="Successful employee bank account creation",
                description="Returns the created employee bank account details.",
                value={
                    "id": 2,
                    "employee": 2,
                    "employee_name": "Alice Smith",
                    "bank_country": 1,
                    "bank_country_name": "Countryland",
                    "bank": 4,
                    "bank_name": "National Bank",
                    "bank_ac_no": "987654321098",
                    "bank_ac_IFSC": "CBIN0005678",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-09-21T14:30:00Z",
                    "last_update_date": "2024-09-21T14:30:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Employee Bank Account Details",
        description="Update information of an existing employee bank account by its ID.",
        request=EmployeeBanksSerializer,
        responses={
            200: OpenApiResponse(
                response=EmployeeBanksSerializer,
                description="Employee bank account updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Employee bank account not found.")
        },
        tags=["Employee Bank"],
        examples=[
            OpenApiExample(
                name="Employee Bank Update Request",
                summary="Request body for updating an employee bank account",
                description="Provide fields to update for the employee bank account.",
                value={
                    "bank_ac_IFSC": "CBIN0009101",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Employee Bank Update Success Response",
                summary="Successful employee bank account update",
                description="Returns the updated employee bank account details.",
                value={
                    "id": 1,
                    "employee": 1,
                    "employee_name": "John Doe",
                    "bank_country": 1,
                    "bank_country_name": "Countryland",
                    "bank": 3,
                    "bank_name": "Country Bank",
                    "bank_ac_no": "123456789012",
                    "bank_ac_IFSC": "CBIN0009101",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-08-20T10:00:00Z",
                    "last_update_date": "2024-09-22T16:20:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete an Employee Bank Account",
        description="Remove an employee bank account from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Employee bank account deleted successfully."),
            404: OpenApiResponse(description="Employee bank account not found.")
        },
        tags=["Employee Bank"],
        examples=[
            OpenApiExample(
                name="Employee Bank Deletion Success Response",
                summary="Successful employee bank account deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class EmployeeBanksViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing employee bank account instances.
    """
    queryset = EmployeeBanks.objects.select_related(
        'employee',
        'bank',
        'bank_country'
    ).all()
    serializer_class = EmployeeBanksSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'bank', 'bank_country', 'status', 'is_active']
    search_fields = ['bank_ac_no', 'bank_ac_IFSC']
    ordering_fields = ['bank_ac_no', 'bank', 'bank_country', 'status', 'is_active']
    ordering = ['bank_ac_no']
    permission_classes = [IsAuthenticated, IsEmployee]