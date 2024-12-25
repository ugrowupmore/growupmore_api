
# master/views/country.py

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from master.models.promotion_type import PromotionType
from master.serializers import PromotionTypeSerializer
from authuser.permissions import IsEmployee
from rest_framework.permissions import IsAuthenticated

@extend_schema_view(
    list=extend_schema(
        summary="List Promotion Types",
        description="Retrieve a list of all promotion types.",
        responses={
            200: OpenApiResponse(
                response=PromotionTypeSerializer(many=True),
                description="A list of promotion types."
            )
        },
        tags=["Promotion Type"],
        examples=[
            OpenApiExample(
                name="Promotion Type List Response",
                summary="Successful retrieval of promotion type list",
                description="Returns a list of all promotion types with their details.",
                value=[
                    {
                        "id": 1,
                        "type": "Seasonal Promotion",
                        "description": "Promotions tied to specific seasons or holidays.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-07-30T10:15:00Z",
                        "last_update_date": "2024-08-30T11:25:00Z",
                        "updated_by": None
                    },
                    # ... more promotion types
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Promotion Type Details",
        description="Retrieve detailed information about a specific promotion type by its ID.",
        responses={
            200: OpenApiResponse(
                response=PromotionTypeSerializer,
                description="Detailed information about the promotion type."
            ),
            404: OpenApiResponse(description="Promotion type not found.")
        },
        tags=["Promotion Type"],
        examples=[
            OpenApiExample(
                name="Promotion Type Detail Response",
                summary="Successful retrieval of promotion type details",
                description="Returns detailed information about a specific promotion type.",
                value={
                    "id": 1,
                    "type": "Seasonal Promotion",
                    "description": "Promotions tied to specific seasons or holidays.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-30T10:15:00Z",
                    "last_update_date": "2024-08-30T11:25:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Promotion Type",
        description="Add a new promotion type to the system by providing necessary details.",
        request=PromotionTypeSerializer,
        responses={
            201: OpenApiResponse(
                response=PromotionTypeSerializer,
                description="Promotion type created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Promotion Type"],
        examples=[
            OpenApiExample(
                name="Promotion Type Creation Request",
                summary="Request body for creating a new promotion type",
                description="Provide necessary fields to create a new promotion type.",
                value={
                    "type": "Flash Sale",
                    "description": "Limited-time sales offering significant discounts.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Promotion Type Creation Success Response",
                summary="Successful promotion type creation",
                description="Returns the created promotion type details.",
                value={
                    "id": 2,
                    "type": "Flash Sale",
                    "description": "Limited-time sales offering significant discounts.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-08-15T14:30:00Z",
                    "last_update_date": "2024-08-15T14:30:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Promotion Type Details",
        description="Update information of an existing promotion type by its ID.",
        request=PromotionTypeSerializer,
        responses={
            200: OpenApiResponse(
                response=PromotionTypeSerializer,
                description="Promotion type updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Promotion type not found.")
        },
        tags=["Promotion Type"],
        examples=[
            OpenApiExample(
                name="Promotion Type Update Request",
                summary="Request body for updating a promotion type",
                description="Provide fields to update for the promotion type.",
                value={
                    "description": "Updated description for Seasonal Promotion.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Promotion Type Update Success Response",
                summary="Successful promotion type update",
                description="Returns the updated promotion type details.",
                value={
                    "id": 1,
                    "type": "Seasonal Promotion",
                    "description": "Updated description for Seasonal Promotion.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-07-30T10:15:00Z",
                    "last_update_date": "2024-08-13T17:35:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Promotion Type",
        description="Remove a promotion type from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Promotion type deleted successfully."),
            404: OpenApiResponse(description="Promotion type not found.")
        },
        tags=["Promotion Type"],
        examples=[
            OpenApiExample(
                name="Promotion Type Deletion Success Response",
                summary="Successful promotion type deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class PromotionTypeViewSet(viewsets.ModelViewSet):
    queryset = PromotionType.objects.all()
    serializer_class = PromotionTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status', 'is_active']
    search_fields = ['type', 'description', 'status']
    ordering_fields = ['type', 'status', 'is_active']
    ordering = ['type']
    permission_classes = [IsAuthenticated, IsEmployee]