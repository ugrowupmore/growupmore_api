# authuser/serializers/auth_responses.py

from rest_framework import serializers

class LogoutResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
