
# hr/views/branch_document.py

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
from hr.models.branch_document import BranchDocument
from hr.serializers import BranchDocumentSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List Branch Documents",
        description="Retrieve a list of all branch documents.",
        responses={
            200: OpenApiResponse(
                response=BranchDocumentSerializer(many=True),
                description="A list of branch documents."
            )
        },
        tags=["Branch Document"],
        examples=[
            OpenApiExample(
                name="Branch Document List Response",
                summary="Successful retrieval of branch document list",
                description="Returns a list of all branch documents with their details.",
                value=[
                    {
                        "id": 1,
                        "branch": 1,
                        "branch_name": "Downtown Branch",
                        "document_type": 2,
                        "document_type_name": "Business License",
                        "document": 5,
                        "document_name": "General Business License",
                        "document_number": "BL-123456",
                        "issue_date": "2024-01-15",
                        "expiry_date": "2025-01-14",
                        "issue_country": 1,
                        "issue_country_name": "Countryland",
                        "issue_state": 5,
                        "issue_state_name": "Stateland",
                        "issue_city": 10,
                        "issue_city_name": "Cityville",
                        "description": "Valid business license for operations.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-07-28T12:00:00Z",
                        "last_update_date": "2024-08-28T13:10:00Z",
                        "updated_by": None
                    },
                    # ... more branch documents
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Branch Document Details",
        description="Retrieve detailed information about a specific branch document by its ID.",
        responses={
            200: OpenApiResponse(
                response=BranchDocumentSerializer,
                description="Detailed information about the branch document."
            ),
            404: OpenApiResponse(description="Branch document not found.")
        },
        tags=["Branch Document"],
        examples=[
            OpenApiExample(
                name="Branch Document Detail Response",
                summary="Successful retrieval of branch document details",
                description="Returns detailed information about a specific branch document.",
                value={
                    "id": 1,
                    "branch": 1,
                    "branch_name": "Downtown Branch",
                    "document_type": 2,
                    "document_type_name": "Business License",
                    "document": 5,
                    "document_name": "General Business License",
                    "document_number": "BL-123456",
                    "issue_date": "2024-01-15",
                    "expiry_date": "2025-01-14",
                    "issue_country": 1,
                    "issue_country_name": "Countryland",
                    "issue_state": 5,
                    "issue_state_name": "Stateland",
                    "issue_city": 10,
                    "issue_city_name": "Cityville",
                    "description": "Valid business license for operations.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-28T12:00:00Z",
                    "last_update_date": "2024-08-28T13:10:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Branch Document",
        description="Add a new branch document to the system by providing necessary details.",
        request=BranchDocumentSerializer,
        responses={
            201: OpenApiResponse(
                response=BranchDocumentSerializer,
                description="Branch document created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Branch Document"],
        examples=[
            OpenApiExample(
                name="Branch Document Creation Request",
                summary="Request body for creating a new branch document",
                description="Provide necessary fields to create a new branch document.",
                value={
                    "branch": 2,
                    "document_type": 3,
                    "document": 6,
                    "document_number": "BL-654321",
                    "issue_date": "2024-02-20",
                    "expiry_date": "2026-02-19",
                    "issue_country": 1,
                    "issue_state": 5,
                    "issue_city": 12,
                    "description": "Updated business license for Uptown Branch.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Branch Document Creation Success Response",
                summary="Successful branch document creation",
                description="Returns the created branch document details.",
                value={
                    "id": 2,
                    "branch": 2,
                    "branch_name": "Uptown Branch",
                    "document_type": 3,
                    "document_type_name": "Health Permit",
                    "document": 6,
                    "document_name": "General Health Permit",
                    "document_number": "BL-654321",
                    "issue_date": "2024-02-20",
                    "expiry_date": "2026-02-19",
                    "issue_country": 1,
                    "issue_country_name": "Countryland",
                    "issue_state": 5,
                    "issue_state_name": "Stateland",
                    "issue_city": 12,
                    "issue_city_name": "Uptown City",
                    "description": "Updated business license for Uptown Branch.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-09-08T14:30:00Z",
                    "last_update_date": "2024-09-08T14:30:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Branch Document Details",
        description="Update information of an existing branch document by its ID.",
        request=BranchDocumentSerializer,
        responses={
            200: OpenApiResponse(
                response=BranchDocumentSerializer,
                description="Branch document updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Branch document not found.")
        },
        tags=["Branch Document"],
        examples=[
            OpenApiExample(
                name="Branch Document Update Request",
                summary="Request body for updating a branch document",
                description="Provide fields to update for the branch document.",
                value={
                    "description": "Updated description for Business License.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Branch Document Update Success Response",
                summary="Successful branch document update",
                description="Returns the updated branch document details.",
                value={
                    "id": 1,
                    "branch": 1,
                    "branch_name": "Downtown Branch",
                    "document_type": 2,
                    "document_type_name": "Business License",
                    "document": 5,
                    "document_name": "General Business License",
                    "document_number": "BL-123456",
                    "issue_date": "2024-01-15",
                    "expiry_date": "2025-01-14",
                    "issue_country": 1,
                    "issue_country_name": "Countryland",
                    "issue_state": 5,
                    "issue_state_name": "Stateland",
                    "issue_city": 10,
                    "issue_city_name": "Cityville",
                    "description": "Updated description for Business License.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-07-28T12:00:00Z",
                    "last_update_date": "2024-09-09T16:20:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Branch Document",
        description="Remove a branch document from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Branch document deleted successfully."),
            404: OpenApiResponse(description="Branch document not found.")
        },
        tags=["Branch Document"],
        examples=[
            OpenApiExample(
                name="Branch Document Deletion Success Response",
                summary="Successful branch document deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class BranchDocumentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing branch document instances.
    """
    queryset = BranchDocument.objects.select_related(
        'branch',
        'document_type',
        'document',
        'issue_country',
        'issue_state',
        'issue_city'
    ).all()
    serializer_class = BranchDocumentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['branch', 'document_type', 'issue_country', 'issue_state', 'issue_city', 'status', 'is_active']
    search_fields = ['document_number']
    ordering_fields = ['document_number', 'branch', 'document_type', 'status', 'is_active']
    ordering = ['document_number']
    permission_classes = [IsAuthenticated, IsEmployee]