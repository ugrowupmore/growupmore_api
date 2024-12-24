
# master/views/country.py

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from master.models.document import Document
from master.serializers import DocumentSerializer
from authuser.permissions import IsEmployee
from rest_framework.permissions import IsAuthenticated

@extend_schema_view(
    list=extend_schema(
        summary="List Documents",
        description="Retrieve a list of all documents.",
        responses={
            200: OpenApiResponse(
                response=DocumentSerializer(many=True),
                description="A list of documents."
            )
        },
        tags=["Document"],
        examples=[
            OpenApiExample(
                name="Document List Response",
                summary="Successful retrieval of document list",
                description="Returns a list of all documents with their details.",
                value=[
                    {
                        "id": 1,
                        "document_type": 1,
                        "document_type_name": "Passport",
                        "name": "John Doe Passport",
                        "image": "http://localhost:8000/media/documents/passport_john_doe.png",
                        "description": "Passport of John Doe.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-06-01T10:30:00Z",
                        "last_update_date": "2024-07-01T11:40:00Z",
                        "updated_by": None
                    },
                    # ... more documents
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Document Details",
        description="Retrieve detailed information about a specific document by its ID.",
        responses={
            200: OpenApiResponse(
                response=DocumentSerializer,
                description="Detailed information about the document."
            ),
            404: OpenApiResponse(description="Document not found.")
        },
        tags=["Document"],
        examples=[
            OpenApiExample(
                name="Document Detail Response",
                summary="Successful retrieval of document details",
                description="Returns detailed information about a specific document.",
                value={
                    "id": 1,
                    "document_type": 1,
                    "document_type_name": "Passport",
                    "name": "John Doe Passport",
                    "image": "http://localhost:8000/media/documents/passport_john_doe.png",
                    "description": "Passport of John Doe.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-06-01T10:30:00Z",
                    "last_update_date": "2024-07-01T11:40:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Document",
        description="Add a new document to the system by providing necessary details.",
        request=DocumentSerializer,
        responses={
            201: OpenApiResponse(
                response=DocumentSerializer,
                description="Document created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Document"],
        examples=[
            OpenApiExample(
                name="Document Creation Request",
                summary="Request body for creating a new document",
                description="Provide necessary fields to create a new document.",
                value={
                    "document_type": 2,
                    "name": "Jane Smith Driver's License",
                    "image": "http://localhost:8000/media/documents/drivers_license_jane_smith.png",
                    "description": "Driver's license of Jane Smith.",
                    "status": "ACTIVE",
                    "is_active": True
                }
            ),
            OpenApiExample(
                name="Document Creation Success Response",
                summary="Successful document creation",
                description="Returns the created document details.",
                value={
                    "id": 2,
                    "document_type": 2,
                    "document_type_name": "Driver's License",
                    "name": "Jane Smith Driver's License",
                    "image": "http://localhost:8000/media/documents/drivers_license_jane_smith.png",
                    "description": "Driver's license of Jane Smith.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-23T14:20:00Z",
                    "last_update_date": "2024-07-23T14:20:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Document Details",
        description="Update information of an existing document by its ID.",
        request=DocumentSerializer,
        responses={
            200: OpenApiResponse(
                response=DocumentSerializer,
                description="Document updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Document not found.")
        },
        tags=["Document"],
        examples=[
            OpenApiExample(
                name="Document Update Request",
                summary="Request body for updating a document",
                description="Provide fields to update for the document.",
                value={
                    "description": "Updated description for John Doe's Passport.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Document Update Success Response",
                summary="Successful document update",
                description="Returns the updated document details.",
                value={
                    "id": 1,
                    "document_type": 1,
                    "document_type_name": "Passport",
                    "name": "John Doe Passport",
                    "image": "http://localhost:8000/media/documents/passport_john_doe.png",
                    "description": "Updated description for John Doe's Passport.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-06-01T10:30:00Z",
                    "last_update_date": "2024-08-09T16:55:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Document",
        description="Remove a document from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Document deleted successfully."),
            404: OpenApiResponse(description="Document not found.")
        },
        tags=["Document"],
        examples=[
            OpenApiExample(
                name="Document Deletion Success Response",
                summary="Successful document deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.select_related('document_type').all()
    serializer_class = DocumentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'status', 'is_active', 'document_type']
    search_fields = ['name', 'description', 'status', 'document_type__type']
    ordering_fields = ['name', 'document_type_id', 'status', 'is_active']
    ordering = ['name']
    permission_classes = [IsAuthenticated, IsEmployee]