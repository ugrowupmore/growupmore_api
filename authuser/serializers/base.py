# authuser/serializers/base.py

from rest_framework import serializers
from django.contrib.auth.hashers import make_password

class BaseUserSerializer(serializers.ModelSerializer):
    """
    A generic serializer for user registration.
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        # To be defined in subclasses
        model = None
        fields = ('email', 'mobile', 'password')

    def create(self, validated_data):
        user = self.Meta.model(
            email=validated_data['email'],
            mobile=validated_data['mobile'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
