
# curriculum/views/course_subcategory.py

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

from curriculum.models.course_subcategory import CourseSubCategory
from curriculum.serializers import CourseSubCategorySerializer


@extend_schema_view(
    list=extend_schema(
        summary="List Course SubCategories",
        description="Retrieve a list of all course subcategories.",
        responses={
            200: OpenApiResponse(
                response=CourseSubCategorySerializer(many=True),
                description="A list of course subcategories."
            )
        },
        tags=["CourseSubCategory"],
        examples=[
            OpenApiExample(
                name="CourseSubCategory List Response",
                summary="Successful retrieval of course subcategory list",
                description="Returns a list of all course subcategories with their details.",
                value=[
                    {
                        "id": 1,
                        "course_category": 1,
                        "sub_category": "Physics",
                        "description": "Advanced Physics courses.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-07-19T11:00:00Z",
                        "last_update_date": "2024-07-29T12:15:00Z",
                        "updated_by": None
                    },
                    # ... more course subcategories
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve CourseSubCategory Details",
        description="Retrieve detailed information about a specific course subcategory by its ID.",
        responses={
            200: OpenApiResponse(
                response=CourseSubCategorySerializer,
                description="Detailed information about the course subcategory."
            ),
            404: OpenApiResponse(description="CourseSubCategory not found.")
        },
        tags=["CourseSubCategory"],
        examples=[
            OpenApiExample(
                name="CourseSubCategory Detail Response",
                summary="Successful retrieval of course subcategory details",
                description="Returns detailed information about a specific course subcategory.",
                value={
                    "id": 1,
                    "course_category": 1,
                    "sub_category": "Physics",
                    "description": "Advanced Physics courses.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-19T11:00:00Z",
                    "last_update_date": "2024-07-29T12:15:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New CourseSubCategory",
        description="Add a new course subcategory to the system by providing necessary details.",
        request=CourseSubCategorySerializer,
        responses={
            201: OpenApiResponse(
                response=CourseSubCategorySerializer,
                description="CourseSubCategory created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["CourseSubCategory"],
        examples=[
            OpenApiExample(
                name="CourseSubCategory Creation Request",
                summary="Request body for creating a new course subcategory",
                description="Provide necessary fields to create a new course subcategory.",
                value={
                    "course_category": 1,
                    "sub_category": "Chemistry",
                    "description": "Advanced Chemistry courses.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="CourseSubCategory Creation Success Response",
                summary="Successful course subcategory creation",
                description="Returns the created course subcategory details.",
                value={
                    "id": 2,
                    "course_category": 1,
                    "sub_category": "Chemistry",
                    "description": "Advanced Chemistry courses.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-30T15:25:00Z",
                    "last_update_date": "2024-07-30T15:25:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update CourseSubCategory Details",
        description="Update information of an existing course subcategory by its ID.",
        request=CourseSubCategorySerializer,
        responses={
            200: OpenApiResponse(
                response=CourseSubCategorySerializer,
                description="CourseSubCategory updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="CourseSubCategory not found.")
        },
        tags=["CourseSubCategory"],
        examples=[
            OpenApiExample(
                name="CourseSubCategory Update Request",
                summary="Request body for updating a course subcategory",
                description="Provide fields to update for the course subcategory.",
                value={
                    "description": "Updated description for Physics courses.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="CourseSubCategory Update Success Response",
                summary="Successful course subcategory update",
                description="Returns the updated course subcategory details.",
                value={
                    "id": 1,
                    "course_category": 1,
                    "sub_category": "Physics",
                    "description": "Updated description for Physics courses.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-07-19T11:00:00Z",
                    "last_update_date": "2024-08-06T18:40:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a CourseSubCategory",
        description="Remove a course subcategory from the system by its ID.",
        responses={
            204: OpenApiResponse(description="CourseSubCategory deleted successfully."),
            404: OpenApiResponse(description="CourseSubCategory not found.")
        },
        tags=["CourseSubCategory"],
        examples=[
            OpenApiExample(
                name="CourseSubCategory Deletion Success Response",
                summary="Successful course subcategory deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class CourseSubCategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing CourseSubCategory instances.
    """
    queryset = CourseSubCategory.objects.select_related('course_category').all()
    serializer_class = CourseSubCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sub_category', 'status', 'is_active', 'course_category__category']
    search_fields = ['sub_category', 'course_category__category']
    ordering_fields = ['sub_category', 'course_category__category', 'status', 'is_active']
    ordering = ['sub_category']
    permission_classes = [IsAuthenticated, IsEmployee]