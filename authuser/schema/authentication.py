# authuser/schema/authentication.py

from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework import authentication

class UnifiedJWTAuthenticationExtension(OpenApiAuthenticationExtension):
    target_class = 'authuser.authentication.unified_jwt_authentication.UnifiedJWTAuthentication'
    name = 'UnifiedJWTAuthentication'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
            'description': 'Enter your JWT token in the format **Bearer <token>**.'
        }
