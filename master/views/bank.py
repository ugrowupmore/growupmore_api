
# master/views/country.py

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

from master.models.bank import Bank
from master.serializers import BankSerializer

@extend_schema_view(
    list=extend_schema(
        summary="List Banks",
        description="Retrieve a list of all banks.",
        responses={
            200: OpenApiResponse(
                response=BankSerializer(many=True),
                description="A list of banks."
            )
        },
        tags=["Bank"],
        examples=[
            OpenApiExample(
                name="Bank List Response",
                summary="Successful retrieval of bank list",
                description="Returns a list of all banks with their details.",
                value=[
                    {
                        "id": 1,
                        "name": "Bank of America",
                        "country": 1,
                        "country_name": "United States",
                        "swift_code": "BOFAUS3N",
                        "iban_code": "US12345678901234567890123456",
                        "description": "A major American multinational investment bank and financial services company.",
                        "status": "ACTIVE",
                        "is_active": True,
                        "create_date": "2024-04-05T14:30:00Z",
                        "last_update_date": "2024-06-05T15:45:00Z",
                        "updated_by": None
                    },
                    # ... more banks
                ]
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve Bank Details",
        description="Retrieve detailed information about a specific bank by its ID.",
        responses={
            200: OpenApiResponse(
                response=BankSerializer,
                description="Detailed information about the bank."
            ),
            404: OpenApiResponse(description="Bank not found.")
        },
        tags=["Bank"],
        examples=[
            OpenApiExample(
                name="Bank Detail Response",
                summary="Successful retrieval of bank details",
                description="Returns detailed information about a specific bank.",
                value={
                    "id": 1,
                    "name": "Bank of America",
                    "country": 1,
                    "country_name": "United States",
                    "swift_code": "BOFAUS3N",
                    "iban_code": "US12345678901234567890123456",
                    "description": "A major American multinational investment bank and financial services company.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-04-05T14:30:00Z",
                    "last_update_date": "2024-06-05T15:45:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    create=extend_schema(
        summary="Create a New Bank",
        description="Add a new bank to the system by providing necessary details.",
        request=BankSerializer,
        responses={
            201: OpenApiResponse(
                response=BankSerializer,
                description="Bank created successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors.")
        },
        tags=["Bank"],
        examples=[
            OpenApiExample(
                name="Bank Creation Request",
                summary="Request body for creating a new bank",
                description="Provide necessary fields to create a new bank.",
                value={
                    "name": "Chase Bank",
                    "country": 1,
                    "swift_code": "CHASUS33",
                    "iban_code": "US98765432109876543210987654",
                    "description": "A large national bank headquartered in San Francisco."
                }
            ),
            OpenApiExample(
                name="Bank Creation Success Response",
                summary="Successful bank creation",
                description="Returns the created bank details.",
                value={
                    "id": 2,
                    "name": "Chase Bank",
                    "country": 1,
                    "country_name": "United States",
                    "swift_code": "CHASUS33",
                    "iban_code": "US98765432109876543210987654",
                    "description": "A large national bank headquartered in San Francisco.",
                    "status": "ACTIVE",
                    "is_active": True,
                    "create_date": "2024-07-18T10:00:00Z",
                    "last_update_date": "2024-07-18T10:00:00Z",
                    "updated_by": None
                }
            )
        ]
    ),
    update=extend_schema(
        summary="Update Bank Details",
        description="Update information of an existing bank by its ID.",
        request=BankSerializer,
        responses={
            200: OpenApiResponse(
                response=BankSerializer,
                description="Bank updated successfully."
            ),
            400: OpenApiResponse(description="Bad Request. Validation errors."),
            404: OpenApiResponse(description="Bank not found.")
        },
        tags=["Bank"],
        examples=[
            OpenApiExample(
                name="Bank Update Request",
                summary="Request body for updating a bank",
                description="Provide fields to update for the bank.",
                value={
                    "description": "Updated description for Chase Bank.",
                    "is_active": False
                }
            ),
            OpenApiExample(
                name="Bank Update Success Response",
                summary="Successful bank update",
                description="Returns the updated bank details.",
                value={
                    "id": 2,
                    "name": "Chase Bank",
                    "country": 1,
                    "country_name": "United States",
                    "swift_code": "CHASUS33",
                    "iban_code": "US98765432109876543210987654",
                    "description": "Updated description for Chase Bank.",
                    "status": "ACTIVE",
                    "is_active": False,
                    "create_date": "2024-07-18T10:00:00Z",
                    "last_update_date": "2024-08-04T17:10:00Z",
                    "updated_by": 1
                }
            )
        ]
    ),
    destroy=extend_schema(
        summary="Delete a Bank",
        description="Remove a bank from the system by its ID.",
        responses={
            204: OpenApiResponse(description="Bank deleted successfully."),
            404: OpenApiResponse(description="Bank not found.")
        },
        tags=["Bank"],
        examples=[
            OpenApiExample(
                name="Bank Deletion Success Response",
                summary="Successful bank deletion",
                description="No content returned upon successful deletion.",
                value={}
            )
        ]
    )
)
class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.select_related('country').all()
    serializer_class = BankSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'status', 'is_active', 'country', 'swift_code', 'iban_code']
    search_fields = ['name', 'status', 'is_active', 'country__name', 'swift_code', 'iban_code']
    ordering_fields = ['name', 'country_id', 'swift_code', 'iban_code', 'status', 'is_active']
    ordering = ['name']
    permission_classes = [IsAuthenticated, IsEmployee]