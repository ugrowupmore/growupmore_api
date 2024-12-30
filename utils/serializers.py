# utils/serializers.py

from rest_framework import serializers
from .models import OTP

class OTPCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = '__all__'
