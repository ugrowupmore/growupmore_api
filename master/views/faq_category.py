
# master/views/country.py

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from master.models.faq_category import FAQCategory
from master.serializers import FAQCategorySerializer
from authuser.permissions import IsEmployee
from rest_framework.permissions import IsAuthenticated

@extend_schema_view(
    list=extend_schema(
        summary="List FAQ Categories",
        description="Retrieve a list of all FAQ categories.",
        responses={
            200: OpenApiResponse(
                response=FAQCategorySerializer(many=True),
                description="A list of FAQ categories."
            )
        },
        tags=["FAQ Category"],
        examples=[
            OpenApiExample(
                name="FAQ Category List Response",
                summary="Successful retrieval of FAQ category list",
                description="Returns a list of all FAQ categories with their details.",
                value=[
                    {
                        "id": 1,
                        "category": "General",
                        "description": "General questions about our services.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-06-15T08:45:00Z",
                        "last_update_date": "2024-07-15T09:55:00Z",
                        "updated_by": None
                    },
                    # ... more FAQ categories
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve FAQ Category Details",
        description="Retrieve detailed information about a specific FAQ category by its ID.",
        responses={
            200: OpenApiResponse(
                response=FAQCategorySerializer,
                description="Detailed information about the FAQ category."
            ),
            404: OpenApiResponse(description="FAQ category not found.")
        },
        tags=["FAQ Category"],
        examples=[
            OpenApiExample(
                name="FAQ Category Detail Response",
                summary="Successful retrieval of FAQ category details",
                description="Returns detailed information about a specific FAQ category.",
                value={
                    "id": 1,
                    "category": "General",
                    "description": "General questions about our services.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-06-15T08:45:00Z",
                    "last_update_date": "2024-07-15T09:55:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New FAQ Category",
        description="Add a new FAQ category to the system by providing necessary details.",
        request=FAQCategorySerializer,
        responses={
            201: OpenApiResponse(
                response=FAQCategorySerializer,
                description="FAQ category created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["FAQ Category"],
        examples=[
            OpenApiExample(
                name="FAQ Category Creation Request",
                summary="Request body for creating a new FAQ category",
                description="Provide necessary fields to create a new FAQ category.",
                value={
                    "category": "Billing",
                    "description": "Questions related to billing and payments.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="FAQ Category Creation Success Response",
                summary="Successful FAQ category creation",
                description="Returns the created FAQ category details.",
                value={
                    "id": 2,
                    "category": "Billing",
                    "description": "Questions related to billing and payments.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-25T13:50:00Z",
                    "last_update_date": "2024-07-25T13:50:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update FAQ Category Details",
        description="Update information of an existing FAQ category by its ID.",
        request=FAQCategorySerializer,
        responses={
            200: OpenApiResponse(
                response=FAQCategorySerializer,
                description="FAQ category updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="FAQ category not found.")
        },
        tags=["FAQ Category"],
        examples=[
            OpenApiExample(
                name="FAQ Category Update Request",
                summary="Request body for updating an FAQ category",
                description="Provide fields to update for the FAQ category.",
                value={
                    "description": "Updated description for Billing.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="FAQ Category Update Success Response",
                summary="Successful FAQ category update",
                description="Returns the updated FAQ category details.",
                value={
                    "id": 2,
                    "category": "Billing",
                    "description": "Updated description for Billing.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-07-25T13:50:00Z",
                    "last_update_date": "2024-08-10T18:05:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete an FAQ Category",
        description="Remove an FAQ category from the system by its ID.",
        responses={
            204: OpenApiResponse(description="FAQ category deleted successfully."),
            404: OpenApiResponse(description="FAQ category not found.")
        },
        tags=["FAQ Category"],
        examples=[
            OpenApiExample(
                name="FAQ Category Deletion Success Response",
                summary="Successful FAQ category deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class FAQCategoryViewSet(viewsets.ModelViewSet):
    queryset = FAQCategory.objects.all()
    serializer_class = FAQCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'is_active']
    search_fields = ['category', 'description', 'status']
    ordering_fields = ['category', 'status', 'is_active']
    ordering = ['category']
    permission_classes = [IsAuthenticated, IsEmployee]