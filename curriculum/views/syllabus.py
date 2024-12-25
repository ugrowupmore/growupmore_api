
# curriculum/views/syllabus.py

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

from curriculum.models.syllabus import Syllabus
from curriculum.serializers import SyllabusSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List Syllabuses",
        description="Retrieve a list of all syllabuses.",
        responses={
            200: OpenApiResponse(
                response=SyllabusSerializer(many=True),
                description="A list of syllabuses."
            )
        },
        tags=["Syllabus"],
        examples=[
            OpenApiExample(
                name="Syllabus List Response",
                summary="Successful retrieval of syllabus list",
                description="Returns a list of all syllabuses with their details.",
                value=[
                    {
                        "id": 1,
                        "course": 1,
                        "module": 1,
                        "subject": 1,
                        "chapter": 1,
                        "topic": 1,
                        "name": "Week 1: Basics",
                        "content": "Introduction to the course and foundational concepts.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-07-22T12:20:00Z",
                        "last_update_date": "2024-08-01T13:35:00Z",
                        "updated_by": None
                    },
                    # ... more syllabuses
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Syllabus Details",
        description="Retrieve detailed information about a specific syllabus by its ID.",
        responses={
            200: OpenApiResponse(
                response=SyllabusSerializer,
                description="Detailed information about the syllabus."
            ),
            404: OpenApiResponse(description="Syllabus not found.")
        },
        tags=["Syllabus"],
        examples=[
            OpenApiExample(
                name="Syllabus Detail Response",
                summary="Successful retrieval of syllabus details",
                description="Returns detailed information about a specific syllabus.",
                value={
                    "id": 1,
                    "course": 1,
                    "module": 1,
                    "subject": 1,
                    "chapter": 1,
                    "topic": 1,
                    "name": "Week 1: Basics",
                    "content": "Introduction to the course and foundational concepts.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-22T12:20:00Z",
                    "last_update_date": "2024-08-01T13:35:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Syllabus",
        description="Add a new syllabus to the system by providing necessary details.",
        request=SyllabusSerializer,
        responses={
            201: OpenApiResponse(
                response=SyllabusSerializer,
                description="Syllabus created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Syllabus"],
        examples=[
            OpenApiExample(
                name="Syllabus Creation Request",
                summary="Request body for creating a new syllabus",
                description="Provide necessary fields to create a new syllabus.",
                value={
                    "course": 1,
                    "module": 1,
                    "subject": 1,
                    "chapter": 1,
                    "topic": 1,
                    "name": "Week 2: Intermediate Concepts",
                    "content": "Exploration of intermediate topics and practical applications.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Syllabus Creation Success Response",
                summary="Successful syllabus creation",
                description="Returns the created syllabus details.",
                value={
                    "id": 2,
                    "course": 1,
                    "module": 1,
                    "subject": 1,
                    "chapter": 1,
                    "topic": 1,
                    "name": "Week 2: Intermediate Concepts",
                    "content": "Exploration of intermediate topics and practical applications.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-08-02T14:50:00Z",
                    "last_update_date": "2024-08-02T14:50:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Syllabus Details",
        description="Update information of an existing syllabus by its ID.",
        request=SyllabusSerializer,
        responses={
            200: OpenApiResponse(
                response=SyllabusSerializer,
                description="Syllabus updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Syllabus not found.")
        },
        tags=["Syllabus"],
        examples=[
            OpenApiExample(
                name="Syllabus Update Request",
                summary="Request body for updating a syllabus",
                description="Provide fields to update for the syllabus.",
                value={
                    "content": "Updated content for Week 1, including additional exercises.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Syllabus Update Success Response",
                summary="Successful syllabus update",
                description="Returns the updated syllabus details.",
                value={
                    "id": 1,
                    "course": 1,
                    "module": 1,
                    "subject": 1,
                    "chapter": 1,
                    "topic": 1,
                    "name": "Week 1: Basics",
                    "content": "Updated content for Week 1, including additional exercises.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-07-22T12:20:00Z",
                    "last_update_date": "2024-08-03T19:10:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Syllabus",
        description="Remove a syllabus from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Syllabus deleted successfully."),
            404: OpenApiResponse(description="Syllabus not found.")
        },
        tags=["Syllabus"],
        examples=[
            OpenApiExample(
                name="Syllabus Deletion Success Response",
                summary="Successful syllabus deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class SyllabusViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Syllabus instances.
    """
    queryset = Syllabus.objects.select_related(
        'course',
        'module',
        'subject',
        'chapter',
        'topic'
    ).all()
    serializer_class = SyllabusSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'course',
        'module',
        'subject',
        'chapter',
        'topic',
        'status',
        'is_active'
    ]
    search_fields = []
    ordering_fields = ['course__name', 'module__module_name', 'subject__name', 'chapter__name', 'topic__name', 'status', 'is_active']
    ordering = ['course__name']
    permission_classes = [IsAuthenticated, IsEmployee]