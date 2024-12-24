
# curriculum/views/module.py

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

from curriculum.models.course import Course
from curriculum.models.module import Module
from curriculum.serializers import CourseSerializer, ModuleSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List Modules",
        description="Retrieve a list of all modules.",
        responses={
            200: OpenApiResponse(
                response=ModuleSerializer(many=True),
                description="A list of modules."
            )
        },
        tags=["Module"],
        examples=[
            OpenApiExample(
                name="Module List Response",
                summary="Successful retrieval of module list",
                description="Returns a list of all modules with their details.",
                value=[
                    {
                        "id": 1,
                        "course": 1,
                        "module_name": "Introduction to Programming",
                        "short_intro": "Basics of programming.",
                        "long_intro": "Covers fundamental programming concepts, including variables, control structures, and data types.",
                        "description": "An introductory module on programming fundamentals.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-07-21T11:30:00Z",
                        "last_update_date": "2024-07-31T12:40:00Z",
                        "updated_by": None
                    },
                    # ... more modules
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Module Details",
        description="Retrieve detailed information about a specific module by its ID.",
        responses={
            200: OpenApiResponse(
                response=ModuleSerializer,
                description="Detailed information about the module."
            ),
            404: OpenApiResponse(description="Module not found.")
        },
        tags=["Module"],
        examples=[
            OpenApiExample(
                name="Module Detail Response",
                summary="Successful retrieval of module details",
                description="Returns detailed information about a specific module.",
                value={
                    "id": 1,
                    "course": 1,
                    "module_name": "Introduction to Programming",
                    "short_intro": "Basics of programming.",
                    "long_intro": "Covers fundamental programming concepts, including variables, control structures, and data types.",
                    "description": "An introductory module on programming fundamentals.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-21T11:30:00Z",
                    "last_update_date": "2024-07-31T12:40:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Module",
        description="Add a new module to the system by providing necessary details.",
        request=ModuleSerializer,
        responses={
            201: OpenApiResponse(
                response=ModuleSerializer,
                description="Module created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Module"],
        examples=[
            OpenApiExample(
                name="Module Creation Request",
                summary="Request body for creating a new module",
                description="Provide necessary fields to create a new module.",
                value={
                    "course": 1,
                    "module_name": "Advanced Programming Concepts",
                    "short_intro": "Deep dive into programming.",
                    "long_intro": "Explores advanced programming topics such as object-oriented programming, recursion, and algorithm optimization.",
                    "description": "An advanced module on programming concepts.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Module Creation Success Response",
                summary="Successful module creation",
                description="Returns the created module details.",
                value={
                    "id": 2,
                    "course": 1,
                    "module_name": "Advanced Programming Concepts",
                    "short_intro": "Deep dive into programming.",
                    "long_intro": "Explores advanced programming topics such as object-oriented programming, recursion, and algorithm optimization.",
                    "description": "An advanced module on programming concepts.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-08-01T14:50:00Z",
                    "last_update_date": "2024-08-01T14:50:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Module Details",
        description="Update information of an existing module by its ID.",
        request=ModuleSerializer,
        responses={
            200: OpenApiResponse(
                response=ModuleSerializer,
                description="Module updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Module not found.")
        },
        tags=["Module"],
        examples=[
            OpenApiExample(
                name="Module Update Request",
                summary="Request body for updating a module",
                description="Provide fields to update for the module.",
                value={
                    "long_intro": "Updated exploration of advanced programming topics including concurrency and design patterns.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Module Update Success Response",
                summary="Successful module update",
                description="Returns the updated module details.",
                value={
                    "id": 1,
                    "course": 1,
                    "module_name": "Introduction to Programming",
                    "short_intro": "Basics of programming.",
                    "long_intro": "Updated exploration of fundamental programming concepts, including variables, control structures, and data types.",
                    "description": "An introductory module on programming fundamentals.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-07-21T11:30:00Z",
                    "last_update_date": "2024-08-02T17:00:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Module",
        description="Remove a module from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Module deleted successfully."),
            404: OpenApiResponse(description="Module not found.")
        },
        tags=["Module"],
        examples=[
            OpenApiExample(
                name="Module Deletion Success Response",
                summary="Successful module deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class ModuleViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Module instances.
    """
    queryset = Module.objects.select_related('course').all()
    serializer_class = ModuleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['course', 'module_name', 'status', 'is_active']
    search_fields = ['module_name']
    ordering_fields = ['module_name', 'course', 'status', 'is_active']
    ordering = ['module_name']
    permission_classes = [IsAuthenticated, IsEmployee]