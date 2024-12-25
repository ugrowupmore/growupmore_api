# authuser/views/employee.py

from .base import (
    BaseRegisterView, BaseActivateView, BaseLoginView, BaseLogoutView,
    BaseChangePasswordView, BaseForgotPasswordView, BasePasswordResetView,
    BaseProfileView
)
from authuser.models import Employee, EmployeeBlacklistedToken
from authuser.serializers import EmployeeSerializer, EmployeeProfileSerializer
from authuser.permissions import IsEmployee
from rest_framework.permissions import AllowAny, IsAuthenticated


class EmployeeRegisterView(BaseRegisterView):
    user_model = Employee
    serializer_class = EmployeeSerializer
    permission_classes = [AllowAny]
    activation_url_name = 'employee-activate'


class EmployeeActivateView(BaseActivateView):
    user_model = Employee
    permission_classes = [AllowAny]


class EmployeeLoginView(BaseLoginView):
    user_model = Employee
    blacklisted_token_model = EmployeeBlacklistedToken
    serializer_class = EmployeeSerializer
    permission_classes = [AllowAny]


class EmployeeLogoutView(BaseLogoutView):
    user_model = Employee
    blacklisted_token_model = EmployeeBlacklistedToken
    permission_classes = [IsAuthenticated, IsEmployee]


class EmployeeChangePasswordView(BaseChangePasswordView):
    permission_classes = [IsAuthenticated, IsEmployee]


class EmployeeForgotPasswordView(BaseForgotPasswordView):
    user_model = Employee
    permission_classes = [AllowAny]


class EmployeePasswordResetView(BasePasswordResetView):
    user_model = Employee
    permission_classes = [AllowAny]
    password_reset_url_name = 'employee-password-reset'


class EmployeeProfileView(BaseProfileView):
    serializer_class = EmployeeProfileSerializer
    permission_classes = [IsAuthenticated, IsEmployee]
