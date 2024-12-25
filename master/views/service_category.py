
# master/views/country.py

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from master.models.service_category import ServiceCategory
from master.serializers import ServiceCategorySerializer
from authuser.permissions import IsEmployee
from rest_framework.permissions import IsAuthenticated

@extend_schema_view(
    list=extend_schema(
        summary="List Service Categories",
        description="Retrieve a list of all service categories.",
        responses={
            200: OpenApiResponse(
                response=ServiceCategorySerializer(many=True),
                description="A list of service categories."
            )
        },
        tags=["Service Category"],
        examples=[
            OpenApiExample(
                name="Service Category List Response",
                summary="Successful retrieval of service category list",
                description="Returns a list of all service categories with their details.",
                value=[
                    {
                        "id": 1,
                        "category": "Consulting",
                        "description": "Professional consulting services.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-05-15T11:00:00Z",
                        "last_update_date": "2024-06-15T12:00:00Z",
                        "updated_by": None
                    },
                    # ... more service categories
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Service Category Details",
        description="Retrieve detailed information about a specific service category by its ID.",
        responses={
            200: OpenApiResponse(
                response=ServiceCategorySerializer,
                description="Detailed information about the service category."
            ),
            404: OpenApiResponse(description="Service category not found.")
        },
        tags=["Service Category"],
        examples=[
            OpenApiExample(
                name="Service Category Detail Response",
                summary="Successful retrieval of service category details",
                description="Returns detailed information about a specific service category.",
                value={
                    "id": 1,
                    "category": "Consulting",
                    "description": "Professional consulting services.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-05-15T11:00:00Z",
                    "last_update_date": "2024-06-15T12:00:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Service Category",
        description="Add a new service category to the system by providing necessary details.",
        request=ServiceCategorySerializer,
        responses={
            201: OpenApiResponse(
                response=ServiceCategorySerializer,
                description="Service category created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Service Category"],
        examples=[
            OpenApiExample(
                name="Service Category Creation Request",
                summary="Request body for creating a new service category",
                description="Provide necessary fields to create a new service category.",
                value={
                    "category": "IT Support",
                    "description": "Technical support services for IT infrastructure.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Service Category Creation Success Response",
                summary="Successful service category creation",
                description="Returns the created service category details.",
                value={
                    "id": 2,
                    "category": "IT Support",
                    "description": "Technical support services for IT infrastructure.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-20T13:45:00Z",
                    "last_update_date": "2024-07-20T13:45:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Service Category Details",
        description="Update information of an existing service category by its ID.",
        request=ServiceCategorySerializer,
        responses={
            200: OpenApiResponse(
                response=ServiceCategorySerializer,
                description="Service category updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Service category not found.")
        },
        tags=["Service Category"],
        examples=[
            OpenApiExample(
                name="Service Category Update Request",
                summary="Request body for updating a service category",
                description="Provide fields to update for the service category.",
                value={
                    "description": "Comprehensive IT support and maintenance services.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Service Category Update Success Response",
                summary="Successful service category update",
                description="Returns the updated service category details.",
                value={
                    "id": 2,
                    "category": "IT Support",
                    "description": "Comprehensive IT support and maintenance services.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-07-20T13:45:00Z",
                    "last_update_date": "2024-08-06T16:20:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Service Category",
        description="Remove a service category from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Service category deleted successfully."),
            404: OpenApiResponse(description="Service category not found.")
        },
        tags=["Service Category"],
        examples=[
            OpenApiExample(
                name="Service Category Deletion Success Response",
                summary="Successful service category deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'is_active']
    search_fields = ['category', 'status', 'is_active']
    ordering_fields = ['category', 'status', 'is_active']
    ordering = ['category']
    permission_classes = [IsAuthenticated, IsEmployee]