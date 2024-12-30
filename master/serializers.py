# master/serializers.py

from rest_framework import serializers
from .models import Country, State, City

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), source='country', write_only=True
    )

    class Meta:
        model = State
        fields = ['id', 'name', 'country', 'country_id']

class CitySerializer(serializers.ModelSerializer):
    state = StateSerializer(read_only=True)
    state_id = serializers.PrimaryKeyRelatedField(
        queryset=State.objects.all(), source='state', write_only=True
    )

    class Meta:
        model = City
        fields = ['id', 'name', 'state', 'state_id']
