
# hr/views/branch_department.py

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
from hr.models.branch_department import BranchDepartment
from hr.serializers import BranchDepartmentSerializer

@extend_schema_view(
    list=extend_schema(
        summary="List Branch Departments",
        description="Retrieve a list of all branch departments.",
        responses={
            200: OpenApiResponse(
                response=BranchDepartmentSerializer(many=True),
                description="A list of branch departments."
            )
        },
        tags=["Branch Department"],
        examples=[
            OpenApiExample(
                name="Branch Department List Response",
                summary="Successful retrieval of branch department list",
                description="Returns a list of all branch departments with their details.",
                value=[
                    {
                        "id": 1,
                        "branch": 1,
                        "branch_name": "Downtown Branch",
                        "department": 3,
                        "department_name": "Sales",
                        "manager": 2,
                        "manager_name": "Jane Smith",
                        "code": "SLS001",
                        "address": "123 Main St, Cityville",
                        "country": 1,
                        "country_name": "Countryland",
                        "state": 5,
                        "state_name": "Stateland",
                        "city": 10,
                        "city_name": "Cityville",
                        "zipcode": "12345",
                        "contact1": 1234567890,
                        "contact2": 9876543210,
                        "latitude": "40.712776",
                        "longitude": "-74.005974",
                        "opening_hour": "09:00:00",
                        "closing_hour": "17:00:00",
                        "establishment_year": 2005,
                        "description": "Handles all sales-related activities.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-07-26T11:00:00Z",
                        "last_update_date": "2024-08-26T12:10:00Z",
                        "updated_by": None
                    },
                    # ... more branch departments
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Branch Department Details",
        description="Retrieve detailed information about a specific branch department by its ID.",
        responses={
            200: OpenApiResponse(
                response=BranchDepartmentSerializer,
                description="Detailed information about the branch department."
            ),
            404: OpenApiResponse(description="Branch department not found.")
        },
        tags=["Branch Department"],
        examples=[
            OpenApiExample(
                name="Branch Department Detail Response",
                summary="Successful retrieval of branch department details",
                description="Returns detailed information about a specific branch department.",
                value={
                    "id": 1,
                    "branch": 1,
                    "branch_name": "Downtown Branch",
                    "department": 3,
                    "department_name": "Sales",
                    "manager": 2,
                    "manager_name": "Jane Smith",
                    "code": "SLS001",
                    "address": "123 Main St, Cityville",
                    "country": 1,
                    "country_name": "Countryland",
                    "state": 5,
                    "state_name": "Stateland",
                    "city": 10,
                    "city_name": "Cityville",
                    "zipcode": "12345",
                    "contact1": 1234567890,
                    "contact2": 9876543210,
                    "latitude": "40.712776",
                    "longitude": "-74.005974",
                    "opening_hour": "09:00:00",
                    "closing_hour": "17:00:00",
                    "establishment_year": 2005,
                    "description": "Handles all sales-related activities.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-26T11:00:00Z",
                    "last_update_date": "2024-08-26T12:10:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Branch Department",
        description="Add a new branch department to the system by providing necessary details.",
        request=BranchDepartmentSerializer,
        responses={
            201: OpenApiResponse(
                response=BranchDepartmentSerializer,
                description="Branch department created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Branch Department"],
        examples=[
            OpenApiExample(
                name="Branch Department Creation Request",
                summary="Request body for creating a new branch department",
                description="Provide necessary fields to create a new branch department.",
                value={
                    "branch": 2,
                    "department": 4,
                    "manager": 3,
                    "code": "HR002",
                    "address": "456 Uptown Ave, Cityville",
                    "country": 1,
                    "state": 5,
                    "city": 12,
                    "zipcode": "67890",
                    "contact1": 1122334455,
                    "contact2": 5544332211,
                    "latitude": "40.730610",
                    "longitude": "-73.935242",
                    "opening_hour": "10:00:00",
                    "closing_hour": "18:00:00",
                    "establishment_year": 2012,
                    "description": "Handles all human resources activities.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Branch Department Creation Success Response",
                summary="Successful branch department creation",
                description="Returns the created branch department details.",
                value={
                    "id": 2,
                    "branch": 2,
                    "branch_name": "Uptown Branch",
                    "department": 4,
                    "department_name": "Human Resources",
                    "manager": 3,
                    "manager_name": "Bob Johnson",
                    "code": "HR002",
                    "address": "456 Uptown Ave, Cityville",
                    "country": 1,
                    "country_name": "Countryland",
                    "state": 5,
                    "state_name": "Stateland",
                    "city": 12,
                    "city_name": "Uptown City",
                    "zipcode": "67890",
                    "contact1": 1122334455,
                    "contact2": 5544332211,
                    "latitude": "40.730610",
                    "longitude": "-73.935242",
                    "opening_hour": "10:00:00",
                    "closing_hour": "18:00:00",
                    "establishment_year": 2012,
                    "description": "Handles all human resources activities.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-09-07T14:00:00Z",
                    "last_update_date": "2024-09-07T14:00:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Branch Department Details",
        description="Update information of an existing branch department by its ID.",
        request=BranchDepartmentSerializer,
        responses={
            200: OpenApiResponse(
                response=BranchDepartmentSerializer,
                description="Branch department updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Branch department not found.")
        },
        tags=["Branch Department"],
        examples=[
            OpenApiExample(
                name="Branch Department Update Request",
                summary="Request body for updating a branch department",
                description="Provide fields to update for the branch department.",
                value={
                    "description": "Updated description for Sales Department.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Branch Department Update Success Response",
                summary="Successful branch department update",
                description="Returns the updated branch department details.",
                value={
                    "id": 1,
                    "branch": 1,
                    "branch_name": "Downtown Branch",
                    "department": 3,
                    "department_name": "Sales",
                    "manager": 2,
                    "manager_name": "Jane Smith",
                    "code": "SLS001",
                    "address": "123 Main St, Cityville",
                    "country": 1,
                    "country_name": "Countryland",
                    "state": 5,
                    "state_name": "Stateland",
                    "city": 10,
                    "city_name": "Cityville",
                    "zipcode": "12345",
                    "contact1": 1234567890,
                    "contact2": 9876543210,
                    "latitude": "40.712776",
                    "longitude": "-74.005974",
                    "opening_hour": "09:00:00",
                    "closing_hour": "17:00:00",
                    "establishment_year": 2005,
                    "description": "Updated description for Sales Department.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-07-26T11:00:00Z",
                    "last_update_date": "2024-09-08T16:20:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Branch Department",
        description="Remove a branch department from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Branch department deleted successfully."),
            404: OpenApiResponse(description="Branch department not found.")
        },
        tags=["Branch Department"],
        examples=[
            OpenApiExample(
                name="Branch Department Deletion Success Response",
                summary="Successful branch department deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class BranchDepartmentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing branch department instances.
    """
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
    ordering_fields = ['code', 'branch', 'department', 'manager', 'status', 'is_active']
    ordering = ['code']
    permission_classes = [IsAuthenticated, IsEmployee]