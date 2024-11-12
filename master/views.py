# master/views.py

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from master.models.bank import Bank
from master.models.branch_type import BranchType
from master.models.campaign_type import CampaignType
from master.models.city import City
from master.models.communication_type import CommunicationType
from master.models.content import Content
from master.models.country import Country
from master.models.course_category import CourseCategory
from master.models.course_sub_category import CourseSubCategory
from master.models.department import Department
from master.models.designation import Designation
from master.models.document import Document
from master.models.document_type import DocumentType
from master.models.event_type import EventType
from master.models.faq_category import FAQCategory
from master.models.marketing_type import MarketingType
from master.models.offer_type import OfferType
from master.models.package import Package
from master.models.package_content import PackageContent
from master.models.promotion_type import PromotionType
from master.models.service_category import ServiceCategory
from master.models.social_status import SocialStatus
from master.models.state import State
from master.models.ticket_type import TicketType
from .serializers import (
    CountrySerializer, StateSerializer, CitySerializer, BankSerializer, DepartmentSerializer,
    DesignationSerializer, SocialStatusSerializer, DocumentTypeSerializer,
    DocumentSerializer, BranchTypeSerializer, PackageSerializer, ContentSerializer,
    PackageContentSerializer, ServiceCategorySerializer, CourseCategorySerializer,
    CourseSubCategorySerializer, FAQCategorySerializer,
    CampaignTypeSerializer, CommunicationTypeSerializer, 
    EventTypeSerializer, MarketingTypeSerializer, OfferTypeSerializer, 
    PromotionTypeSerializer, TicketTypeSerializer )


# Country ViewSet
class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'iso2', 'iso3', 'currency', 'national_language', 'nationality', 'languages', 'status', 'is_active']
    search_fields = ['name', 'iso2', 'iso3', 'currency', 'national_language', 'nationality', 'languages', 'status']
    ordering_fields = ['name', 'iso2', 'iso3', 'currency', 'national_language', 'nationality', 'languages', 'status', 'is_active']
    ordering = ['name']

# State ViewSet
class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.select_related('country').all()
    serializer_class = StateSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'status', 'is_active', 'country']
    search_fields = ['name', 'status', 'is_active']
    ordering_fields = '__all__'
    ordering = ['name']

# City ViewSet
class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.select_related('country', 'state').all()
    serializer_class = CitySerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'status', 'is_active', 'country', 'state']
    search_fields = ['name', 'status', 'is_active']
    filterset_fields = '__all__'
    ordering = ['name']

# Bank ViewSet
class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.select_related('country').all()
    serializer_class = BankSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'status', 'is_active', 'country', 'swift_code', 'iban_code']
    search_fields = ['name', 'status', 'is_active', 'country', 'swift_code', 'iban_code']
    ordering_fields = '__all__'
    ordering = ['name']

# Department ViewSet
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'status', 'is_active']
    search_fields = ['name', 'status', 'is_active']
    ordering_fields = '__all__'
    ordering = ['name']

# Designation ViewSet
class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'status', 'is_active', 'level', 'travel_required', 'training_required']
    search_fields = ['name', 'status', 'is_active', 'level']
    ordering_fields = '__all__'
    ordering = ['name']

# SocialStatus ViewSet
class SocialStatusViewSet(viewsets.ModelViewSet):
    queryset = SocialStatus.objects.all()
    serializer_class = SocialStatusSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'status', 'is_active']
    search_fields = ['name', 'status', 'is_active']
    ordering_fields = '__all__'
    ordering = ['name']

# DocumentType ViewSet
class DocumentTypeViewSet(viewsets.ModelViewSet):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status', 'is_active']
    search_fields = ['type', 'status', 'is_active']
    ordering_fields = ['type', 'status', 'is_active']
    ordering = ['type']

# Document ViewSet
class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.select_related('document_type').all()
    serializer_class = DocumentSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'status', 'is_active', 'document_type']
    search_fields = ['name', 'status', 'is_active', 'document_type']
    ordering_fields = '__all__'
    ordering = ['name']

