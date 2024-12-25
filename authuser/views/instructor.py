# authuser/views/instructor.py

from .base import (
    BaseRegisterView, BaseActivateView, BaseLoginView, BaseLogoutView,
    BaseChangePasswordView, BaseForgotPasswordView, BasePasswordResetView,
    BaseProfileView
)
from authuser.models import Instructor, InstructorBlacklistedToken
from authuser.serializers import InstructorSerializer, InstructorProfileSerializer
from authuser.permissions import IsInstructor
from authuser.authentication.unified_jwt_authentication import UnifiedJWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated


class InstructorRegisterView(BaseRegisterView):
    user_model = Instructor
    serializer_class = InstructorSerializer
    permission_classes = [AllowAny]
    activation_url_name = 'instructor-activate'

class InstructorActivateView(BaseActivateView):
    user_model = Instructor
    permission_classes = [AllowAny]
    authentication_classes = []  # No authentication needed for activation

class InstructorLoginView(BaseLoginView):
    user_model = Instructor
    blacklisted_token_model = InstructorBlacklistedToken
    serializer_class = InstructorSerializer
    permission_classes = [AllowAny]


class InstructorLogoutView(BaseLogoutView):
    user_model = Instructor
    blacklisted_token_model = InstructorBlacklistedToken
    permission_classes = [IsAuthenticated, IsInstructor]
    authentication_classes = [UnifiedJWTAuthentication]

class InstructorChangePasswordView(BaseChangePasswordView):
    permission_classes = [IsAuthenticated, IsInstructor]


class InstructorForgotPasswordView(BaseForgotPasswordView):
    user_model = Instructor
    permission_classes = [AllowAny]
    password_reset_url_name = 'instructor-password-reset'


class InstructorPasswordResetView(BasePasswordResetView):
    user_model = Instructor
    permission_classes = [AllowAny]


class InstructorProfileView(BaseProfileView):
    serializer_class = InstructorProfileSerializer
    permission_classes = [IsAuthenticated, IsInstructor]
