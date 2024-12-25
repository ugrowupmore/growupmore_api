
# master/views/country.py

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from master.models.package_content import PackageContent
from master.serializers import PackageContentSerializer
from authuser.permissions import IsEmployee
from rest_framework.permissions import IsAuthenticated

@extend_schema_view(
    list=extend_schema(
        summary="List Package Contents",
        description="Retrieve a list of all package contents.",
        responses={
            200: OpenApiResponse(
                response=PackageContentSerializer(many=True),
                description="A list of package contents."
            )
        },
        tags=["Package Content"],
        examples=[
            OpenApiExample(
                name="Package Content List Response",
                summary="Successful retrieval of package content list",
                description="Returns a list of all package contents with their details.",
                value=[
                    {
                        "id": 1,
                        "package": 1,
                        "package_name": "Premium Package",
                        "content": 1,
                        "content_name": "Welcome Message",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-08-01T10:00:00Z",
                        "last_update_date": "2024-09-01T11:15:00Z",
                        "updated_by": None
                    },
                    # ... more package contents
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Package Content Details",
        description="Retrieve detailed information about a specific package content by its ID.",
        responses={
            200: OpenApiResponse(
                response=PackageContentSerializer,
                description="Detailed information about the package content."
            ),
            404: OpenApiResponse(description="Package content not found.")
        },
        tags=["Package Content"],
        examples=[
            OpenApiExample(
                name="Package Content Detail Response",
                summary="Successful retrieval of package content details",
                description="Returns detailed information about a specific package content.",
                value={
                    "id": 1,
                    "package": 1,
                    "package_name": "Premium Package",
                    "content": 1,
                    "content_name": "Welcome Message",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-08-01T10:00:00Z",
                    "last_update_date": "2024-09-01T11:15:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Package Content",
        description="Add a new package content to the system by providing necessary details.",
        request=PackageContentSerializer,
        responses={
            201: OpenApiResponse(
                response=PackageContentSerializer,
                description="Package content created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Package Content"],
        examples=[
            OpenApiExample(
                name="Package Content Creation Request",
                summary="Request body for creating a new package content",
                description="Provide necessary fields to create a new package content.",
                value={
                    "package": 2,
                    "content": 2,
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Package Content Creation Success Response",
                summary="Successful package content creation",
                description="Returns the created package content details.",
                value={
                    "id": 2,
                    "package": 2,
                    "package_name": "Basic Package",
                    "content": 2,
                    "content_name": "Thank You Message",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-09-02T14:25:00Z",
                    "last_update_date": "2024-09-02T14:25:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Package Content Details",
        description="Update information of an existing package content by its ID.",
        request=PackageContentSerializer,
        responses={
            200: OpenApiResponse(
                response=PackageContentSerializer,
                description="Package content updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Package content not found.")
        },
        tags=["Package Content"],
        examples=[
            OpenApiExample(
                name="Package Content Update Request",
                summary="Request body for updating a package content",
                description="Provide fields to update for the package content.",
                value={
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Package Content Update Success Response",
                summary="Successful package content update",
                description="Returns the updated package content details.",
                value={
                    "id": 1,
                    "package": 1,
                    "package_name": "Premium Package",
                    "content": 1,
                    "content_name": "Welcome Message",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-08-01T10:00:00Z",
                    "last_update_date": "2024-09-03T17:35:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Package Content",
        description="Remove a package content from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Package content deleted successfully."),
            404: OpenApiResponse(description="Package content not found.")
        },
        tags=["Package Content"],
        examples=[
            OpenApiExample(
                name="Package Content Deletion Success Response",
                summary="Successful package content deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class PackageContentViewSet(viewsets.ModelViewSet):
    queryset = PackageContent.objects.select_related('package', 'content').all()
    serializer_class = PackageContentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'is_active', 'package', 'content']
    search_fields = ['status', 'is_active', 'package__name', 'content__content']
    ordering_fields = ['package__name', 'content__content', 'status', 'is_active']
    ordering = ['package__name']
    permission_classes = [IsAuthenticated, IsEmployee]