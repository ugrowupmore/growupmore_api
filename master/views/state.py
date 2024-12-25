
# master/views/state.py

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from master.models.state import State
from master.serializers import StateSerializer
from authuser.permissions import IsEmployee
from rest_framework.permissions import IsAuthenticated

@extend_schema_view(
    list=extend_schema(
        summary="List States",
        description="Retrieve a list of all states.",
        responses={
            200: OpenApiResponse(
                response=StateSerializer(many=True),
                description="A list of states."
            )
        },
        tags=["State"],
        examples=[
            OpenApiExample(
                name="State List Response",
                summary="Successful retrieval of state list",
                description="Returns a list of all states with their details.",
                value=[
                    {
                        "id": 1,
                        "country": 1,
                        "country_name": "United States",
                        "name": "California",
                        "founded_date": "1850-09-09",
                        "website": "https://www.ca.gov",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-02-01T12:00:00Z",
                        "last_update_date": "2024-06-01T12:00:00Z",
                        "updated_by": None
                    },
                    # ... more states
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve State Details",
        description="Retrieve detailed information about a specific state by its ID.",
        responses={
            200: OpenApiResponse(
                response=StateSerializer,
                description="Detailed information about the state."
            ),
            404: OpenApiResponse(description="State not found.")
        },
        tags=["State"],
        examples=[
            OpenApiExample(
                name="State Detail Response",
                summary="Successful retrieval of state details",
                description="Returns detailed information about a specific state.",
                value={
                    "id": 1,
                    "country": 1,
                    "country_name": "United States",
                    "name": "California",
                    "founded_date": "1850-09-09",
                    "website": "https://www.ca.gov",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-02-01T12:00:00Z",
                    "last_update_date": "2024-06-01T12:00:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New State",
        description="Add a new state to the system by providing necessary details.",
        request=StateSerializer,
        responses={
            201: OpenApiResponse(
                response=StateSerializer,
                description="State created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["State"],
        examples=[
            OpenApiExample(
                name="State Creation Request",
                summary="Request body for creating a new state",
                description="Provide necessary fields to create a new state.",
                value={
                    "country": 1,
                    "name": "Texas",
                    "founded_date": "1845-12-29",
                    "website": "https://www.texas.gov",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="State Creation Success Response",
                summary="Successful state creation",
                description="Returns the created state details.",
                value={
                    "id": 2,
                    "country": 1,
                    "country_name": "United States",
                    "name": "Texas",
                    "founded_date": "1845-12-29",
                    "website": "https://www.texas.gov",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-16T11:20:00Z",
                    "last_update_date": "2024-07-16T11:20:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update State Details",
        description="Update information of an existing state by its ID.",
        request=StateSerializer,
        responses={
            200: OpenApiResponse(
                response=StateSerializer,
                description="State updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="State not found.")
        },
        tags=["State"],
        examples=[
            OpenApiExample(
                name="State Update Request",
                summary="Request body for updating a state",
                description="Provide fields to update for the state.",
                value={
                    "name": "New California",
                    "website": "https://www.newca.gov",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="State Update Success Response",
                summary="Successful state update",
                description="Returns the updated state details.",
                value={
                    "id": 1,
                    "country": 1,
                    "country_name": "United States",
                    "name": "New California",
                    "founded_date": "1850-09-09",
                    "website": "https://www.newca.gov",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-02-01T12:00:00Z",
                    "last_update_date": "2024-08-02T14:50:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a State",
        description="Remove a state from the system by its ID.",
        responses={
            204: OpenApiResponse(description="State deleted successfully."),
            404: OpenApiResponse(description="State not found.")
        },
        tags=["State"],
        examples=[
            OpenApiExample(
                name="State Deletion Success Response",
                summary="Successful state deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.select_related('country').all()
    serializer_class = StateSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'status', 'is_active', 'country']
    search_fields = ['name', 'status', 'is_active']
    ordering_fields = ['name', 'country_id', 'status', 'is_active']
    ordering = ['name']
    permission_classes = [IsAuthenticated, IsEmployee]