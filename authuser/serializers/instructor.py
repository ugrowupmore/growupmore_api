# authuser/serializers/instructor.py

from rest_framework import serializers
from .base import BaseUserSerializer
from authuser.models.instructor import Instructor
from rest_framework_simplejwt.tokens import RefreshToken


class InstructorSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = Instructor
        fields = ('email', 'mobile', 'password')

    @staticmethod
    def generate_refresh_token(user):
        refresh = RefreshToken.for_user(user)
        refresh['user_type'] = 'instructor'
        return refresh


class InstructorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},              
            'create_date': {'read_only': True},
            'last_update_date': {'read_only': True},            
            'failed_login_attempts': {'read_only': True},
            'account_locked_until': {'read_only': True},
        }

    def update(self, instance, validated_data):
        # Prevent updating read-only fields
        validated_data.pop('password', None)
        return super().update(instance, validated_data)
