
# master/views/country.py

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from master.models.country import Country
from master.serializers import CountrySerializer
from authuser.permissions import IsEmployee
from rest_framework.permissions import IsAuthenticated

@extend_schema_view(
    list=extend_schema(
        summary="List Countries",
        description="Retrieve a list of all countries.",
        responses={
            200: OpenApiResponse(
                response=CountrySerializer(many=True),
                description="A list of countries."
            )
        },
        tags=["Country"],
        examples=[
            OpenApiExample(
                name="Country List Response",
                summary="Successful retrieval of country list",
                description="Returns a list of all countries with their details.",
                value=[
                    {
                        "id": 1,
                        "name": "United States",
                        "numeric_code": 840,
                        "iso2": "US",
                        "iso3": "USA",
                        "phone_code": "+1",
                        "currency": "USD",
                        "currency_name": "United States Dollar",
                        "currency_symbol": "$",
                        "national_language": "English",
                        "nationality": "American",
                        "languages": "English",
                        "tld": ".us",
                        "website": "https://www.usa.gov",
                        "founded_date": "1776-07-04",
                        "flag_image": "http://localhost:8000/media/countries_flags/usa.png",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-01-01T12:00:00Z",
                        "last_update_date": "2024-06-01T12:00:00Z",
                        "updated_by": None
                    },
                    # ... more countries
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Country Details",
        description="Retrieve detailed information about a specific country by its ID.",
        responses={
            200: OpenApiResponse(
                response=CountrySerializer,
                description="Detailed information about the country."
            ),
            404: OpenApiResponse(description="Country not found.")
        },
        tags=["Country"],
        examples=[
            OpenApiExample(
                name="Country Detail Response",
                summary="Successful retrieval of country details",
                description="Returns detailed information about a specific country.",
                value={
                    "id": 1,
                    "name": "United States",
                    "numeric_code": 840,
                    "iso2": "US",
                    "iso3": "USA",
                    "phone_code": "+1",
                    "currency": "USD",
                    "currency_name": "United States Dollar",
                    "currency_symbol": "$",
                    "national_language": "English",
                    "nationality": "American",
                    "languages": "English",
                    "tld": ".us",
                    "website": "https://www.usa.gov",
                    "founded_date": "1776-07-04",
                    "flag_image": "http://localhost:8000/media/countries_flags/usa.png",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-01-01T12:00:00Z",
                    "last_update_date": "2024-06-01T12:00:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Country",
        description="Add a new country to the system by providing necessary details.",
        request=CountrySerializer,
        responses={
            201: OpenApiResponse(
                response=CountrySerializer,
                description="Country created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Country"],
        examples=[
            OpenApiExample(
                name="Country Creation Request",
                summary="Request body for creating a new country",
                description="Provide necessary fields to create a new country.",
                value={
                    "name": "Canada",
                    "numeric_code": 124,
                    "iso2": "CA",
                    "iso3": "CAN",
                    "phone_code": "+1",
                    "currency": "CAD",
                    "currency_name": "Canadian Dollar",
                    "currency_symbol": "$",
                    "national_language": "English, French",
                    "nationality": "Canadian",
                    "languages": "English, French",
                    "tld": ".ca",
                    "website": "https://www.canada.ca",
                    "founded_date": "1867-07-01",
                    "flag_image": "http://localhost:8000/media/countries_flags/canada.png",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Country Creation Success Response",
                summary="Successful country creation",
                description="Returns the created country details.",
                value={
                    "id": 2,
                    "name": "Canada",
                    "numeric_code": 124,
                    "iso2": "CA",
                    "iso3": "CAN",
                    "phone_code": "+1",
                    "currency": "CAD",
                    "currency_name": "Canadian Dollar",
                    "currency_symbol": "$",
                    "national_language": "English, French",
                    "nationality": "Canadian",
                    "languages": "English, French",
                    "tld": ".ca",
                    "website": "https://www.canada.ca",
                    "founded_date": "1867-07-01",
                    "flag_image": "http://localhost:8000/media/countries_flags/canada.png",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-15T10:30:00Z",
                    "last_update_date": "2024-07-15T10:30:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Country Details",
        description="Update information of an existing country by its ID.",
        request=CountrySerializer,
        responses={
            200: OpenApiResponse(
                response=CountrySerializer,
                description="Country updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Country not found.")
        },
        tags=["Country"],
        examples=[
            OpenApiExample(
                name="Country Update Request",
                summary="Request body for updating a country",
                description="Provide fields to update for the country.",
                value={
                    "name": "Canada",
                    "currency_symbol": "C$",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Country Update Success Response",
                summary="Successful country update",
                description="Returns the updated country details.",
                value={
                    "id": 2,
                    "name": "Canada",
                    "numeric_code": 124,
                    "iso2": "CA",
                    "iso3": "CAN",
                    "phone_code": "+1",
                    "currency": "CAD",
                    "currency_name": "Canadian Dollar",
                    "currency_symbol": "C$",
                    "national_language": "English, French",
                    "nationality": "Canadian",
                    "languages": "English, French",
                    "tld": ".ca",
                    "website": "https://www.canada.ca",
                    "founded_date": "1867-07-01",
                    "flag_image": "http://localhost:8000/media/countries_flags/canada.png",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-07-15T10:30:00Z",
                    "last_update_date": "2024-08-01T09:45:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Country",
        description="Remove a country from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Country deleted successfully."),
            404: OpenApiResponse(description="Country not found.")
        },
        tags=["Country"],
        examples=[
            OpenApiExample(
                name="Country Deletion Success Response",
                summary="Successful country deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'iso2', 'iso3', 'currency', 'national_language', 'nationality', 'languages', 'status', 'is_active']
    search_fields = ['name', 'iso2', 'iso3', 'currency', 'national_language', 'nationality', 'languages', 'status']
    ordering_fields = ['name', 'iso2', 'iso3', 'currency', 'national_language', 'nationality', 'languages', 'status', 'is_active']
    ordering = ['name']
    permission_classes = [IsAuthenticated, IsEmployee]