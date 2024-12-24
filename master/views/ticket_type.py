
# master/views/country.py

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from master.models.ticket_type import TicketType
from master.serializers import TicketTypeSerializer
from authuser.permissions import IsEmployee
from rest_framework.permissions import IsAuthenticated

@extend_schema_view(
    list=extend_schema(
        summary="List Ticket Types",
        description="Retrieve a list of all ticket types.",
        responses={
            200: OpenApiResponse(
                response=TicketTypeSerializer(many=True),
                description="A list of ticket types."
            )
        },
        tags=["Ticket Type"],
        examples=[
            OpenApiExample(
                name="Ticket Type List Response",
                summary="Successful retrieval of ticket type list",
                description="Returns a list of all ticket types with their details.",
                value=[
                    {
                        "id": 1,
                        "type": "Support Ticket",
                        "description": "Tickets related to customer support and assistance.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-08-15T09:30:00Z",
                        "last_update_date": "2024-09-15T10:40:00Z",
                        "updated_by": None
                    },
                    # ... more ticket types
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Ticket Type Details",
        description="Retrieve detailed information about a specific ticket type by its ID.",
        responses={
            200: OpenApiResponse(
                response=TicketTypeSerializer,
                description="Detailed information about the ticket type."
            ),
            404: OpenApiResponse(description="Ticket type not found.")
        },
        tags=["Ticket Type"],
        examples=[
            OpenApiExample(
                name="Ticket Type Detail Response",
                summary="Successful retrieval of ticket type details",
                description="Returns detailed information about a specific ticket type.",
                value={
                    "id": 1,
                    "type": "Support Ticket",
                    "description": "Tickets related to customer support and assistance.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-08-15T09:30:00Z",
                    "last_update_date": "2024-09-15T10:40:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Ticket Type",
        description="Add a new ticket type to the system by providing necessary details.",
        request=TicketTypeSerializer,
        responses={
            201: OpenApiResponse(
                response=TicketTypeSerializer,
                description="Ticket type created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Ticket Type"],
        examples=[
            OpenApiExample(
                name="Ticket Type Creation Request",
                summary="Request body for creating a new ticket type",
                description="Provide necessary fields to create a new ticket type.",
                value={
                    "type": "Bug Report",
                    "description": "Tickets for reporting software bugs and issues.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Ticket Type Creation Success Response",
                summary="Successful ticket type creation",
                description="Returns the created ticket type details.",
                value={
                    "id": 2,
                    "type": "Bug Report",
                    "description": "Tickets for reporting software bugs and issues.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-09-05T14:35:00Z",
                    "last_update_date": "2024-09-05T14:35:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Ticket Type Details",
        description="Update information of an existing ticket type by its ID.",
        request=TicketTypeSerializer,
        responses={
            200: OpenApiResponse(
                response=TicketTypeSerializer,
                description="Ticket type updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Ticket type not found.")
        },
        tags=["Ticket Type"],
        examples=[
            OpenApiExample(
                name="Ticket Type Update Request",
                summary="Request body for updating a ticket type",
                description="Provide fields to update for the ticket type.",
                value={
                    "description": "Updated description for Support Ticket.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Ticket Type Update Success Response",
                summary="Successful ticket type update",
                description="Returns the updated ticket type details.",
                value={
                    "id": 1,
                    "type": "Support Ticket",
                    "description": "Updated description for Support Ticket.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-08-15T09:30:00Z",
                    "last_update_date": "2024-09-16T17:50:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Ticket Type",
        description="Remove a ticket type from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Ticket type deleted successfully."),
            404: OpenApiResponse(description="Ticket type not found.")
        },
        tags=["Ticket Type"],
        examples=[
            OpenApiExample(
                name="Ticket Type Deletion Success Response",
                summary="Successful ticket type deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class TicketTypeViewSet(viewsets.ModelViewSet):
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status', 'is_active']
    search_fields = ['type', 'description', 'status']
    ordering_fields = ['type', 'status', 'is_active']
    ordering = ['type']
    permission_classes = [IsAuthenticated, IsEmployee]