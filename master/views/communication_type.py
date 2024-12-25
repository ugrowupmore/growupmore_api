
# master/views/country.py

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from master.models.communication_type import CommunicationType
from master.serializers import CommunicationTypeSerializer
from authuser.permissions import IsEmployee
from rest_framework.permissions import IsAuthenticated

@extend_schema_view(
    list=extend_schema(
        summary="List Communication Types",
        description="Retrieve a list of all communication types.",
        responses={
            200: OpenApiResponse(
                response=CommunicationTypeSerializer(many=True),
                description="A list of communication types."
            )
        },
        tags=["Communication Type"],
        examples=[
            OpenApiExample(
                name="Communication Type List Response",
                summary="Successful retrieval of communication type list",
                description="Returns a list of all communication types with their details.",
                value=[
                    {
                        "id": 1,
                        "type": "Email",
                        "description": "Electronic mail communication.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-07-10T12:30:00Z",
                        "last_update_date": "2024-08-10T13:40:00Z",
                        "updated_by": None
                    },
                    # ... more communication types
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Communication Type Details",
        description="Retrieve detailed information about a specific communication type by its ID.",
        responses={
            200: OpenApiResponse(
                response=CommunicationTypeSerializer,
                description="Detailed information about the communication type."
            ),
            404: OpenApiResponse(description="Communication type not found.")
        },
        tags=["Communication Type"],
        examples=[
            OpenApiExample(
                name="Communication Type Detail Response",
                summary="Successful retrieval of communication type details",
                description="Returns detailed information about a specific communication type.",
                value={
                    "id": 1,
                    "type": "Email",
                    "description": "Electronic mail communication.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-10T12:30:00Z",
                    "last_update_date": "2024-08-10T13:40:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Communication Type",
        description="Add a new communication type to the system by providing necessary details.",
        request=CommunicationTypeSerializer,
        responses={
            201: OpenApiResponse(
                response=CommunicationTypeSerializer,
                description="Communication type created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Communication Type"],
        examples=[
            OpenApiExample(
                name="Communication Type Creation Request",
                summary="Request body for creating a new communication type",
                description="Provide necessary fields to create a new communication type.",
                value={
                    "type": "SMS",
                    "description": "Short Message Service communication.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Communication Type Creation Success Response",
                summary="Successful communication type creation",
                description="Returns the created communication type details.",
                value={
                    "id": 2,
                    "type": "SMS",
                    "description": "Short Message Service communication.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-08-07T14:45:00Z",
                    "last_update_date": "2024-08-07T14:45:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Communication Type Details",
        description="Update information of an existing communication type by its ID.",
        request=CommunicationTypeSerializer,
        responses={
            200: OpenApiResponse(
                response=CommunicationTypeSerializer,
                description="Communication type updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Communication type not found.")
        },
        tags=["Communication Type"],
        examples=[
            OpenApiExample(
                name="Communication Type Update Request",
                summary="Request body for updating a communication type",
                description="Provide fields to update for the communication type.",
                value={
                    "description": "Updated description for Email communication.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Communication Type Update Success Response",
                summary="Successful communication type update",
                description="Returns the updated communication type details.",
                value={
                    "id": 1,
                    "type": "Email",
                    "description": "Updated description for Email communication.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-07-10T12:30:00Z",
                    "last_update_date": "2024-08-12T17:55:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Communication Type",
        description="Remove a communication type from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Communication type deleted successfully."),
            404: OpenApiResponse(description="Communication type not found.")
        },
        tags=["Communication Type"],
        examples=[
            OpenApiExample(
                name="Communication Type Deletion Success Response",
                summary="Successful communication type deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class CommunicationTypeViewSet(viewsets.ModelViewSet):
    queryset = CommunicationType.objects.all()
    serializer_class = CommunicationTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status', 'is_active']
    search_fields = ['type', 'description', 'status']
    ordering_fields = ['type', 'status', 'is_active']
    ordering = ['type']
    permission_classes = [IsAuthenticated, IsEmployee]