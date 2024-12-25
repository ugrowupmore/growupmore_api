# authuser/views/student.py

from .base import (
    BaseRegisterView, BaseActivateView, BaseLoginView, BaseLogoutView,
    BaseChangePasswordView, BaseForgotPasswordView, BasePasswordResetView,
    BaseProfileView
)
from authuser.models import Student, StudentBlacklistedToken
from authuser.serializers import StudentSerializer, StudentProfileSerializer
from authuser.permissions import IsStudent
from authuser.authentication.unified_jwt_authentication import UnifiedJWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

class StudentRegisterView(BaseRegisterView):
    user_model = Student
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]
    activation_url_name = 'student-activate'

class StudentActivateView(BaseActivateView):
    user_model = Student
    permission_classes = [AllowAny]
    authentication_classes = []  # No authentication needed for activation

class StudentLoginView(BaseLoginView):
    user_model = Student
    blacklisted_token_model = StudentBlacklistedToken
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]

class StudentLogoutView(BaseLogoutView):
    user_model = Student
    blacklisted_token_model = StudentBlacklistedToken
    permission_classes = [IsAuthenticated, IsStudent]
    authentication_classes = [UnifiedJWTAuthentication]

class StudentChangePasswordView(BaseChangePasswordView):
    permission_classes = [IsAuthenticated, IsStudent]

class StudentForgotPasswordView(BaseForgotPasswordView):
    user_model = Student
    permission_classes = [AllowAny]
    password_reset_url_name = 'student-password-reset'

class StudentPasswordResetView(BasePasswordResetView):
    user_model = Student
    permission_classes = [AllowAny]

class StudentProfileView(BaseProfileView):
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated, IsStudent]
