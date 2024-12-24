
# master/views/country.py

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from master.models.campaign_type import CampaignType
from master.serializers import CampaignTypeSerializer
from authuser.permissions import IsEmployee
from rest_framework.permissions import IsAuthenticated

@extend_schema_view(
    list=extend_schema(
        summary="List Campaign Types",
        description="Retrieve a list of all campaign types.",
        responses={
            200: OpenApiResponse(
                response=CampaignTypeSerializer(many=True),
                description="A list of campaign types."
            )
        },
        tags=["Campaign Type"],
        examples=[
            OpenApiExample(
                name="Campaign Type List Response",
                summary="Successful retrieval of campaign type list",
                description="Returns a list of all campaign types with their details.",
                value=[
                    {
                        "id": 1,
                        "type": "Email Marketing",
                        "description": "Campaigns using email to reach customers.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-07-05T11:00:00Z",
                        "last_update_date": "2024-08-05T12:10:00Z",
                        "updated_by": None
                    },
                    # ... more campaign types
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Campaign Type Details",
        description="Retrieve detailed information about a specific campaign type by its ID.",
        responses={
            200: OpenApiResponse(
                response=CampaignTypeSerializer,
                description="Detailed information about the campaign type."
            ),
            404: OpenApiResponse(description="Campaign type not found.")
        },
        tags=["Campaign Type"],
        examples=[
            OpenApiExample(
                name="Campaign Type Detail Response",
                summary="Successful retrieval of campaign type details",
                description="Returns detailed information about a specific campaign type.",
                value={
                    "id": 1,
                    "type": "Email Marketing",
                    "description": "Campaigns using email to reach customers.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-05T11:00:00Z",
                    "last_update_date": "2024-08-05T12:10:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Campaign Type",
        description="Add a new campaign type to the system by providing necessary details.",
        request=CampaignTypeSerializer,
        responses={
            201: OpenApiResponse(
                response=CampaignTypeSerializer,
                description="Campaign type created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Campaign Type"],
        examples=[
            OpenApiExample(
                name="Campaign Type Creation Request",
                summary="Request body for creating a new campaign type",
                description="Provide necessary fields to create a new campaign type.",
                value={
                    "type": "Social Media Marketing",
                    "description": "Campaigns leveraging social media platforms to engage customers.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Campaign Type Creation Success Response",
                summary="Successful campaign type creation",
                description="Returns the created campaign type details.",
                value={
                    "id": 2,
                    "type": "Social Media Marketing",
                    "description": "Campaigns leveraging social media platforms to engage customers.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-08-06T14:25:00Z",
                    "last_update_date": "2024-08-06T14:25:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Campaign Type Details",
        description="Update information of an existing campaign type by its ID.",
        request=CampaignTypeSerializer,
        responses={
            200: OpenApiResponse(
                response=CampaignTypeSerializer,
                description="Campaign type updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Campaign type not found.")
        },
        tags=["Campaign Type"],
        examples=[
            OpenApiExample(
                name="Campaign Type Update Request",
                summary="Request body for updating a campaign type",
                description="Provide fields to update for the campaign type.",
                value={
                    "description": "Updated description for Email Marketing.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Campaign Type Update Success Response",
                summary="Successful campaign type update",
                description="Returns the updated campaign type details.",
                value={
                    "id": 1,
                    "type": "Email Marketing",
                    "description": "Updated description for Email Marketing.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-07-05T11:00:00Z",
                    "last_update_date": "2024-08-11T16:35:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Campaign Type",
        description="Remove a campaign type from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Campaign type deleted successfully."),
            404: OpenApiResponse(description="Campaign type not found.")
        },
        tags=["Campaign Type"],
        examples=[
            OpenApiExample(
                name="Campaign Type Deletion Success Response",
                summary="Successful campaign type deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class CampaignTypeViewSet(viewsets.ModelViewSet):
    queryset = CampaignType.objects.all()
    serializer_class = CampaignTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status', 'is_active']
    search_fields = ['type', 'description', 'status']
    ordering_fields = ['type', 'status', 'is_active']
    ordering = ['type']
    permission_classes = [IsAuthenticated, IsEmployee]