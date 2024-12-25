
# master/views/country.py

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from master.models.branch_type import BranchType
from master.serializers import BranchTypeSerializer
from authuser.permissions import IsEmployee
from rest_framework.permissions import IsAuthenticated

@extend_schema_view(
    list=extend_schema(
        summary="List Branch Types",
        description="Retrieve a list of all branch types.",
        responses={
            200: OpenApiResponse(
                response=BranchTypeSerializer(many=True),
                description="A list of branch types."
            )
        },
        tags=["Branch Type"],
        examples=[
            OpenApiExample(
                name="Branch Type List Response",
                summary="Successful retrieval of branch type list",
                description="Returns a list of all branch types with their details.",
                value=[
                    {
                        "id": 1,
                        "type": "Main Branch",
                        "image": "http://localhost:8000/media/branch_types/main_branch.png",
                        "description": "Primary branch handling major operations.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-07-01T10:00:00Z",
                        "last_update_date": "2024-08-01T11:15:00Z",
                        "updated_by": None
                    },
                    # ... more branch types
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Branch Type Details",
        description="Retrieve detailed information about a specific branch type by its ID.",
        responses={
            200: OpenApiResponse(
                response=BranchTypeSerializer,
                description="Detailed information about the branch type."
            ),
            404: OpenApiResponse(description="Branch type not found.")
        },
        tags=["Branch Type"],
        examples=[
            OpenApiExample(
                name="Branch Type Detail Response",
                summary="Successful retrieval of branch type details",
                description="Returns detailed information about a specific branch type.",
                value={
                    "id": 1,
                    "type": "Main Branch",
                    "image": "http://localhost:8000/media/branch_types/main_branch.png",
                    "description": "Primary branch handling major operations.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-01T10:00:00Z",
                    "last_update_date": "2024-08-01T11:15:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Branch Type",
        description="Add a new branch type to the system by providing necessary details.",
        request=BranchTypeSerializer,
        responses={
            201: OpenApiResponse(
                response=BranchTypeSerializer,
                description="Branch type created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Branch Type"],
        examples=[
            OpenApiExample(
                name="Branch Type Creation Request",
                summary="Request body for creating a new branch type",
                description="Provide necessary fields to create a new branch type.",
                value={
                    "type": "Satellite Branch",
                    "image": "http://localhost:8000/media/branch_types/satellite_branch.png",
                    "description": "Secondary branch supporting the main branch operations.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Branch Type Creation Success Response",
                summary="Successful branch type creation",
                description="Returns the created branch type details.",
                value={
                    "id": 2,
                    "type": "Satellite Branch",
                    "image": "http://localhost:8000/media/branch_types/satellite_branch.png",
                    "description": "Secondary branch supporting the main branch operations.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-08-05T09:30:00Z",
                    "last_update_date": "2024-08-05T09:30:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Branch Type Details",
        description="Update information of an existing branch type by its ID.",
        request=BranchTypeSerializer,
        responses={
            200: OpenApiResponse(
                response=BranchTypeSerializer,
                description="Branch type updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Branch type not found.")
        },
        tags=["Branch Type"],
        examples=[
            OpenApiExample(
                name="Branch Type Update Request",
                summary="Request body for updating a branch type",
                description="Provide fields to update for the branch type.",
                value={
                    "description": "Updated description for Main Branch.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Branch Type Update Success Response",
                summary="Successful branch type update",
                description="Returns the updated branch type details.",
                value={
                    "id": 1,
                    "type": "Main Branch",
                    "image": "http://localhost:8000/media/branch_types/main_branch.png",
                    "description": "Updated description for Main Branch.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-07-01T10:00:00Z",
                    "last_update_date": "2024-08-10T12:20:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Branch Type",
        description="Remove a branch type from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Branch type deleted successfully."),
            404: OpenApiResponse(description="Branch type not found.")
        },
        tags=["Branch Type"],
        examples=[
            OpenApiExample(
                name="Branch Type Deletion Success Response",
                summary="Successful branch type deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class BranchTypeViewSet(viewsets.ModelViewSet):
    queryset = BranchType.objects.all()
    serializer_class = BranchTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status', 'is_active']
    search_fields = ['type', 'description', 'status']
    ordering_fields = ['type', 'status', 'is_active']
    ordering = ['type']
    permission_classes = [IsAuthenticated, IsEmployee]