# authuser/serializers/superuser.py

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class SuperUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), username=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid credentials.')

        if not user.is_superuser:
            raise serializers.ValidationError('You do not have superuser privileges.')

        if not user.is_active:
            raise serializers.ValidationError('User account is inactive.')

        refresh = RefreshToken.for_user(user)
        refresh['user_type'] = 'superuser'

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
