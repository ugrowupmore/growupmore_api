
# master/views/country.py

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from master.models.event_type import EventType
from master.serializers import EventTypeSerializer
from authuser.permissions import IsEmployee
from rest_framework.permissions import IsAuthenticated

@extend_schema_view(
    list=extend_schema(
        summary="List Event Types",
        description="Retrieve a list of all event types.",
        responses={
            200: OpenApiResponse(
                response=EventTypeSerializer(many=True),
                description="A list of event types."
            )
        },
        tags=["Event Type"],
        examples=[
            OpenApiExample(
                name="Event Type List Response",
                summary="Successful retrieval of event type list",
                description="Returns a list of all event types with their details.",
                value=[
                    {
                        "id": 1,
                        "type": "Conference",
                        "description": "Large formal gatherings for discussion.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-06-10T09:00:00Z",
                        "last_update_date": "2024-07-10T10:10:00Z",
                        "updated_by": None
                    },
                    # ... more event types
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Event Type Details",
        description="Retrieve detailed information about a specific event type by its ID.",
        responses={
            200: OpenApiResponse(
                response=EventTypeSerializer,
                description="Detailed information about the event type."
            ),
            404: OpenApiResponse(description="Event type not found.")
        },
        tags=["Event Type"],
        examples=[
            OpenApiExample(
                name="Event Type Detail Response",
                summary="Successful retrieval of event type details",
                description="Returns detailed information about a specific event type.",
                value={
                    "id": 1,
                    "type": "Conference",
                    "description": "Large formal gatherings for discussion.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-06-10T09:00:00Z",
                    "last_update_date": "2024-07-10T10:10:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Event Type",
        description="Add a new event type to the system by providing necessary details.",
        request=EventTypeSerializer,
        responses={
            201: OpenApiResponse(
                response=EventTypeSerializer,
                description="Event type created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Event Type"],
        examples=[
            OpenApiExample(
                name="Event Type Creation Request",
                summary="Request body for creating a new event type",
                description="Provide necessary fields to create a new event type.",
                value={
                    "type": "Workshop",
                    "description": "Interactive training sessions focusing on specific skills.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Event Type Creation Success Response",
                summary="Successful event type creation",
                description="Returns the created event type details.",
                value={
                    "id": 2,
                    "type": "Workshop",
                    "description": "Interactive training sessions focusing on specific skills.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-24T11:15:00Z",
                    "last_update_date": "2024-07-24T11:15:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Event Type Details",
        description="Update information of an existing event type by its ID.",
        request=EventTypeSerializer,
        responses={
            200: OpenApiResponse(
                response=EventTypeSerializer,
                description="Event type updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Event type not found.")
        },
        tags=["Event Type"],
        examples=[
            OpenApiExample(
                name="Event Type Update Request",
                summary="Request body for updating an event type",
                description="Provide fields to update for the event type.",
                value={
                    "description": "Updated description for Conference.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Event Type Update Success Response",
                summary="Successful event type update",
                description="Returns the updated event type details.",
                value={
                    "id": 1,
                    "type": "Conference",
                    "description": "Updated description for Conference.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-06-10T09:00:00Z",
                    "last_update_date": "2024-08-10T17:20:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete an Event Type",
        description="Remove an event type from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Event type deleted successfully."),
            404: OpenApiResponse(description="Event type not found.")
        },
        tags=["Event Type"],
        examples=[
            OpenApiExample(
                name="Event Type Deletion Success Response",
                summary="Successful event type deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class EventTypeViewSet(viewsets.ModelViewSet):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status', 'is_active']
    search_fields = ['type', 'description', 'status']
    ordering_fields = ['type', 'status', 'is_active']
    ordering = ['type']
    permission_classes = [IsAuthenticated, IsEmployee]