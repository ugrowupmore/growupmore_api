
# master/views/country.py

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from master.models.marketing_type import MarketingType
from master.serializers import MarketingTypeSerializer
from authuser.permissions import IsEmployee
from rest_framework.permissions import IsAuthenticated

@extend_schema_view(
    list=extend_schema(
        summary="List Marketing Types",
        description="Retrieve a list of all marketing types.",
        responses={
            200: OpenApiResponse(
                response=MarketingTypeSerializer(many=True),
                description="A list of marketing types."
            )
        },
        tags=["Marketing Type"],
        examples=[
            OpenApiExample(
                name="Marketing Type List Response",
                summary="Successful retrieval of marketing type list",
                description="Returns a list of all marketing types with their details.",
                value=[
                    {
                        "id": 1,
                        "type": "Digital Marketing",
                        "description": "Online marketing activities including SEO, SEM, and social media marketing.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-06-20T07:30:00Z",
                        "last_update_date": "2024-07-20T08:40:00Z",
                        "updated_by": None
                    },
                    # ... more marketing types
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Marketing Type Details",
        description="Retrieve detailed information about a specific marketing type by its ID.",
        responses={
            200: OpenApiResponse(
                response=MarketingTypeSerializer,
                description="Detailed information about the marketing type."
            ),
            404: OpenApiResponse(description="Marketing type not found.")
        },
        tags=["Marketing Type"],
        examples=[
            OpenApiExample(
                name="Marketing Type Detail Response",
                summary="Successful retrieval of marketing type details",
                description="Returns detailed information about a specific marketing type.",
                value={
                    "id": 1,
                    "type": "Digital Marketing",
                    "description": "Online marketing activities including SEO, SEM, and social media marketing.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-06-20T07:30:00Z",
                    "last_update_date": "2024-07-20T08:40:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Marketing Type",
        description="Add a new marketing type to the system by providing necessary details.",
        request=MarketingTypeSerializer,
        responses={
            201: OpenApiResponse(
                response=MarketingTypeSerializer,
                description="Marketing type created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Marketing Type"],
        examples=[
            OpenApiExample(
                name="Marketing Type Creation Request",
                summary="Request body for creating a new marketing type",
                description="Provide necessary fields to create a new marketing type.",
                value={
                    "type": "Content Marketing",
                    "description": "Creating and distributing valuable content to attract and engage target audiences.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Marketing Type Creation Success Response",
                summary="Successful marketing type creation",
                description="Returns the created marketing type details.",
                value={
                    "id": 2,
                    "type": "Content Marketing",
                    "description": "Creating and distributing valuable content to attract and engage target audiences.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-26T16:10:00Z",
                    "last_update_date": "2024-07-26T16:10:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Marketing Type Details",
        description="Update information of an existing marketing type by its ID.",
        request=MarketingTypeSerializer,
        responses={
            200: OpenApiResponse(
                response=MarketingTypeSerializer,
                description="Marketing type updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Marketing type not found.")
        },
        tags=["Marketing Type"],
        examples=[
            OpenApiExample(
                name="Marketing Type Update Request",
                summary="Request body for updating a marketing type",
                description="Provide fields to update for the marketing type.",
                value={
                    "description": "Updated description for Digital Marketing.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Marketing Type Update Success Response",
                summary="Successful marketing type update",
                description="Returns the updated marketing type details.",
                value={
                    "id": 1,
                    "type": "Digital Marketing",
                    "description": "Updated description for Digital Marketing.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-06-20T07:30:00Z",
                    "last_update_date": "2024-08-11T19:00:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Marketing Type",
        description="Remove a marketing type from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Marketing type deleted successfully."),
            404: OpenApiResponse(description="Marketing type not found.")
        },
        tags=["Marketing Type"],
        examples=[
            OpenApiExample(
                name="Marketing Type Deletion Success Response",
                summary="Successful marketing type deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class MarketingTypeViewSet(viewsets.ModelViewSet):
    queryset = MarketingType.objects.all()
    serializer_class = MarketingTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status', 'is_active']
    search_fields = ['type', 'description', 'status']
    ordering_fields = ['type', 'status', 'is_active']
    ordering = ['type']
    permission_classes = [IsAuthenticated, IsEmployee]