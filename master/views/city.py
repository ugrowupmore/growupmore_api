
# master/views/city.py

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from authuser.permissions import IsEmployee
from rest_framework.permissions import IsAuthenticated

from master.models.city import City
from master.serializers import CitySerializer

@extend_schema_view(
    list=extend_schema(
        summary="List Cities",
        description="Retrieve a list of all cities.",
        responses={
            200: OpenApiResponse(
                response=CitySerializer(many=True),
                description="A list of cities."
            )
        },
        tags=["City"],
        examples=[
            OpenApiExample(
                name="City List Response",
                summary="Successful retrieval of city list",
                description="Returns a list of all cities with their details.",
                value=[
                    {
                        "id": 1,
                        "country": 1,
                        "country_name": "United States",
                        "state": 1,
                        "state_name": "California",
                        "name": "Los Angeles",
                        "latitude": "34.05223500",
                        "longitude": "-118.24368300",
                        "location_url": "https://www.google.com/maps/place/Los+Angeles",
                        "phonecode": 1,
                        "population": 3980400,
                        "timezone": "PST",
                        "founded_date": "1781-09-04",
                        "website": "https://www.lacity.org",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-03-10T09:15:00Z",
                        "last_update_date": "2024-06-10T10:20:00Z",
                        "updated_by": None
                    },
                    # ... more cities
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve City Details",
        description="Retrieve detailed information about a specific city by its ID.",
        responses={
            200: OpenApiResponse(
                response=CitySerializer,
                description="Detailed information about the city."
            ),
            404: OpenApiResponse(description="City not found.")
        },
        tags=["City"],
        examples=[
            OpenApiExample(
                name="City Detail Response",
                summary="Successful retrieval of city details",
                description="Returns detailed information about a specific city.",
                value={
                    "id": 1,
                    "country": 1,
                    "country_name": "United States",
                    "state": 1,
                    "state_name": "California",
                    "name": "Los Angeles",
                    "latitude": "34.05223500",
                    "longitude": "-118.24368300",
                    "location_url": "https://www.google.com/maps/place/Los+Angeles",
                    "phonecode": 1,
                    "population": 3980400,
                    "timezone": "PST",
                    "founded_date": "1781-09-04",
                    "website": "https://www.lacity.org",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-03-10T09:15:00Z",
                    "last_update_date": "2024-06-10T10:20:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New City",
        description="Add a new city to the system by providing necessary details.",
        request=CitySerializer,
        responses={
            201: OpenApiResponse(
                response=CitySerializer,
                description="City created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["City"],
        examples=[
            OpenApiExample(
                name="City Creation Request",
                summary="Request body for creating a new city",
                description="Provide necessary fields to create a new city.",
                value={
                    "country": 1,
                    "state": 1,
                    "name": "San Francisco",
                    "latitude": "37.77492900",
                    "longitude": "-122.41941800",
                    "location_url": "https://www.google.com/maps/place/San+Francisco",
                    "phonecode": 1,
                    "population": 883305,
                    "timezone": "PST",
                    "founded_date": "1776-06-29",
                    "website": "https://sf.gov",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="City Creation Success Response",
                summary="Successful city creation",
                description="Returns the created city details.",
                value={
                    "id": 2,
                    "country": 1,
                    "country_name": "United States",
                    "state": 1,
                    "state_name": "California",
                    "name": "San Francisco",
                    "latitude": "37.77492900",
                    "longitude": "-122.41941800",
                    "location_url": "https://www.google.com/maps/place/San+Francisco",
                    "phonecode": 1,
                    "population": 883305,
                    "timezone": "PST",
                    "founded_date": "1776-06-29",
                    "website": "https://sf.gov",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-17T08:25:00Z",
                    "last_update_date": "2024-07-17T08:25:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update City Details",
        description="Update information of an existing city by its ID.",
        request=CitySerializer,
        responses={
            200: OpenApiResponse(
                response=CitySerializer,
                description="City updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="City not found.")
        },
        tags=["City"],
        examples=[
            OpenApiExample(
                name="City Update Request",
                summary="Request body for updating a city",
                description="Provide fields to update for the city.",
                value={
                    "name": "Los Angeles Updated",
                    "population": 4000000,
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="City Update Success Response",
                summary="Successful city update",
                description="Returns the updated city details.",
                value={
                    "id": 1,
                    "country": 1,
                    "country_name": "United States",
                    "state": 1,
                    "state_name": "California",
                    "name": "Los Angeles Updated",
                    "latitude": "34.05223500",
                    "longitude": "-118.24368300",
                    "location_url": "https://www.google.com/maps/place/Los+Angeles",
                    "phonecode": 1,
                    "population": 4000000,
                    "timezone": "PST",
                    "founded_date": "1781-09-04",
                    "website": "https://www.lacity.org",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-02-01T12:00:00Z",
                    "last_update_date": "2024-08-03T16:35:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a City",
        description="Remove a city from the system by its ID.",
        responses={
            204: OpenApiResponse(description="City deleted successfully."),
            404: OpenApiResponse(description="City not found.")
        },
        tags=["City"],
        examples=[
            OpenApiExample(
                name="City Deletion Success Response",
                summary="Successful city deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.select_related('country', 'state').all()
    serializer_class = CitySerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'status', 'is_active', 'country', 'state']
    search_fields = ['name', 'status', 'is_active']
    ordering_fields = ['name', 'country_id', 'state_id', 'status', 'is_active']
    ordering = ['name']
    permission_classes = [IsAuthenticated, IsEmployee]