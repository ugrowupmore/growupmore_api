
# master/views/country.py

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from master.models.offer_type import OfferType
from master.serializers import OfferTypeSerializer
from authuser.permissions import IsEmployee
from rest_framework.permissions import IsAuthenticated

@extend_schema_view(
    list=extend_schema(
        summary="List Offer Types",
        description="Retrieve a list of all offer types.",
        responses={
            200: OpenApiResponse(
                response=OfferTypeSerializer(many=True),
                description="A list of offer types."
            )
        },
        tags=["Offer Type"],
        examples=[
            OpenApiExample(
                name="Offer Type List Response",
                summary="Successful retrieval of offer type list",
                description="Returns a list of all offer types with their details.",
                value=[
                    {
                        "id": 1,
                        "type": "Discount",
                        "description": "Offers providing price reductions on products or services.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-07-20T10:15:00Z",
                        "last_update_date": "2024-08-20T11:25:00Z",
                        "updated_by": None
                    },
                    # ... more offer types
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Offer Type Details",
        description="Retrieve detailed information about a specific offer type by its ID.",
        responses={
            200: OpenApiResponse(
                response=OfferTypeSerializer,
                description="Detailed information about the offer type."
            ),
            404: OpenApiResponse(description="Offer type not found.")
        },
        tags=["Offer Type"],
        examples=[
            OpenApiExample(
                name="Offer Type Detail Response",
                summary="Successful retrieval of offer type details",
                description="Returns detailed information about a specific offer type.",
                value={
                    "id": 1,
                    "type": "Discount",
                    "description": "Offers providing price reductions on products or services.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-20T10:15:00Z",
                    "last_update_date": "2024-08-20T11:25:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Offer Type",
        description="Add a new offer type to the system by providing necessary details.",
        request=OfferTypeSerializer,
        responses={
            201: OpenApiResponse(
                response=OfferTypeSerializer,
                description="Offer type created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Offer Type"],
        examples=[
            OpenApiExample(
                name="Offer Type Creation Request",
                summary="Request body for creating a new offer type",
                description="Provide necessary fields to create a new offer type.",
                value={
                    "type": "Buy One Get One Free",
                    "description": "Promotions where buying one item gets another free.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Offer Type Creation Success Response",
                summary="Successful offer type creation",
                description="Returns the created offer type details.",
                value={
                    "id": 2,
                    "type": "Buy One Get One Free",
                    "description": "Promotions where buying one item gets another free.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-08-08T14:45:00Z",
                    "last_update_date": "2024-08-08T14:45:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Offer Type Details",
        description="Update information of an existing offer type by its ID.",
        request=OfferTypeSerializer,
        responses={
            200: OpenApiResponse(
                response=OfferTypeSerializer,
                description="Offer type updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Offer type not found.")
        },
        tags=["Offer Type"],
        examples=[
            OpenApiExample(
                name="Offer Type Update Request",
                summary="Request body for updating an offer type",
                description="Provide fields to update for the offer type.",
                value={
                    "description": "Updated description for Discount.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Offer Type Update Success Response",
                summary="Successful offer type update",
                description="Returns the updated offer type details.",
                value={
                    "id": 1,
                    "type": "Discount",
                    "description": "Updated description for Discount.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-07-20T10:15:00Z",
                    "last_update_date": "2024-08-12T17:55:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete an Offer Type",
        description="Remove an offer type from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Offer type deleted successfully."),
            404: OpenApiResponse(description="Offer type not found.")
        },
        tags=["Offer Type"],
        examples=[
            OpenApiExample(
                name="Offer Type Deletion Success Response",
                summary="Successful offer type deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class OfferTypeViewSet(viewsets.ModelViewSet):
    queryset = OfferType.objects.all()
    serializer_class = OfferTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status', 'is_active']
    search_fields = ['type', 'description', 'status']
    ordering_fields = ['type', 'status', 'is_active']
    ordering = ['type']
    permission_classes = [IsAuthenticated, IsEmployee]