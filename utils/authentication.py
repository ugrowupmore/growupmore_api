# utils/authentication.py

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class GlobalTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Retrieve the token from the Authorization header
        token = request.headers.get("Authorization")
        
        if not token:
            raise AuthenticationFailed("Authorization header missing.")
        
        # Check if the token matches the global API key
        if token != f"Token {settings.GLOBAL_API_KEY}":
            raise AuthenticationFailed("Invalid or missing API key.")
        
        # Authentication successful; return None for anonymous/global access
        return (None, None)
