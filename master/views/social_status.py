
# master/views/country.py

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from master.models.social_status import SocialStatus
from master.serializers import SocialStatusSerializer
from authuser.permissions import IsEmployee
from rest_framework.permissions import IsAuthenticated

@extend_schema_view(
    list=extend_schema(
        summary="List Social Statuses",
        description="Retrieve a list of all social statuses.",
        responses={
            200: OpenApiResponse(
                response=SocialStatusSerializer(many=True),
                description="A list of social statuses."
            )
        },
        tags=["Social Status"],
        examples=[
            OpenApiExample(
                name="Social Status List Response",
                summary="Successful retrieval of social status list",
                description="Returns a list of all social statuses with their details.",
                value=[
                    {
                        "id": 1,
                        "name": "Single",
                        "description": "Individual not married.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-08-10T09:00:00Z",
                        "last_update_date": "2024-09-10T10:10:00Z",
                        "updated_by": None
                    },
                    # ... more social statuses
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Social Status Details",
        description="Retrieve detailed information about a specific social status by its ID.",
        responses={
            200: OpenApiResponse(
                response=SocialStatusSerializer,
                description="Detailed information about the social status."
            ),
            404: OpenApiResponse(description="Social status not found.")
        },
        tags=["Social Status"],
        examples=[
            OpenApiExample(
                name="Social Status Detail Response",
                summary="Successful retrieval of social status details",
                description="Returns detailed information about a specific social status.",
                value={
                    "id": 1,
                    "name": "Single",
                    "description": "Individual not married.",
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
        summary="Create a New Social Status",
        description="Add a new social status to the system by providing necessary details.",
        request=SocialStatusSerializer,
        responses={
            201: OpenApiResponse(
                response=SocialStatusSerializer,
                description="Social status created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Social Status"],
        examples=[
            OpenApiExample(
                name="Social Status Creation Request",
                summary="Request body for creating a new social status",
                description="Provide necessary fields to create a new social status.",
                value={
                    "name": "Married",
                    "description": "Individual is legally married.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Social Status Creation Success Response",
                summary="Successful social status creation",
                description="Returns the created social status details.",
                value={
                    "id": 2,
                    "name": "Married",
                    "description": "Individual is legally married.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-09-05T14:15:00Z",
                    "last_update_date": "2024-09-05T14:15:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Social Status Details",
        description="Update information of an existing social status by its ID.",
        request=SocialStatusSerializer,
        responses={
            200: OpenApiResponse(
                response=SocialStatusSerializer,
                description="Social status updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Social status not found.")
        },
        tags=["Social Status"],
        examples=[
            OpenApiExample(
                name="Social Status Update Request",
                summary="Request body for updating a social status",
                description="Provide fields to update for the social status.",
                value={
                    "description": "Updated description for Single status.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Social Status Update Success Response",
                summary="Successful social status update",
                description="Returns the updated social status details.",
                value={
                    "id": 1,
                    "name": "Single",
                    "description": "Updated description for Single status.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-08-10T09:00:00Z",
                    "last_update_date": "2024-09-15T17:35:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Social Status",
        description="Remove a social status from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Social status deleted successfully."),
            404: OpenApiResponse(description="Social status not found.")
        },
        tags=["Social Status"],
        examples=[
            OpenApiExample(
                name="Social Status Deletion Success Response",
                summary="Successful social status deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class SocialStatusViewSet(viewsets.ModelViewSet):
    queryset = SocialStatus.objects.all()
    serializer_class = SocialStatusSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'status', 'is_active']
    search_fields = ['name', 'description', 'status']
    ordering_fields = ['name', 'status', 'is_active']
    ordering = ['name']
    permission_classes = [IsAuthenticated, IsEmployee]