
# curriculum/views/subtopic.py

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

from curriculum.models.subtopic import Subtopic
from curriculum.serializers import SubTopicSerializer

@extend_schema_view(
    list=extend_schema(
        summary="List SubTopics",
        description="Retrieve a list of all subtopics.",
        responses={
            200: OpenApiResponse(
                response=SubTopicSerializer(many=True),
                description="A list of subtopics."
            )
        },
        tags=["SubTopic"],
        examples=[
            OpenApiExample(
                name="SubTopic List Response",
                summary="Successful retrieval of subtopic list",
                description="Returns a list of all subtopics with their details.",
                value=[
                    {
                        "id": 1,
                        "topic": 1,
                        "name": "Solving Linear Equations",
                        "image": "http://localhost:8000/media/subtopics_images/solving_linear.png",
                        "image_alt": "Solving Linear Equations Image",
                        "short_intro": "Techniques for solving linear equations.",
                        "long_intro": "Detailed methods and examples for solving linear equations.",
                        "yt_thumb_image": "http://localhost:8000/media/subtopics_yt_thumbnails/solving_linear_thumb.png",
                        "yt_thumb_image_alt": "Solving Linear Equations Thumbnail",
                        "video_url": "https://www.youtube.com/watch?v=subtopic_example",
                        "video_title": "Solving Linear Equations",
                        "video_description": "A video demonstrating techniques for solving linear equations.",
                        "tags": "linear, equations, solving",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-07-16T10:15:00Z",
                        "last_update_date": "2024-07-26T11:25:00Z",
                        "updated_by": None
                    },
                    # ... more subtopics
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve SubTopic Details",
        description="Retrieve detailed information about a specific subtopic by its ID.",
        responses={
            200: OpenApiResponse(
                response=SubTopicSerializer,
                description="Detailed information about the subtopic."
            ),
            404: OpenApiResponse(description="SubTopic not found.")
        },
        tags=["SubTopic"],
        examples=[
            OpenApiExample(
                name="SubTopic Detail Response",
                summary="Successful retrieval of subtopic details",
                description="Returns detailed information about a specific subtopic.",
                value={
                    "id": 1,
                    "topic": 1,
                    "name": "Solving Linear Equations",
                    "image": "http://localhost:8000/media/subtopics_images/solving_linear.png",
                    "image_alt": "Solving Linear Equations Image",
                    "short_intro": "Techniques for solving linear equations.",
                    "long_intro": "Detailed methods and examples for solving linear equations.",
                    "yt_thumb_image": "http://localhost:8000/media/subtopics_yt_thumbnails/solving_linear_thumb.png",
                    "yt_thumb_image_alt": "Solving Linear Equations Thumbnail",
                    "video_url": "https://www.youtube.com/watch?v=subtopic_example",
                    "video_title": "Solving Linear Equations",
                    "video_description": "A video demonstrating techniques for solving linear equations.",
                    "tags": "linear, equations, solving",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-16T10:15:00Z",
                    "last_update_date": "2024-07-26T11:25:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New SubTopic",
        description="Add a new subtopic to the system by providing necessary details.",
        request=SubTopicSerializer,
        responses={
            201: OpenApiResponse(
                response=SubTopicSerializer,
                description="SubTopic created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["SubTopic"],
        examples=[
            OpenApiExample(
                name="SubTopic Creation Request",
                summary="Request body for creating a new subtopic",
                description="Provide necessary fields to create a new subtopic.",
                value={
                    "topic": 1,
                    "name": "Graphing Linear Equations",
                    "image": "http://localhost:8000/media/subtopics_images/graphing_linear.png",
                    "image_alt": "Graphing Linear Equations Image",
                    "short_intro": "Visual methods for graphing linear equations.",
                    "long_intro": "Learn how to graph linear equations and interpret their graphs.",
                    "yt_thumb_image": "http://localhost:8000/media/subtopics_yt_thumbnails/graphing_linear_thumb.png",
                    "yt_thumb_image_alt": "Graphing Linear Equations Thumbnail",
                    "video_url": "https://www.youtube.com/watch?v=graphing_linear_example",
                    "video_title": "Graphing Linear Equations",
                    "video_description": "A video tutorial on graphing linear equations.",
                    "tags": "linear, equations, graphing",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="SubTopic Creation Success Response",
                summary="Successful subtopic creation",
                description="Returns the created subtopic details.",
                value={
                    "id": 2,
                    "topic": 1,
                    "name": "Graphing Linear Equations",
                    "image": "http://localhost:8000/media/subtopics_images/graphing_linear.png",
                    "image_alt": "Graphing Linear Equations Image",
                    "short_intro": "Visual methods for graphing linear equations.",
                    "long_intro": "Learn how to graph linear equations and interpret their graphs.",
                    "yt_thumb_image": "http://localhost:8000/media/subtopics_yt_thumbnails/graphing_linear_thumb.png",
                    "yt_thumb_image_alt": "Graphing Linear Equations Thumbnail",
                    "video_url": "https://www.youtube.com/watch?v=graphing_linear_example",
                    "video_title": "Graphing Linear Equations",
                    "video_description": "A video tutorial on graphing linear equations.",
                    "tags": "linear, equations, graphing",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-27T14:30:00Z",
                    "last_update_date": "2024-07-27T14:30:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update SubTopic Details",
        description="Update information of an existing subtopic by its ID.",
        request=SubTopicSerializer,
        responses={
            200: OpenApiResponse(
                response=SubTopicSerializer,
                description="SubTopic updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="SubTopic not found.")
        },
        tags=["SubTopic"],
        examples=[
            OpenApiExample(
                name="SubTopic Update Request",
                summary="Request body for updating a subtopic",
                description="Provide fields to update for the subtopic.",
                value={
                    "long_intro": "Enhanced methods for graphing and analyzing linear equations.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="SubTopic Update Success Response",
                summary="Successful subtopic update",
                description="Returns the updated subtopic details.",
                value={
                    "id": 1,
                    "topic": 1,
                    "name": "Solving Linear Equations",
                    "image": "http://localhost:8000/media/subtopics_images/solving_linear.png",
                    "image_alt": "Solving Linear Equations Image",
                    "short_intro": "Techniques for solving linear equations.",
                    "long_intro": "Enhanced methods and examples for solving linear equations.",
                    "yt_thumb_image": "http://localhost:8000/media/subtopics_yt_thumbnails/solving_linear_thumb.png",
                    "yt_thumb_image_alt": "Solving Linear Equations Thumbnail",
                    "video_url": "https://www.youtube.com/watch?v=subtopic_example",
                    "video_title": "Solving Linear Equations",
                    "video_description": "An explanatory video on linear equations.",
                    "tags": "linear, equations, solving",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-07-16T10:15:00Z",
                    "last_update_date": "2024-08-04T17:50:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a SubTopic",
        description="Remove a subtopic from the system by its ID.",
        responses={
            204: OpenApiResponse(description="SubTopic deleted successfully."),
            404: OpenApiResponse(description="SubTopic not found.")
        },
        tags=["SubTopic"],
        examples=[
            OpenApiExample(
                name="SubTopic Deletion Success Response",
                summary="Successful subtopic deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class SubTopicViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing SubTopic instances.
    """
    queryset = Subtopic.objects.select_related('topic__chapter__subject').all()
    serializer_class = SubTopicSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'topic__chapter__subject',
        'topic__chapter',
        'topic',
        'status',
        'is_active'
    ]
    search_fields = ['name']
    ordering_fields = ['name', 'topic', 'status', 'is_active']
    ordering = ['name']
    permission_classes = [IsAuthenticated, IsEmployee]