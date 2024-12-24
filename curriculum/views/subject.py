
# curriculum/views/subject.py

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

from curriculum.models.subject import Subject
from curriculum.serializers import SubjectSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List Subjects",
        description="Retrieve a list of all subjects.",
        responses={
            200: OpenApiResponse(
                response=SubjectSerializer(many=True),
                description="A list of subjects."
            )
        },
        tags=["Subject"],
        examples=[
            OpenApiExample(
                name="Subject List Response",
                summary="Successful retrieval of subject list",
                description="Returns a list of all subjects with their details.",
                value=[
                    {
                        "id": 1,
                        "name": "Mathematics",
                        "short_name": "Math",
                        "subject_code": "MATH101",
                        "image": "http://localhost:8000/media/subjects_images/math.png",
                        "image_alt": "Mathematics Image",
                        "short_intro": "Introduction to Mathematics.",
                        "long_intro": "A comprehensive course covering algebra, geometry, calculus, and more.",
                        "yt_thumb_image": "http://localhost:8000/media/subjects_yt_thumbnails/math_thumb.png",
                        "yt_thumb_image_alt": "Mathematics Thumbnail",
                        "video_url": "https://www.youtube.com/watch?v=example",
                        "video_title": "Mathematics Overview",
                        "video_description": "An overview video for the Mathematics subject.",
                        "tags": "math, algebra, geometry, calculus",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-07-10T09:00:00Z",
                        "last_update_date": "2024-07-20T10:30:00Z",
                        "updated_by": None
                    },
                    # ... more subjects
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Subject Details",
        description="Retrieve detailed information about a specific subject by its ID.",
        responses={
            200: OpenApiResponse(
                response=SubjectSerializer,
                description="Detailed information about the subject."
            ),
            404: OpenApiResponse(description="Subject not found.")
        },
        tags=["Subject"],
        examples=[
            OpenApiExample(
                name="Subject Detail Response",
                summary="Successful retrieval of subject details",
                description="Returns detailed information about a specific subject.",
                value={
                    "id": 1,
                    "name": "Mathematics",
                    "short_name": "Math",
                    "subject_code": "MATH101",
                    "image": "http://localhost:8000/media/subjects_images/math.png",
                    "image_alt": "Mathematics Image",
                    "short_intro": "Introduction to Mathematics.",
                    "long_intro": "A comprehensive course covering algebra, geometry, calculus, and more.",
                    "yt_thumb_image": "http://localhost:8000/media/subjects_yt_thumbnails/math_thumb.png",
                    "yt_thumb_image_alt": "Mathematics Thumbnail",
                    "video_url": "https://www.youtube.com/watch?v=example",
                    "video_title": "Mathematics Overview",
                    "video_description": "An overview video for the Mathematics subject.",
                    "tags": "math, algebra, geometry, calculus",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-10T09:00:00Z",
                    "last_update_date": "2024-07-20T10:30:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Subject",
        description="Add a new subject to the system by providing necessary details.",
        request=SubjectSerializer,
        responses={
            201: OpenApiResponse(
                response=SubjectSerializer,
                description="Subject created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Subject"],
        examples=[
            OpenApiExample(
                name="Subject Creation Request",
                summary="Request body for creating a new subject",
                description="Provide necessary fields to create a new subject.",
                value={
                    "name": "Physics",
                    "short_name": "Phys",
                    "subject_code": "PHYS101",
                    "image": "http://localhost:8000/media/subjects_images/physics.png",
                    "image_alt": "Physics Image",
                    "short_intro": "Introduction to Physics.",
                    "long_intro": "A comprehensive course covering mechanics, thermodynamics, electromagnetism, and more.",
                    "yt_thumb_image": "http://localhost:8000/media/subjects_yt_thumbnails/physics_thumb.png",
                    "yt_thumb_image_alt": "Physics Thumbnail",
                    "video_url": "https://www.youtube.com/watch?v=example2",
                    "video_title": "Physics Overview",
                    "video_description": "An overview video for the Physics subject.",
                    "tags": "physics, mechanics, thermodynamics, electromagnetism",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Subject Creation Success Response",
                summary="Successful subject creation",
                description="Returns the created subject details.",
                value={
                    "id": 2,
                    "name": "Physics",
                    "short_name": "Phys",
                    "subject_code": "PHYS101",
                    "image": "http://localhost:8000/media/subjects_images/physics.png",
                    "image_alt": "Physics Image",
                    "short_intro": "Introduction to Physics.",
                    "long_intro": "A comprehensive course covering mechanics, thermodynamics, electromagnetism, and more.",
                    "yt_thumb_image": "http://localhost:8000/media/subjects_yt_thumbnails/physics_thumb.png",
                    "yt_thumb_image_alt": "Physics Thumbnail",
                    "video_url": "https://www.youtube.com/watch?v=example2",
                    "video_title": "Physics Overview",
                    "video_description": "An overview video for the Physics subject.",
                    "tags": "physics, mechanics, thermodynamics, electromagnetism",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-21T11:15:00Z",
                    "last_update_date": "2024-07-21T11:15:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Subject Details",
        description="Update information of an existing subject by its ID.",
        request=SubjectSerializer,
        responses={
            200: OpenApiResponse(
                response=SubjectSerializer,
                description="Subject updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Subject not found.")
        },
        tags=["Subject"],
        examples=[
            OpenApiExample(
                name="Subject Update Request",
                summary="Request body for updating a subject",
                description="Provide fields to update for the subject.",
                value={
                    "short_intro": "Advanced Introduction to Mathematics.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Subject Update Success Response",
                summary="Successful subject update",
                description="Returns the updated subject details.",
                value={
                    "id": 1,
                    "name": "Mathematics",
                    "short_name": "Math",
                    "subject_code": "MATH101",
                    "image": "http://localhost:8000/media/subjects_images/math.png",
                    "image_alt": "Mathematics Image",
                    "short_intro": "Advanced Introduction to Mathematics.",
                    "long_intro": "A comprehensive course covering algebra, geometry, calculus, and more.",
                    "yt_thumb_image": "http://localhost:8000/media/subjects_yt_thumbnails/math_thumb.png",
                    "yt_thumb_image_alt": "Mathematics Thumbnail",
                    "video_url": "https://www.youtube.com/watch?v=example",
                    "video_title": "Mathematics Overview",
                    "video_description": "An overview video for the Mathematics subject.",
                    "tags": "math, algebra, geometry, calculus",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-07-10T09:00:00Z",
                    "last_update_date": "2024-08-05T14:20:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Subject",
        description="Remove a subject from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Subject deleted successfully."),
            404: OpenApiResponse(description="Subject not found.")
        },
        tags=["Subject"],
        examples=[
            OpenApiExample(
                name="Subject Deletion Success Response",
                summary="Successful subject deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class SubjectViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Subject instances.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'short_name', 'subject_code', 'status', 'is_active']
    search_fields = ['name', 'short_name', 'subject_code']
    ordering_fields = ['name', 'short_name', 'subject_code', 'status', 'is_active']
    ordering = ['name']
    permission_classes = [IsAuthenticated, IsEmployee]