
# master/views/country.py

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from master.models.document_type import DocumentType
from master.serializers import DocumentTypeSerializer
from authuser.permissions import IsEmployee
from rest_framework.permissions import IsAuthenticated

@extend_schema_view(
    list=extend_schema(
        summary="List Document Types",
        description="Retrieve a list of all document types.",
        responses={
            200: OpenApiResponse(
                response=DocumentTypeSerializer(many=True),
                description="A list of document types."
            )
        },
        tags=["Document Type"],
        examples=[
            OpenApiExample(
                name="Document Type List Response",
                summary="Successful retrieval of document type list",
                description="Returns a list of all document types with their details.",
                value=[
                    {
                        "id": 1,
                        "type": "Passport",
                        "image": "http://localhost:8000/media/document_types/passport.png",
                        "description": "International travel document.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-05-25T10:15:00Z",
                        "last_update_date": "2024-06-25T11:25:00Z",
                        "updated_by": None
                    },
                    # ... more document types
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Document Type Details",
        description="Retrieve detailed information about a specific document type by its ID.",
        responses={
            200: OpenApiResponse(
                response=DocumentTypeSerializer,
                description="Detailed information about the document type."
            ),
            404: OpenApiResponse(description="Document type not found.")
        },
        tags=["Document Type"],
        examples=[
            OpenApiExample(
                name="Document Type Detail Response",
                summary="Successful retrieval of document type details",
                description="Returns detailed information about a specific document type.",
                value={
                    "id": 1,
                    "type": "Passport",
                    "image": "http://localhost:8000/media/document_types/passport.png",
                    "description": "International travel document.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-05-25T10:15:00Z",
                    "last_update_date": "2024-06-25T11:25:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Document Type",
        description="Add a new document type to the system by providing necessary details.",
        request=DocumentTypeSerializer,
        responses={
            201: OpenApiResponse(
                response=DocumentTypeSerializer,
                description="Document type created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Document Type"],
        examples=[
            OpenApiExample(
                name="Document Type Creation Request",
                summary="Request body for creating a new document type",
                description="Provide necessary fields to create a new document type.",
                value={
                    "type": "Driver's License",
                    "image": "http://localhost:8000/media/document_types/drivers_license.png",
                    "description": "Official document permitting a person to drive a motor vehicle.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Document Type Creation Success Response",
                summary="Successful document type creation",
                description="Returns the created document type details.",
                value={
                    "id": 2,
                    "type": "Driver's License",
                    "image": "http://localhost:8000/media/document_types/drivers_license.png",
                    "description": "Official document permitting a person to drive a motor vehicle.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-22T12:00:00Z",
                    "last_update_date": "2024-07-22T12:00:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Document Type Details",
        description="Update information of an existing document type by its ID.",
        request=DocumentTypeSerializer,
        responses={
            200: OpenApiResponse(
                response=DocumentTypeSerializer,
                description="Document type updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Document type not found.")
        },
        tags=["Document Type"],
        examples=[
            OpenApiExample(
                name="Document Type Update Request",
                summary="Request body for updating a document type",
                description="Provide fields to update for the document type.",
                value={
                    "description": "Updated description for Passport.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Document Type Update Success Response",
                summary="Successful document type update",
                description="Returns the updated document type details.",
                value={
                    "id": 1,
                    "type": "Passport",
                    "image": "http://localhost:8000/media/document_types/passport.png",
                    "description": "Updated description for Passport.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-05-25T10:15:00Z",
                    "last_update_date": "2024-08-08T14:30:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Document Type",
        description="Remove a document type from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Document type deleted successfully."),
            404: OpenApiResponse(description="Document type not found.")
        },
        tags=["Document Type"],
        examples=[
            OpenApiExample(
                name="Document Type Deletion Success Response",
                summary="Successful document type deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class DocumentTypeViewSet(viewsets.ModelViewSet):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status', 'is_active']
    search_fields = ['type', 'description', 'status']
    ordering_fields = ['type', 'status', 'is_active']
    ordering = ['type']
    permission_classes = [IsAuthenticated, IsEmployee]