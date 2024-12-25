from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CountryViewSet, StateViewSet, CityViewSet, BankViewSet, DepartmentViewSet, 
    DesignationViewSet, SocialStatusViewSet, DocumentTypeViewSet, DocumentViewSet, 
    BranchTypeViewSet, PackageViewSet, ContentViewSet, PackageContentViewSet, 
    ServiceCategoryViewSet, FAQCategoryViewSet,
    CampaignTypeViewSet, CommunicationTypeViewSet, 
    EventTypeViewSet, MarketingTypeViewSet, OfferTypeViewSet, 
    PromotionTypeViewSet, TicketTypeViewSet
)

# Initialize the router
router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'states', StateViewSet, basename='state')
router.register(r'cities', CityViewSet, basename='city')
router.register(r'banks', BankViewSet, basename='bank')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'designations', DesignationViewSet, basename='designation')
router.register(r'social-status', SocialStatusViewSet, basename='social-status')
router.register(r'document-types', DocumentTypeViewSet, basename='document-type')
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'branch-types', BranchTypeViewSet, basename='branch-type')
router.register(r'packages', PackageViewSet, basename='package')
router.register(r'contents', ContentViewSet, basename='content')
router.register(r'package-contents', PackageContentViewSet, basename='package-content')
router.register(r'service-categories', ServiceCategoryViewSet, basename='service-category')
router.register(r'faq-categories', FAQCategoryViewSet, basename='faq-category')
router.register(r'campaign-types', CampaignTypeViewSet, basename='campaign-type')
router.register(r'communication-types', CommunicationTypeViewSet, basename='communication-type')
router.register(r'event-types', EventTypeViewSet, basename='event-type')
router.register(r'marketing-types', MarketingTypeViewSet, basename='marketing-type')
router.register(r'offer-types', OfferTypeViewSet, basename='offer-type')
router.register(r'promotion-types', PromotionTypeViewSet, basename='promotion-type')
router.register(r'ticket-types', TicketTypeViewSet, basename='ticket-type')

# Define the URL patterns
urlpatterns = [
    path('', include(router.urls)),
]
