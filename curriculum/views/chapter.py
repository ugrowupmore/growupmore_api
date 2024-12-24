
# curriculum/views/chapter.py

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

from curriculum.models.chapter import Chapter
from curriculum.serializers import ChapterSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List Chapters",
        description="Retrieve a list of all chapters.",
        responses={
            200: OpenApiResponse(
                response=ChapterSerializer(many=True),
                description="A list of chapters."
            )
        },
        tags=["Chapter"],
        examples=[
            OpenApiExample(
                name="Chapter List Response",
                summary="Successful retrieval of chapter list",
                description="Returns a list of all chapters with their details.",
                value=[
                    {
                        "id": 1,
                        "subject": 1,
                        "name": "Algebra Basics",
                        "short_intro": "Introduction to Algebra.",
                        "long_intro": "Covers fundamental concepts of algebra including variables, equations, and functions.",
                        "yt_thumb_image": "http://localhost:8000/media/chapters_yt_thumbnails/algebra_thumb.png",
                        "yt_thumb_image_alt": "Algebra Thumbnail",
                        "video_url": "https://www.youtube.com/watch?v=chapter_example",
                        "video_title": "Algebra Basics Overview",
                        "video_description": "An overview video for Algebra Basics chapter.",
                        "tags": "algebra, equations, functions",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-07-12T10:00:00Z",
                        "last_update_date": "2024-07-22T11:30:00Z",
                        "updated_by": None
                    },
                    # ... more chapters
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Chapter Details",
        description="Retrieve detailed information about a specific chapter by its ID.",
        responses={
            200: OpenApiResponse(
                response=ChapterSerializer,
                description="Detailed information about the chapter."
            ),
            404: OpenApiResponse(description="Chapter not found.")
        },
        tags=["Chapter"],
        examples=[
            OpenApiExample(
                name="Chapter Detail Response",
                summary="Successful retrieval of chapter details",
                description="Returns detailed information about a specific chapter.",
                value={
                    "id": 1,
                    "subject": 1,
                    "name": "Algebra Basics",
                    "short_intro": "Introduction to Algebra.",
                    "long_intro": "Covers fundamental concepts of algebra including variables, equations, and functions.",
                    "yt_thumb_image": "http://localhost:8000/media/chapters_yt_thumbnails/algebra_thumb.png",
                    "yt_thumb_image_alt": "Algebra Thumbnail",
                    "video_url": "https://www.youtube.com/watch?v=chapter_example",
                    "video_title": "Algebra Basics Overview",
                    "video_description": "An overview video for Algebra Basics chapter.",
                    "tags": "algebra, equations, functions",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-12T10:00:00Z",
                    "last_update_date": "2024-07-22T11:30:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Chapter",
        description="Add a new chapter to the system by providing necessary details.",
        request=ChapterSerializer,
        responses={
            201: OpenApiResponse(
                response=ChapterSerializer,
                description="Chapter created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Chapter"],
        examples=[
            OpenApiExample(
                name="Chapter Creation Request",
                summary="Request body for creating a new chapter",
                description="Provide necessary fields to create a new chapter.",
                value={
                    "subject": 1,
                    "name": "Calculus Introduction",
                    "short_intro": "Introduction to Calculus.",
                    "long_intro": "Covers the basics of differential and integral calculus.",
                    "yt_thumb_image": "http://localhost:8000/media/chapters_yt_thumbnails/calculus_thumb.png",
                    "yt_thumb_image_alt": "Calculus Thumbnail",
                    "video_url": "https://www.youtube.com/watch?v=calculus_example",
                    "video_title": "Calculus Introduction",
                    "video_description": "An introduction video for Calculus chapter.",
                    "tags": "calculus, derivatives, integrals",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Chapter Creation Success Response",
                summary="Successful chapter creation",
                description="Returns the created chapter details.",
                value={
                    "id": 2,
                    "subject": 1,
                    "name": "Calculus Introduction",
                    "short_intro": "Introduction to Calculus.",
                    "long_intro": "Covers the basics of differential and integral calculus.",
                    "yt_thumb_image": "http://localhost:8000/media/chapters_yt_thumbnails/calculus_thumb.png",
                    "yt_thumb_image_alt": "Calculus Thumbnail",
                    "video_url": "https://www.youtube.com/watch?v=calculus_example",
                    "video_title": "Calculus Introduction",
                    "video_description": "An introduction video for Calculus chapter.",
                    "tags": "calculus, derivatives, integrals",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-23T12:45:00Z",
                    "last_update_date": "2024-07-23T12:45:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Chapter Details",
        description="Update information of an existing chapter by its ID.",
        request=ChapterSerializer,
        responses={
            200: OpenApiResponse(
                response=ChapterSerializer,
                description="Chapter updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Chapter not found.")
        },
        tags=["Chapter"],
        examples=[
            OpenApiExample(
                name="Chapter Update Request",
                summary="Request body for updating a chapter",
                description="Provide fields to update for the chapter.",
                value={
                    "short_intro": "Advanced Introduction to Algebra.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Chapter Update Success Response",
                summary="Successful chapter update",
                description="Returns the updated chapter details.",
                value={
                    "id": 1,
                    "subject": 1,
                    "name": "Algebra Basics",
                    "short_intro": "Advanced Introduction to Algebra.",
                    "long_intro": "Covers fundamental concepts of algebra including variables, equations, and functions.",
                    "yt_thumb_image": "http://localhost:8000/media/chapters_yt_thumbnails/algebra_thumb.png",
                    "yt_thumb_image_alt": "Algebra Thumbnail",
                    "video_url": "https://www.youtube.com/watch?v=chapter_example",
                    "video_title": "Algebra Basics Overview",
                    "video_description": "An overview video for Algebra Basics chapter.",
                    "tags": "algebra, equations, functions",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-07-12T10:00:00Z",
                    "last_update_date": "2024-08-02T15:00:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Chapter",
        description="Remove a chapter from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Chapter deleted successfully."),
            404: OpenApiResponse(description="Chapter not found.")
        },
        tags=["Chapter"],
        examples=[
            OpenApiExample(
                name="Chapter Deletion Success Response",
                summary="Successful chapter deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class ChapterViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Chapter instances.
    """
    queryset = Chapter.objects.select_related('subject').all()
    serializer_class = ChapterSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['subject', 'status', 'is_active']
    search_fields = ['name']
    ordering_fields = ['name', 'subject', 'status', 'is_active']
    ordering = ['name']
    permission_classes = [IsAuthenticated, IsEmployee]