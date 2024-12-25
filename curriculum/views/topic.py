
# curriculum/views/topic.py

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

from curriculum.models.topic import Topic
from curriculum.serializers import TopicSerializer

@extend_schema_view(
    list=extend_schema(
        summary="List Topics",
        description="Retrieve a list of all topics.",
        responses={
            200: OpenApiResponse(
                response=TopicSerializer(many=True),
                description="A list of topics."
            )
        },
        tags=["Topic"],
        examples=[
            OpenApiExample(
                name="Topic List Response",
                summary="Successful retrieval of topic list",
                description="Returns a list of all topics with their details.",
                value=[
                    {
                        "id": 1,
                        "chapter": 1,
                        "name": "Linear Equations",
                        "short_intro": "Understanding linear equations.",
                        "long_intro": "Detailed study of linear equations, solutions, and applications.",
                        "yt_thumb_image": "http://localhost:8000/media/topic_yt_thumbnails/linear_equations_thumb.png",
                        "yt_thumb_image_alt": "Linear Equations Thumbnail",
                        "video_url": "https://www.youtube.com/watch?v=topic_example",
                        "video_title": "Linear Equations Explained",
                        "video_description": "An explanatory video on linear equations.",
                        "tags": "linear, equations, algebra",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-07-14T08:30:00Z",
                        "last_update_date": "2024-07-24T09:45:00Z",
                        "updated_by": None
                    },
                    # ... more topics
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Topic Details",
        description="Retrieve detailed information about a specific topic by its ID.",
        responses={
            200: OpenApiResponse(
                response=TopicSerializer,
                description="Detailed information about the topic."
            ),
            404: OpenApiResponse(description="Topic not found.")
        },
        tags=["Topic"],
        examples=[
            OpenApiExample(
                name="Topic Detail Response",
                summary="Successful retrieval of topic details",
                description="Returns detailed information about a specific topic.",
                value={
                    "id": 1,
                    "chapter": 1,
                    "name": "Linear Equations",
                    "short_intro": "Understanding linear equations.",
                    "long_intro": "Detailed study of linear equations, solutions, and applications.",
                    "yt_thumb_image": "http://localhost:8000/media/topic_yt_thumbnails/linear_equations_thumb.png",
                    "yt_thumb_image_alt": "Linear Equations Thumbnail",
                    "video_url": "https://www.youtube.com/watch?v=topic_example",
                    "video_title": "Linear Equations Explained",
                    "video_description": "An explanatory video on linear equations.",
                    "tags": "linear, equations, algebra",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-14T08:30:00Z",
                    "last_update_date": "2024-07-24T09:45:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Topic",
        description="Add a new topic to the system by providing necessary details.",
        request=TopicSerializer,
        responses={
            201: OpenApiResponse(
                response=TopicSerializer,
                description="Topic created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Topic"],
        examples=[
            OpenApiExample(
                name="Topic Creation Request",
                summary="Request body for creating a new topic",
                description="Provide necessary fields to create a new topic.",
                value={
                    "chapter": 1,
                    "name": "Quadratic Equations",
                    "short_intro": "Introduction to quadratic equations.",
                    "long_intro": "Exploration of quadratic equations, solutions, and their graphs.",
                    "yt_thumb_image": "http://localhost:8000/media/topic_yt_thumbnails/quadratic_equations_thumb.png",
                    "yt_thumb_image_alt": "Quadratic Equations Thumbnail",
                    "video_url": "https://www.youtube.com/watch?v=quadratic_example",
                    "video_title": "Quadratic Equations Introduction",
                    "video_description": "An introductory video on quadratic equations.",
                    "tags": "quadratic, equations, algebra",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Topic Creation Success Response",
                summary="Successful topic creation",
                description="Returns the created topic details.",
                value={
                    "id": 2,
                    "chapter": 1,
                    "name": "Quadratic Equations",
                    "short_intro": "Introduction to quadratic equations.",
                    "long_intro": "Exploration of quadratic equations, solutions, and their graphs.",
                    "yt_thumb_image": "http://localhost:8000/media/topic_yt_thumbnails/quadratic_equations_thumb.png",
                    "yt_thumb_image_alt": "Quadratic Equations Thumbnail",
                    "video_url": "https://www.youtube.com/watch?v=quadratic_example",
                    "video_title": "Quadratic Equations Introduction",
                    "video_description": "An introductory video on quadratic equations.",
                    "tags": "quadratic, equations, algebra",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-25T13:00:00Z",
                    "last_update_date": "2024-07-25T13:00:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Topic Details",
        description="Update information of an existing topic by its ID.",
        request=TopicSerializer,
        responses={
            200: OpenApiResponse(
                response=TopicSerializer,
                description="Topic updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Topic not found.")
        },
        tags=["Topic"],
        examples=[
            OpenApiExample(
                name="Topic Update Request",
                summary="Request body for updating a topic",
                description="Provide fields to update for the topic.",
                value={
                    "long_intro": "Advanced study of quadratic equations and their applications.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Topic Update Success Response",
                summary="Successful topic update",
                description="Returns the updated topic details.",
                value={
                    "id": 1,
                    "chapter": 1,
                    "name": "Linear Equations",
                    "short_intro": "Understanding linear equations.",
                    "long_intro": "Advanced study of linear equations, solutions, and applications.",
                    "yt_thumb_image": "http://localhost:8000/media/topic_yt_thumbnails/linear_equations_thumb.png",
                    "yt_thumb_image_alt": "Linear Equations Thumbnail",
                    "video_url": "https://www.youtube.com/watch?v=topic_example",
                    "video_title": "Linear Equations Explained",
                    "video_description": "An explanatory video on linear equations.",
                    "tags": "linear, equations, algebra",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-07-14T08:30:00Z",
                    "last_update_date": "2024-08-03T16:00:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Topic",
        description="Remove a topic from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Topic deleted successfully."),
            404: OpenApiResponse(description="Topic not found.")
        },
        tags=["Topic"],
        examples=[
            OpenApiExample(
                name="Topic Deletion Success Response",
                summary="Successful topic deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class TopicViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Topic instances.
    """
    queryset = Topic.objects.select_related('chapter__subject').all()
    serializer_class = TopicSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['chapter__subject', 'chapter', 'status', 'is_active']
    search_fields = ['name']
    ordering_fields = ['name', 'chapter', 'status', 'is_active']
    ordering = ['name']
    permission_classes = [IsAuthenticated, IsEmployee]