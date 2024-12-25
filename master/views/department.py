
# master/views/country.py

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from master.models.department import Department
from master.serializers import DepartmentSerializer
from authuser.permissions import IsEmployee
from rest_framework.permissions import IsAuthenticated

@extend_schema_view(
    list=extend_schema(
        summary="List Departments",
        description="Retrieve a list of all departments.",
        responses={
            200: OpenApiResponse(
                response=DepartmentSerializer(many=True),
                description="A list of departments."
            )
        },
        tags=["Department"],
        examples=[
            OpenApiExample(
                name="Department List Response",
                summary="Successful retrieval of department list",
                description="Returns a list of all departments with their details.",
                value=[
                    {
                        "id": 1,
                        "name": "Human Resources",
                        "description": "Handles recruitment, training, and employee relations.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-05-10T10:00:00Z",
                        "last_update_date": "2024-06-10T11:00:00Z",
                        "updated_by": None
                    },
                    # ... more departments
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Department Details",
        description="Retrieve detailed information about a specific department by its ID.",
        responses={
            200: OpenApiResponse(
                response=DepartmentSerializer,
                description="Detailed information about the department."
            ),
            404: OpenApiResponse(description="Department not found.")
        },
        tags=["Department"],
        examples=[
            OpenApiExample(
                name="Department Detail Response",
                summary="Successful retrieval of department details",
                description="Returns detailed information about a specific department.",
                value={
                    "id": 1,
                    "name": "Human Resources",
                    "description": "Handles recruitment, training, and employee relations.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-05-10T10:00:00Z",
                    "last_update_date": "2024-06-10T11:00:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Department",
        description="Add a new department to the system by providing necessary details.",
        request=DepartmentSerializer,
        responses={
            201: OpenApiResponse(
                response=DepartmentSerializer,
                description="Department created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Department"],
        examples=[
            OpenApiExample(
                name="Department Creation Request",
                summary="Request body for creating a new department",
                description="Provide necessary fields to create a new department.",
                value={
                    "name": "Finance",
                    "description": "Manages company finances, budgeting, and investments.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Department Creation Success Response",
                summary="Successful department creation",
                description="Returns the created department details.",
                value={
                    "id": 2,
                    "name": "Finance",
                    "description": "Manages company finances, budgeting, and investments.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-19T09:30:00Z",
                    "last_update_date": "2024-07-19T09:30:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Department Details",
        description="Update information of an existing department by its ID.",
        request=DepartmentSerializer,
        responses={
            200: OpenApiResponse(
                response=DepartmentSerializer,
                description="Department updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Department not found.")
        },
        tags=["Department"],
        examples=[
            OpenApiExample(
                name="Department Update Request",
                summary="Request body for updating a department",
                description="Provide fields to update for the department.",
                value={
                    "description": "Oversees financial planning and analysis.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Department Update Success Response",
                summary="Successful department update",
                description="Returns the updated department details.",
                value={
                    "id": 2,
                    "name": "Finance",
                    "description": "Oversees financial planning and analysis.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-07-19T09:30:00Z",
                    "last_update_date": "2024-08-05T14:00:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Department",
        description="Remove a department from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Department deleted successfully."),
            404: OpenApiResponse(description="Department not found.")
        },
        tags=["Department"],
        examples=[
            OpenApiExample(
                name="Department Deletion Success Response",
                summary="Successful department deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'status', 'is_active']
    search_fields = ['name', 'status', 'is_active']
    ordering_fields = ['name', 'status', 'is_active']
    ordering = ['name']
    permission_classes = [IsAuthenticated, IsEmployee]