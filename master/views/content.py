
# master/views/country.py

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from master.models.content import Content
from master.serializers import ContentSerializer
from authuser.permissions import IsEmployee
from rest_framework.permissions import IsAuthenticated

@extend_schema_view(
    list=extend_schema(
        summary="List Contents",
        description="Retrieve a list of all contents.",
        responses={
            200: OpenApiResponse(
                response=ContentSerializer(many=True),
                description="A list of contents."
            )
        },
        tags=["Content"],
        examples=[
            OpenApiExample(
                name="Content List Response",
                summary="Successful retrieval of content list",
                description="Returns a list of all contents with their details.",
                value=[
                    {
                        "id": 1,
                        "content": "Welcome Message",
                        "description": "Initial greeting message for new users.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-07-15T09:00:00Z",
                        "last_update_date": "2024-08-15T10:10:00Z",
                        "updated_by": None
                    },
                    # ... more contents
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Content Details",
        description="Retrieve detailed information about a specific content by its ID.",
        responses={
            200: OpenApiResponse(
                response=ContentSerializer,
                description="Detailed information about the content."
            ),
            404: OpenApiResponse(description="Content not found.")
        },
        tags=["Content"],
        examples=[
            OpenApiExample(
                name="Content Detail Response",
                summary="Successful retrieval of content details",
                description="Returns detailed information about a specific content.",
                value={
                    "id": 1,
                    "content": "Welcome Message",
                    "description": "Initial greeting message for new users.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-15T09:00:00Z",
                    "last_update_date": "2024-08-15T10:10:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Content",
        description="Add a new content to the system by providing necessary details.",
        request=ContentSerializer,
        responses={
            201: OpenApiResponse(
                response=ContentSerializer,
                description="Content created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Content"],
        examples=[
            OpenApiExample(
                name="Content Creation Request",
                summary="Request body for creating a new content",
                description="Provide necessary fields to create a new content.",
                value={
                    "content": "Thank You Message",
                    "description": "Message displayed after user completes an action.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Content Creation Success Response",
                summary="Successful content creation",
                description="Returns the created content details.",
                value={
                    "id": 2,
                    "content": "Thank You Message",
                    "description": "Message displayed after user completes an action.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-08-07T11:30:00Z",
                    "last_update_date": "2024-08-07T11:30:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Content Details",
        description="Update information of an existing content by its ID.",
        request=ContentSerializer,
        responses={
            200: OpenApiResponse(
                response=ContentSerializer,
                description="Content updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Content not found.")
        },
        tags=["Content"],
        examples=[
            OpenApiExample(
                name="Content Update Request",
                summary="Request body for updating a content",
                description="Provide fields to update for the content.",
                value={
                    "description": "Updated greeting message for new users.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Content Update Success Response",
                summary="Successful content update",
                description="Returns the updated content details.",
                value={
                    "id": 1,
                    "content": "Welcome Message",
                    "description": "Updated greeting message for new users.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-07-15T09:00:00Z",
                    "last_update_date": "2024-08-12T17:20:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Content",
        description="Remove a content from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Content deleted successfully."),
            404: OpenApiResponse(description="Content not found.")
        },
        tags=["Content"],
        examples=[
            OpenApiExample(
                name="Content Deletion Success Response",
                summary="Successful content deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['content', 'status', 'is_active']
    search_fields = ['content', 'description', 'status']
    ordering_fields = ['content', 'status', 'is_active']
    ordering = ['content']
    permission_classes = [IsAuthenticated, IsEmployee]