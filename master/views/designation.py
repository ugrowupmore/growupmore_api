
# master/views/country.py

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from master.models.designation import Designation
from master.serializers import DesignationSerializer
from authuser.permissions import IsEmployee
from rest_framework.permissions import IsAuthenticated

@extend_schema_view(
    list=extend_schema(
        summary="List Designations",
        description="Retrieve a list of all designations.",
        responses={
            200: OpenApiResponse(
                response=DesignationSerializer(many=True),
                description="A list of designations."
            )
        },
        tags=["Designation"],
        examples=[
            OpenApiExample(
                name="Designation List Response",
                summary="Successful retrieval of designation list",
                description="Returns a list of all designations with their details.",
                value=[
                    {
                        "id": 1,
                        "name": "Software Engineer",
                        "level": "MID",
                        "travel_required": True,
                        "training_required": True,
                        "description": "Responsible for developing and maintaining software applications.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-05-20T10:00:00Z",
                        "last_update_date": "2024-06-20T11:00:00Z",
                        "updated_by": None
                    },
                    # ... more designations
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Designation Details",
        description="Retrieve detailed information about a specific designation by its ID.",
        responses={
            200: OpenApiResponse(
                response=DesignationSerializer,
                description="Detailed information about the designation."
            ),
            404: OpenApiResponse(description="Designation not found.")
        },
        tags=["Designation"],
        examples=[
            OpenApiExample(
                name="Designation Detail Response",
                summary="Successful retrieval of designation details",
                description="Returns detailed information about a specific designation.",
                value={
                    "id": 1,
                    "name": "Software Engineer",
                    "level": "MID",
                    "travel_required": True,
                    "training_required": True,
                    "description": "Responsible for developing and maintaining software applications.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-05-20T10:00:00Z",
                    "last_update_date": "2024-06-20T11:00:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Designation",
        description="Add a new designation to the system by providing necessary details.",
        request=DesignationSerializer,
        responses={
            201: OpenApiResponse(
                response=DesignationSerializer,
                description="Designation created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Designation"],
        examples=[
            OpenApiExample(
                name="Designation Creation Request",
                summary="Request body for creating a new designation",
                description="Provide necessary fields to create a new designation.",
                value={
                    "name": "Senior Software Engineer",
                    "level": "SENIOR",
                    "travel_required": False,
                    "training_required": True,
                    "description": "Leads software development projects and mentors junior engineers.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Designation Creation Success Response",
                summary="Successful designation creation",
                description="Returns the created designation details.",
                value={
                    "id": 2,
                    "name": "Senior Software Engineer",
                    "level": "SENIOR",
                    "travel_required": False,
                    "training_required": True,
                    "description": "Leads software development projects and mentors junior engineers.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-21T09:30:00Z",
                    "last_update_date": "2024-07-21T09:30:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Designation Details",
        description="Update information of an existing designation by its ID.",
        request=DesignationSerializer,
        responses={
            200: OpenApiResponse(
                response=DesignationSerializer,
                description="Designation updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Designation not found.")
        },
        tags=["Designation"],
        examples=[
            OpenApiExample(
                name="Designation Update Request",
                summary="Request body for updating a designation",
                description="Provide fields to update for the designation.",
                value={
                    "level": "LEAD",
                    "travel_required": True
                }
            ),
            OpenApiExample(
                name="Designation Update Success Response",
                summary="Successful designation update",
                description="Returns the updated designation details.",
                value={
                    "id": 2,
                    "name": "Senior Software Engineer",
                    "level": "LEAD",
                    "travel_required": True,
                    "training_required": True,
                    "description": "Leads software development projects and mentors junior engineers.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-21T09:30:00Z",
                    "last_update_date": "2024-08-07T15:45:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Designation",
        description="Remove a designation from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Designation deleted successfully."),
            404: OpenApiResponse(description="Designation not found.")
        },
        tags=["Designation"],
        examples=[
            OpenApiExample(
                name="Designation Deletion Success Response",
                summary="Successful designation deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'level', 'travel_required', 'training_required', 'status', 'is_active']
    search_fields = ['name', 'level', 'description', 'status']
    ordering_fields = ['name', 'level', 'status', 'is_active']
    ordering = ['name']
    permission_classes = [IsAuthenticated, IsEmployee]