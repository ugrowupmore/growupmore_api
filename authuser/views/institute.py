# authuser/views/institute.py

from .base import (
    BaseRegisterView, BaseActivateView, BaseLoginView, BaseLogoutView,
    BaseChangePasswordView, BaseForgotPasswordView, BasePasswordResetView,
    BaseProfileView
)
from authuser.models import Institute, InstituteBlacklistedToken
from authuser.serializers import InstituteSerializer, InstituteProfileSerializer
from authuser.permissions import IsInstitute
from authuser.authentication.unified_jwt_authentication import UnifiedJWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated


class InstituteRegisterView(BaseRegisterView):
    user_model = Institute
    serializer_class = InstituteSerializer
    permission_classes = [AllowAny]
    activation_url_name = 'institute-activate'

class InstituteActivateView(BaseActivateView):
    user_model = Institute
    permission_classes = [AllowAny]
    authentication_classes = []  # No authentication needed for activation

class InstituteLoginView(BaseLoginView):
    user_model = Institute
    blacklisted_token_model = InstituteBlacklistedToken
    serializer_class = InstituteSerializer
    permission_classes = [AllowAny]


class InstituteLogoutView(BaseLogoutView):
    user_model = Institute
    blacklisted_token_model = InstituteBlacklistedToken
    permission_classes = [IsAuthenticated, IsInstitute]
    authentication_classes = [UnifiedJWTAuthentication]


class InstituteChangePasswordView(BaseChangePasswordView):
    permission_classes = [IsAuthenticated, IsInstitute]


class InstituteForgotPasswordView(BaseForgotPasswordView):
    user_model = Institute
    permission_classes = [AllowAny]
    password_reset_url_name = 'institute-password-reset'


class InstitutePasswordResetView(BasePasswordResetView):
    user_model = Institute
    permission_classes = [AllowAny]


class InstituteProfileView(BaseProfileView):
    serializer_class = InstituteProfileSerializer
    permission_classes = [IsAuthenticated, IsInstitute]
