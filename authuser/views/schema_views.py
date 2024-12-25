# authuser/views/schema_views.py

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from authuser.permissions import IsSuperUser
from rest_framework.authentication import SessionAuthentication  # Import SessionAuthentication

class ProtectedSpectacularAPIView(SpectacularAPIView):  
    """
    Spectacular API schema view protected for superusers.
    """
    permission_classes = [IsSuperUser]
    authentication_classes = [SessionAuthentication]  # Use SessionAuthentication

class ProtectedSpectacularSwaggerView(SpectacularSwaggerView):   
    """
    Spectacular Swagger UI view protected for superusers.
    """
    permission_classes = [IsSuperUser]
    authentication_classes = [SessionAuthentication]  # Use SessionAuthentication

class ProtectedSpectacularRedocView(SpectacularRedocView):   
    """
    Spectacular Redoc UI view protected for superusers.
    """
    permission_classes = [IsSuperUser]
    authentication_classes = [SessionAuthentication]  # Use SessionAuthentication
