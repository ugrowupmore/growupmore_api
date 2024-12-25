
# master/views/country.py

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from master.models.package import Package
from master.serializers import PackageSerializer
from authuser.permissions import IsEmployee
from rest_framework.permissions import IsAuthenticated

@extend_schema_view(
    list=extend_schema(
        summary="List Packages",
        description="Retrieve a list of all packages.",
        responses={
            200: OpenApiResponse(
                response=PackageSerializer(many=True),
                description="A list of packages."
            )
        },
        tags=["Package"],
        examples=[
            OpenApiExample(
                name="Package List Response",
                summary="Successful retrieval of package list",
                description="Returns a list of all packages with their details.",
                value=[
                    {
                        "id": 1,
                        "name": "Premium Package",
                        "image": "http://localhost:8000/media/packages/premium_package.png",
                        "description": "Includes all premium features and support.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-07-25T10:45:00Z",
                        "last_update_date": "2024-08-25T11:55:00Z",
                        "updated_by": None
                    },
                    # ... more packages
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Package Details",
        description="Retrieve detailed information about a specific package by its ID.",
        responses={
            200: OpenApiResponse(
                response=PackageSerializer,
                description="Detailed information about the package."
            ),
            404: OpenApiResponse(description="Package not found.")
        },
        tags=["Package"],
        examples=[
            OpenApiExample(
                name="Package Detail Response",
                summary="Successful retrieval of package details",
                description="Returns detailed information about a specific package.",
                value={
                    "id": 1,
                    "name": "Premium Package",
                    "image": "http://localhost:8000/media/packages/premium_package.png",
                    "description": "Includes all premium features and support.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-25T10:45:00Z",
                    "last_update_date": "2024-08-25T11:55:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Package",
        description="Add a new package to the system by providing necessary details.",
        request=PackageSerializer,
        responses={
            201: OpenApiResponse(
                response=PackageSerializer,
                description="Package created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Package"],
        examples=[
            OpenApiExample(
                name="Package Creation Request",
                summary="Request body for creating a new package",
                description="Provide necessary fields to create a new package.",
                value={
                    "name": "Basic Package",
                    "image": "http://localhost:8000/media/packages/basic_package.png",
                    "description": "Includes essential features and limited support.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Package Creation Success Response",
                summary="Successful package creation",
                description="Returns the created package details.",
                value={
                    "id": 2,
                    "name": "Basic Package",
                    "image": "http://localhost:8000/media/packages/basic_package.png",
                    "description": "Includes essential features and limited support.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-08-09T13:50:00Z",
                    "last_update_date": "2024-08-09T13:50:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Package Details",
        description="Update information of an existing package by its ID.",
        request=PackageSerializer,
        responses={
            200: OpenApiResponse(
                response=PackageSerializer,
                description="Package updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Package not found.")
        },
        tags=["Package"],
        examples=[
            OpenApiExample(
                name="Package Update Request",
                summary="Request body for updating a package",
                description="Provide fields to update for the package.",
                value={
                    "description": "Updated description for Premium Package.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Package Update Success Response",
                summary="Successful package update",
                description="Returns the updated package details.",
                value={
                    "id": 1,
                    "name": "Premium Package",
                    "image": "http://localhost:8000/media/packages/premium_package.png",
                    "description": "Updated description for Premium Package.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-07-25T10:45:00Z",
                    "last_update_date": "2024-08-13T18:25:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Package",
        description="Remove a package from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Package deleted successfully."),
            404: OpenApiResponse(description="Package not found.")
        },
        tags=["Package"],
        examples=[
            OpenApiExample(
                name="Package Deletion Success Response",
                summary="Successful package deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'status', 'is_active']
    search_fields = ['name', 'description', 'status']
    ordering_fields = ['name', 'status', 'is_active']
    ordering = ['name']
    permission_classes = [IsAuthenticated, IsEmployee]