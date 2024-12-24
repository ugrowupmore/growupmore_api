
# curriculum/views/course_category.py

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

from curriculum.models.course_category import CourseCategory
from curriculum.serializers import CourseCategorySerializer


@extend_schema_view(
    list=extend_schema(
        summary="List Courses Categories",
        description="Retrieve a list of all course categories.",
        responses={
            200: OpenApiResponse(
                response=CourseCategorySerializer(many=True),
                description="A list of course categories."
            )
        },
        tags=["CourseCategory"],
        examples=[
            OpenApiExample(
                name="CourseCategory List Response",
                summary="Successful retrieval of course category list",
                description="Returns a list of all course categories with their details.",
                value=[
                    {
                        "id": 1,
                        "category": "Science",
                        "description": "Courses related to scientific disciplines.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-07-18T09:45:00Z",
                        "last_update_date": "2024-07-28T10:55:00Z",
                        "updated_by": None
                    },
                    # ... more course categories
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve CourseCategory Details",
        description="Retrieve detailed information about a specific course category by its ID.",
        responses={
            200: OpenApiResponse(
                response=CourseCategorySerializer,
                description="Detailed information about the course category."
            ),
            404: OpenApiResponse(description="CourseCategory not found.")
        },
        tags=["CourseCategory"],
        examples=[
            OpenApiExample(
                name="CourseCategory Detail Response",
                summary="Successful retrieval of course category details",
                description="Returns detailed information about a specific course category.",
                value={
                    "id": 1,
                    "category": "Science",
                    "description": "Courses related to scientific disciplines.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-18T09:45:00Z",
                    "last_update_date": "2024-07-28T10:55:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New CourseCategory",
        description="Add a new course category to the system by providing necessary details.",
        request=CourseCategorySerializer,
        responses={
            201: OpenApiResponse(
                response=CourseCategorySerializer,
                description="CourseCategory created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["CourseCategory"],
        examples=[
            OpenApiExample(
                name="CourseCategory Creation Request",
                summary="Request body for creating a new course category",
                description="Provide necessary fields to create a new course category.",
                value={
                    "category": "Humanities",
                    "description": "Courses related to humanities and social sciences.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="CourseCategory Creation Success Response",
                summary="Successful course category creation",
                description="Returns the created course category details.",
                value={
                    "id": 2,
                    "category": "Humanities",
                    "description": "Courses related to humanities and social sciences.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-29T14:20:00Z",
                    "last_update_date": "2024-07-29T14:20:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update CourseCategory Details",
        description="Update information of an existing course category by its ID.",
        request=CourseCategorySerializer,
        responses={
            200: OpenApiResponse(
                response=CourseCategorySerializer,
                description="CourseCategory updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="CourseCategory not found.")
        },
        tags=["CourseCategory"],
        examples=[
            OpenApiExample(
                name="CourseCategory Update Request",
                summary="Request body for updating a course category",
                description="Provide fields to update for the course category.",
                value={
                    "description": "Updated description for Science courses.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="CourseCategory Update Success Response",
                summary="Successful course category update",
                description="Returns the updated course category details.",
                value={
                    "id": 1,
                    "category": "Science",
                    "description": "Updated description for Science courses.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-07-18T09:45:00Z",
                    "last_update_date": "2024-08-07T18:40:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a CourseCategory",
        description="Remove a course category from the system by its ID.",
        responses={
            204: OpenApiResponse(description="CourseCategory deleted successfully."),
            404: OpenApiResponse(description="CourseCategory not found.")
        },
        tags=["CourseCategory"],
        examples=[
            OpenApiExample(
                name="CourseCategory Deletion Success Response",
                summary="Successful course category deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class CourseCategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing CourseCategory instances.
    """
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'is_active']
    search_fields = ['category']
    ordering_fields = ['category', 'status', 'is_active']
    ordering = ['category']
    permission_classes = [IsAuthenticated, IsEmployee]