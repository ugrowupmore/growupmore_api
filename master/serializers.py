# master/serializers.py

from rest_framework import serializers
from master.models.bank import Bank
from master.models.branch_type import BranchType
from master.models.campaign_type import CampaignType
from master.models.city import City
from master.models.communication_type import CommunicationType
from master.models.content import Content
from master.models.country import Country
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

class CountrySerializer(serializers.ModelSerializer):
    flag_image = serializers.ImageField(max_length=200, default="na.png", required=False)    

    class Meta:
        model = Country
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')       


class StateSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name', read_only=True)   

    class Meta:
        model = State
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')       


class CitySerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name', read_only=True)    
    state_name = serializers.CharField(source='state.name', read_only=True)

    class Meta:
        model = City
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')       


class BankSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name', read_only=True)   

    class Meta:
        model = Bank
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')       


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')       


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')       


class SocialStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialStatus
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')       


class DocumentTypeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=200, default="na.png", required=False)    

    class Meta:
        model = DocumentType
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')       


class DocumentSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=200, default="na.png", required=False)    
    document_type_name = serializers.CharField(source='document_type.type', read_only=True)    

    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')       


class BranchTypeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=200, default="na.png", required=False)    

    class Meta:
        model = BranchType
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')       


class PackageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=200, default="na.png", required=False)    
    
    class Meta:
        model = Package
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')       


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')       


class PackageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageContent
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')          


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')       


class FAQCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQCategory
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')       


class BaseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')       


class CampaignTypeSerializer(BaseTypeSerializer):
    class Meta(BaseTypeSerializer.Meta):
        model = CampaignType
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')       


class CommunicationTypeSerializer(BaseTypeSerializer):
    class Meta(BaseTypeSerializer.Meta):
        model = CommunicationType
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')       


class EventTypeSerializer(BaseTypeSerializer):
    class Meta(BaseTypeSerializer.Meta):
        model = EventType
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')       


class MarketingTypeSerializer(BaseTypeSerializer):
    class Meta(BaseTypeSerializer.Meta):
        model = MarketingType
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')       


class OfferTypeSerializer(BaseTypeSerializer):
    class Meta(BaseTypeSerializer.Meta):
        model = OfferType
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')       


class PromotionTypeSerializer(BaseTypeSerializer):
    class Meta(BaseTypeSerializer.Meta):
        model = PromotionType
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')       


class TicketTypeSerializer(BaseTypeSerializer):
    class Meta(BaseTypeSerializer.Meta):
        model = TicketType
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')       