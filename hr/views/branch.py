
# hr/views/branch.py

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
from hr.models.branch import Branch
from hr.serializers import BranchSerializer



@extend_schema_view(
    list=extend_schema(
        summary="List Branches",
        description="Retrieve a list of all branches.",
        responses={
            200: OpenApiResponse(
                response=BranchSerializer(many=True),
                description="A list of branches."
            )
        },
        tags=["Branch"],
        examples=[
            OpenApiExample(
                name="Branch List Response",
                summary="Successful retrieval of branch list",
                description="Returns a list of all branches with their details.",
                value=[
                    {
                        "id": 1,
                        "branch_type": 1,
                        "branch_type_name": "Main Branch",
                        "name": "Downtown Branch",
                        "code": "DTB001",
                        "logo": "http://localhost:8000/media/branch_logos/downtown_branch.png",
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
                        "email": "downtown@company.com",
                        "latitude": "40.712776",
                        "longitude": "-74.005974",
                        "location_url": "http://maps.example.com/?q=40.712776,-74.005974",
                        "reports_to": None,
                        "reports_to_name": None,
                        "opening_hour": "09:00:00",
                        "closing_hour": "17:00:00",
                        "establishment_year": 2000,
                        "last_audit_date": "2024-09-01",
                        "description": "Handles all major operations.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-07-25T10:45:00Z",
                        "last_update_date": "2024-08-25T11:55:00Z",
                        "updated_by": None
                    },
                    # ... more branches
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Branch Details",
        description="Retrieve detailed information about a specific branch by its ID.",
        responses={
            200: OpenApiResponse(
                response=BranchSerializer,
                description="Detailed information about the branch."
            ),
            404: OpenApiResponse(description="Branch not found.")
        },
        tags=["Branch"],
        examples=[
            OpenApiExample(
                name="Branch Detail Response",
                summary="Successful retrieval of branch details",
                description="Returns detailed information about a specific branch.",
                value={
                    "id": 1,
                    "branch_type": 1,
                    "branch_type_name": "Main Branch",
                    "name": "Downtown Branch",
                    "code": "DTB001",
                    "logo": "http://localhost:8000/media/branch_logos/downtown_branch.png",
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
                    "email": "downtown@company.com",
                    "latitude": "40.712776",
                    "longitude": "-74.005974",
                    "location_url": "http://maps.example.com/?q=40.712776,-74.005974",
                    "reports_to": None,
                    "reports_to_name": None,
                    "opening_hour": "09:00:00",
                    "closing_hour": "17:00:00",
                    "establishment_year": 2000,
                    "last_audit_date": "2024-09-01",
                    "description": "Handles all major operations.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-25T10:45:00Z",
                    "last_update_date": "2024-08-25T11:55:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Branch",
        description="Add a new branch to the system by providing necessary details.",
        request=BranchSerializer,
        responses={
            201: OpenApiResponse(
                response=BranchSerializer,
                description="Branch created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Branch"],
        examples=[
            OpenApiExample(
                name="Branch Creation Request",
                summary="Request body for creating a new branch",
                description="Provide necessary fields to create a new branch.",
                value={
                    "branch_type": 2,
                    "name": "Uptown Branch",
                    "code": "UTB002",
                    "logo": "http://localhost:8000/media/branch_logos/uptown_branch.png",
                    "address": "456 Uptown Ave, Cityville",
                    "country": 1,
                    "state": 5,
                    "city": 12,
                    "zipcode": "67890",
                    "contact1": 1122334455,
                    "contact2": 5544332211,
                    "email": "uptown@company.com",
                    "latitude": "40.730610",
                    "longitude": "-73.935242",
                    "location_url": "http://maps.example.com/?q=40.730610,-73.935242",
                    "reports_to": 1,
                    "opening_hour": "10:00:00",
                    "closing_hour": "18:00:00",
                    "establishment_year": 2010,
                    "last_audit_date": "2024-09-05",
                    "description": "Supports regional operations.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Branch Creation Success Response",
                summary="Successful branch creation",
                description="Returns the created branch details.",
                value={
                    "id": 2,
                    "branch_type": 2,
                    "branch_type_name": "Satellite Branch",
                    "name": "Uptown Branch",
                    "code": "UTB002",
                    "logo": "http://localhost:8000/media/branch_logos/uptown_branch.png",
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
                    "email": "uptown@company.com",
                    "latitude": "40.730610",
                    "longitude": "-73.935242",
                    "location_url": "http://maps.example.com/?q=40.730610,-73.935242",
                    "reports_to": 1,
                    "reports_to_name": "Downtown Manager",
                    "opening_hour": "10:00:00",
                    "closing_hour": "18:00:00",
                    "establishment_year": 2010,
                    "last_audit_date": "2024-09-05",
                    "description": "Supports regional operations.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-09-06T14:50:00Z",
                    "last_update_date": "2024-09-06T14:50:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Branch Details",
        description="Update information of an existing branch by its ID.",
        request=BranchSerializer,
        responses={
            200: OpenApiResponse(
                response=BranchSerializer,
                description="Branch updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Branch not found.")
        },
        tags=["Branch"],
        examples=[
            OpenApiExample(
                name="Branch Update Request",
                summary="Request body for updating a branch",
                description="Provide fields to update for the branch.",
                value={
                    "description": "Updated description for Downtown Branch.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Branch Update Success Response",
                summary="Successful branch update",
                description="Returns the updated branch details.",
                value={
                    "id": 1,
                    "branch_type": 1,
                    "branch_type_name": "Main Branch",
                    "name": "Downtown Branch",
                    "code": "DTB001",
                    "logo": "http://localhost:8000/media/branch_logos/downtown_branch.png",
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
                    "email": "downtown@company.com",
                    "latitude": "40.712776",
                    "longitude": "-74.005974",
                    "location_url": "http://maps.example.com/?q=40.712776,-74.005974",
                    "reports_to": None,
                    "reports_to_name": None,
                    "opening_hour": "09:00:00",
                    "closing_hour": "17:00:00",
                    "establishment_year": 2000,
                    "last_audit_date": "2024-09-01",
                    "description": "Updated description for Downtown Branch.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-07-25T10:45:00Z",
                    "last_update_date": "2024-09-07T16:20:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Branch",
        description="Remove a branch from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Branch deleted successfully."),
            404: OpenApiResponse(description="Branch not found.")
        },
        tags=["Branch"],
        examples=[
            OpenApiExample(
                name="Branch Deletion Success Response",
                summary="Successful branch deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class BranchViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing branch instances.
    """
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
    ordering_fields = ['name', 'code', 'branch_type', 'status', 'is_active']
    ordering = ['code']
    permission_classes = [IsAuthenticated, IsEmployee]