# BranchType ViewSet
class BranchTypeViewSet(viewsets.ModelViewSet):
    queryset = BranchType.objects.all()
    serializer_class = BranchTypeSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status', 'is_active']
    search_fields = ['type', 'status', 'is_active']
    ordering_fields = '__all__'
    ordering = ['type']

# Package ViewSet
class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'status', 'is_active']
    filterset_fields = ['name', 'status', 'is_active']
    ordering_fields = '__all__'
    ordering = ['name']

# Content ViewSet
class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['content', 'status', 'is_active']
    search_fields = ['content', 'status', 'is_active']
    ordering_fields = '__all__'
    ordering = ['content']

# PackageContent ViewSet
class PackageContentViewSet(viewsets.ModelViewSet):
    queryset = PackageContent.objects.select_related('package', 'content').all()
    serializer_class = PackageContentSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'is_active', 'package', 'content']
    search_fields = ['status', 'is_active']
    ordering_fields = '__all__'
    ordering = ['package']

# ServiceCategory ViewSet
class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'is_active']
    search_fields = ['category', 'status', 'is_active']
    ordering_fields = '__all__'
    ordering = ['category']

# CourseCategory ViewSet
class CourseCategoryViewSet(viewsets.ModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'is_active']
    search_fields = ['category', 'status', 'is_active']
    ordering_fields = '__all__'
    ordering = ['category']

# CourseSubCategory ViewSet
class CourseSubCategoryViewSet(viewsets.ModelViewSet):
    queryset = CourseSubCategory.objects.select_related('course_category').all()
    serializer_class = CourseSubCategorySerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sub_category', 'status', 'is_active', 'course_category__category']
    search_fields = ['sub_category', 'status', 'is_active', 'course_category__category']
    ordering_fields = '__all__'
    ordering = ['sub_category']

# FAQCategory ViewSet
class FAQCategoryViewSet(viewsets.ModelViewSet):
    queryset = FAQCategory.objects.all()
    serializer_class = FAQCategorySerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'is_active']
    search_fields = ['category', 'status', 'is_active']
    ordering_fields = '__all__'
    ordering = ['category']

# CampaignType Viewset
class CampaignTypeViewSet(viewsets.ModelViewSet):
    queryset = CampaignType.objects.all()
    serializer_class = CampaignTypeSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status', 'is_active']
    search_fields = ['type', 'status', 'is_active']
    ordering_fields = '__all__'
    ordering = ['type']

# CommunicationType Viewset
class CommunicationTypeViewSet(viewsets.ModelViewSet):
    queryset = CommunicationType.objects.all()
    serializer_class = CommunicationTypeSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status', 'is_active']
    search_fields = ['type', 'status', 'is_active']
    ordering_fields = '__all__'
    ordering = ['type']

# EventType Viewset
class EventTypeViewSet(viewsets.ModelViewSet):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status', 'is_active']
    search_fields = ['type', 'status', 'is_active']
    ordering_fields = '__all__'
    ordering = ['type']

# MarketingType Viewset
class MarketingTypeViewSet(viewsets.ModelViewSet):
    queryset = MarketingType.objects.all()
    serializer_class = MarketingTypeSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status', 'is_active']
    search_fields = ['type', 'status', 'is_active']
    ordering_fields = '__all__'
    ordering = ['type']

# OfferType Viewset
class OfferTypeViewSet(viewsets.ModelViewSet):
    queryset = OfferType.objects.all()
    serializer_class = OfferTypeSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status', 'is_active']
    search_fields = ['type', 'status', 'is_active']
    ordering_fields = '__all__'
    ordering = ['type']

# PromotionType Viewset
class PromotionTypeViewSet(viewsets.ModelViewSet):
    queryset = PromotionType.objects.all()
    serializer_class = PromotionTypeSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status', 'is_active']
    search_fields = ['type', 'status', 'is_active']
    ordering_fields = '__all__'
    ordering = ['type']

# TicketType Viewset
class TicketTypeViewSet(viewsets.ModelViewSet):
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status', 'is_active']
    search_fields = ['type', 'status', 'is_active']
    ordering_fields = '__all__'
    ordering = ['type']