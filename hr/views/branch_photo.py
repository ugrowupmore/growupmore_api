
# hr/views/branch_photo.py

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from authuser.permissions import IsEmployee
from hr.models.branch_photo import BranchPhoto
from hr.serializers import BranchPhotoSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List Branch Photos",
        description="Retrieve a list of all branch photos.",
        responses={
            200: OpenApiResponse(
                response=BranchPhotoSerializer(many=True),
                description="A list of branch photos."
            )
        },
        tags=["Branch Photo"],
        examples=[
            OpenApiExample(
                name="Branch Photo List Response",
                summary="Successful retrieval of branch photo list",
                description="Returns a list of all branch photos with their details.",
                value=[
                    {
                        "id": 1,
                        "branch": 1,
                        "branch_name": "Downtown Branch",
                        "image": "http://localhost:8000/media/branch_photos/downtown_photo1.png",
                        "title": "Main Lobby",
                        "alt_text": "Lobby of Downtown Branch",
                        "description": "Spacious main lobby area.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-08-05T10:30:00Z",
                        "last_update_date": "2024-09-05T11:40:00Z",
                        "updated_by": None
                    },
                    # ... more branch photos
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Branch Photo Details",
        description="Retrieve detailed information about a specific branch photo by its ID.",
        responses={
            200: OpenApiResponse(
                response=BranchPhotoSerializer,
                description="Detailed information about the branch photo."
            ),
            404: OpenApiResponse(description="Branch photo not found.")
        },
        tags=["Branch Photo"],
        examples=[
            OpenApiExample(
                name="Branch Photo Detail Response",
                summary="Successful retrieval of branch photo details",
                description="Returns detailed information about a specific branch photo.",
                value={
                    "id": 1,
                    "branch": 1,
                    "branch_name": "Downtown Branch",
                    "image": "http://localhost:8000/media/branch_photos/downtown_photo1.png",
                    "title": "Main Lobby",
                    "alt_text": "Lobby of Downtown Branch",
                    "description": "Spacious main lobby area.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-08-05T10:30:00Z",
                    "last_update_date": "2024-09-05T11:40:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Branch Photo",
        description="Add a new branch photo to the system by providing necessary details.",
        request=BranchPhotoSerializer,
        responses={
            201: OpenApiResponse(
                response=BranchPhotoSerializer,
                description="Branch photo created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Branch Photo"],
        examples=[
            OpenApiExample(
                name="Branch Photo Creation Request",
                summary="Request body for creating a new branch photo",
                description="Provide necessary fields to create a new branch photo.",
                value={
                    "branch": 2,
                    "image": "http://localhost:8000/media/branch_photos/uptown_photo1.png",
                    "title": "Reception Area",
                    "alt_text": "Reception of Uptown Branch",
                    "description": "Modern reception area with seating.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Branch Photo Creation Success Response",
                summary="Successful branch photo creation",
                description="Returns the created branch photo details.",
                value={
                    "id": 2,
                    "branch": 2,
                    "branch_name": "Uptown Branch",
                    "image": "http://localhost:8000/media/branch_photos/uptown_photo1.png",
                    "title": "Reception Area",
                    "alt_text": "Reception of Uptown Branch",
                    "description": "Modern reception area with seating.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-09-09T14:30:00Z",
                    "last_update_date": "2024-09-09T14:30:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Branch Photo Details",
        description="Update information of an existing branch photo by its ID.",
        request=BranchPhotoSerializer,
        responses={
            200: OpenApiResponse(
                response=BranchPhotoSerializer,
                description="Branch photo updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Branch photo not found.")
        },
        tags=["Branch Photo"],
        examples=[
            OpenApiExample(
                name="Branch Photo Update Request",
                summary="Request body for updating a branch photo",
                description="Provide fields to update for the branch photo.",
                value={
                    "description": "Updated description for Main Lobby photo.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Branch Photo Update Success Response",
                summary="Successful branch photo update",
                description="Returns the updated branch photo details.",
                value={
                    "id": 1,
                    "branch": 1,
                    "branch_name": "Downtown Branch",
                    "image": "http://localhost:8000/media/branch_photos/downtown_photo1.png",
                    "title": "Main Lobby",
                    "alt_text": "Lobby of Downtown Branch",
                    "description": "Updated description for Main Lobby photo.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-08-05T10:30:00Z",
                    "last_update_date": "2024-09-10T16:20:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Branch Photo",
        description="Remove a branch photo from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Branch photo deleted successfully."),
            404: OpenApiResponse(description="Branch photo not found.")
        },
        tags=["Branch Photo"],
        examples=[
            OpenApiExample(
                name="Branch Photo Deletion Success Response",
                summary="Successful branch photo deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class BranchPhotoViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing branch photo instances.
    """
    queryset = BranchPhoto.objects.select_related('branch').all()
    serializer_class = BranchPhotoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['branch', 'status', 'is_active']
    search_fields = ['title']
    ordering_fields = ['title', 'branch', 'status', 'is_active']
    ordering = ['title']
    permission_classes = [IsAuthenticated, IsEmployee]