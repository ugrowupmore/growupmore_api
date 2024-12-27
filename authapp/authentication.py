# authapp/authentication.py

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions

class JWTAuthenticationCookie(JWTAuthentication):
    """
    Custom JWT Authentication class that retrieves the token from HTTP-only cookies.
    """
    def authenticate(self, request):
        # Try to get the token from the Authorization header
        auth = super().authenticate(request)
        if auth:
            return auth

        # If not found in header, try to get it from the cookies
        token = request.COOKIES.get('access_token')

        if token is None:
            return None

        validated_token = self.get_validated_token(token)
        return self.get_user(validated_token), validated_token
