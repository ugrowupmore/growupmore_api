# authuser/views/instructor.py

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
    OpenApiParameter
)
from drf_spectacular.types import OpenApiTypes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from authuser.models import Instructor, InstructorBlacklistedToken
from authuser.serializers.instructor import (
    InstructorSerializer, InstructorProfileSerializer
)
from authuser.serializers.auth_requests import (
    ChangePasswordSerializer, ForgotPasswordSerializer, PasswordResetSerializer
)
from authuser.serializers.auth_responses import LogoutResponseSerializer
from authuser.permissions import IsInstructor
from authuser.views.base import (
    BaseRegisterView, BaseActivateView, BaseLoginView, BaseLogoutView,
    BaseChangePasswordView, BaseForgotPasswordView, BasePasswordResetView,
    BaseProfileView
)

@extend_schema(
    summary="Register a new Instructor",
    description="Register a new instructor by providing email, mobile, and password.",
    request=InstructorSerializer,
    responses={
        201: OpenApiResponse(
            response=InstructorSerializer,
            description="Registration successful."
        ),
        400: OpenApiResponse(description="Bad Request")
    },
    tags=["Instructor"],
    examples=[
        OpenApiExample(
            name="Instructor Registration Request",
            summary="Request body for registering a new instructor",
            description="Provide email, mobile number, password, and reCAPTCHA token.",
            value={
                "email": "jane.doe@example.com",
                "mobile": "+10987654321",
                "password": "InstructorPass123!",
                "recaptcha_token": "dummy-recaptcha-token"
            }
        ),
        OpenApiExample(
            name="Instructor Registration Success Response",
            summary="Successful registration response",
            description="Confirmation message after successful registration.",
            value={
                "message": "Registration successful. Please check your email to activate your account."
            }
        ),
        OpenApiExample(
            name="Instructor Registration Failure Response",
            summary="Failed registration response",
            description="Error message when registration fails due to validation errors.",
            value={
                "email": ["This field must be unique."],
                "password": ["This password is too common."]
            }
        )
    ]
)
class InstructorRegisterView(BaseRegisterView):
    user_model = Instructor
    serializer_class = InstructorSerializer
    permission_classes = [AllowAny]
    activation_url_name = 'instructor-activate'


@extend_schema(
    summary="Activate Instructor Account",
    description="Activate an instructor account using the activation token sent via email.",
    parameters=[
        OpenApiParameter(
            name='token',
            description='Activation token received in email.',
            required=True,
            type=OpenApiTypes.STR,
            location='path'
        )
    ],
    responses={
        200: OpenApiResponse(description="Account activated successfully."),
        400: OpenApiResponse(description="Invalid or expired token."),
        404: OpenApiResponse(description="User does not exist.")
    },
    tags=["Instructor"],
    examples=[
        OpenApiExample(
            name="Account Activation Success Response",
            summary="Successful account activation",
            description="Confirmation message after successful activation.",
            value={
                "message": "Account activated successfully."
            }
        ),
        OpenApiExample(
            name="Account Activation Failure Response",
            summary="Failed account activation",
            description="Error message when activation token is invalid or expired.",
            value={
                "error": "Invalid activation token."
            }
        )
    ]
)
class InstructorActivateView(BaseActivateView):
    user_model = Instructor
    permission_classes = [AllowAny]


@extend_schema(
    summary="Instructor Login",
    description="Authenticate an instructor using email or mobile and password.",
    request=InstructorSerializer,
    responses={
        200: OpenApiResponse(
            description=(
                "Login successful. Returns access and refresh JWT tokens. "
                "If KYC is not approved, an additional message is included."
            )
        ),
        400: OpenApiResponse(description="Bad Request"),
        401: OpenApiResponse(description="Invalid credentials."),
        403: OpenApiResponse(description="Account locked or inactive.")
    },
    tags=["Instructor"],
    examples=[
        OpenApiExample(
            name="Instructor Login Request",
            summary="Request body for instructor login",
            description="Provide identifier (email or mobile), password, and reCAPTCHA token.",
            value={
                "identifier": "jane.doe@example.com",
                "password": "InstructorPass123!",
                "recaptcha_token": "dummy-recaptcha-token"
            }
        ),
        OpenApiExample(
            name="Instructor Login Success Response",
            summary="Successful login response",
            description="Returns access and refresh tokens, and a message if KYC is not approved.",
            value={
                "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "message": "KYC not approved. Please complete your profile."
            }
        ),
        OpenApiExample(
            name="Instructor Login Failure Response",
            summary="Failed login response",
            description="Error message when credentials are invalid.",
            value={
                "error": "Invalid credentials. 2 attempts left before account lock."
            }
        )
    ]
)
class InstructorLoginView(BaseLoginView):
    user_model = Instructor
    blacklisted_token_model = InstructorBlacklistedToken
    serializer_class = InstructorSerializer
    permission_classes = [AllowAny]


@extend_schema(
    summary="Instructor Logout",
    description="Logout an authenticated instructor by blacklisting the current JWT token.",
    responses={
        200: OpenApiResponse(
            response=LogoutResponseSerializer,
            description="Successfully logged out."
        ),
        400: OpenApiResponse(description="Bad Request"),
        401: OpenApiResponse(description="Authentication credentials were not provided."),
    },
    tags=["Instructor"],
    examples=[
        OpenApiExample(
            name="Instructor Logout Success Response",
            summary="Successful logout response",
            description="Confirmation message after successful logout.",
            value={
                "message": "Successfully logged out."
            }
        ),
        OpenApiExample(
            name="Instructor Logout Failure Response",
            summary="Failed logout response",
            description="Error message when token is not provided or invalid.",
            value={
                "error": "Authentication token not provided."
            }
        )
    ]
)
class InstructorLogoutView(BaseLogoutView):
    user_model = Instructor
    blacklisted_token_model = InstructorBlacklistedToken
    permission_classes = [IsAuthenticated, IsInstructor]
    serializer_class = LogoutResponseSerializer  # Added serializer_class


@extend_schema(
    summary="Change Instructor Password",
    description="Allow an authenticated instructor to change their password.",
    request=ChangePasswordSerializer,
    responses={
        200: OpenApiResponse(description="Password changed successfully."),
        400: OpenApiResponse(description="Bad Request"),
        401: OpenApiResponse(description="Incorrect old password.")
    },
    tags=["Instructor"],
    examples=[
        OpenApiExample(
            name="Change Password Request",
            summary="Request body for changing password",
            description="Provide the current password and the new desired password.",
            value={
                "old_password": "OldInstructorPass123!",
                "new_password": "NewInstructorPass456!"
            }
        ),
        OpenApiExample(
            name="Change Password Success Response",
            summary="Successful password change response",
            description="Confirmation message after successfully changing the password.",
            value={
                "message": "Password changed successfully."
            }
        ),
        OpenApiExample(
            name="Change Password Failure Response",
            summary="Failed password change response",
            description="Error message when the old password is incorrect.",
            value={
                "error": "Old password is incorrect."
            }
        )
    ]
)
class InstructorChangePasswordView(BaseChangePasswordView):
    permission_classes = [IsAuthenticated, IsInstructor]
    serializer_class = ChangePasswordSerializer  # Added serializer_class


@extend_schema(
    summary="Initiate Instructor Password Reset",
    description="Send a password reset link to the instructor's email.",
    request=ForgotPasswordSerializer,
    responses={
        200: OpenApiResponse(description="Password reset link sent."),
        400: OpenApiResponse(description="Bad Request"),
        404: OpenApiResponse(description="Email not found.")
    },
    tags=["Instructor"],
    examples=[
        OpenApiExample(
            name="Forgot Password Request",
            summary="Request body for initiating password reset",
            description="Provide the registered email and reCAPTCHA token.",
            value={
                "email": "jane.doe@example.com",
                "recaptcha_token": "dummy-recaptcha-token"
            }
        ),
        OpenApiExample(
            name="Forgot Password Success Response",
            summary="Successful password reset initiation",
            description="Confirmation message after sending the reset link.",
            value={
                "message": "Password reset link sent to your email."
            }
        ),
        OpenApiExample(
            name="Forgot Password Failure Response",
            summary="Failed password reset initiation",
            description="Error message when the email is not found.",
            value={
                "error": "Email not found."
            }
        )
    ]
)
class InstructorForgotPasswordView(BaseForgotPasswordView):
    user_model = Instructor
    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordSerializer  # Added serializer_class


@extend_schema(
    summary="Reset Instructor Password",
    description="Reset the instructor's password using the reset token.",
    parameters=[
        OpenApiParameter(
            name='token',
            description='Password reset token received in email.',
            required=True,
            type=OpenApiTypes.STR,
            location='path'
        )
    ],
    request=PasswordResetSerializer,
    responses={
        200: OpenApiResponse(description="Password reset successful."),
        400: OpenApiResponse(description="Invalid or expired token."),
        404: OpenApiResponse(description="User does not exist.")
    },
    tags=["Instructor"],
    examples=[
        OpenApiExample(
            name="Password Reset Request",
            summary="Request body for resetting password",
            description="Provide the new desired password.",
            value={
                "new_password": "NewInstructorPass456!"
            }
        ),
        OpenApiExample(
            name="Password Reset Success Response",
            summary="Successful password reset response",
            description="Confirmation message after successfully resetting the password.",
            value={
                "message": "Password reset successful."
            }
        ),
        OpenApiExample(
            name="Password Reset Failure Response",
            summary="Failed password reset response",
            description="Error message when the token is invalid or expired.",
            value={
                "error": "Invalid or expired token."
            }
        )
    ]
)
class InstructorPasswordResetView(BasePasswordResetView):
    user_model = Instructor
    permission_classes = [AllowAny]
    password_reset_url_name = 'instructor-password-reset'
    serializer_class = PasswordResetSerializer  # Added serializer_class


@extend_schema(
    summary="Retrieve or Update Instructor Profile",
    description="Get the authenticated instructor's profile or update it.",
    request=InstructorProfileSerializer,
    responses={
        200: OpenApiResponse(
            response=InstructorProfileSerializer,
            description="Profile retrieved or updated successfully."
        ),
        400: OpenApiResponse(description="Bad Request"),
        401: OpenApiResponse(description="Authentication credentials were not provided."),
    },
    tags=["Instructor"],
    examples=[
        OpenApiExample(
            name="Profile Retrieval Success Response",
            summary="Successful profile retrieval",
            description="Returns the instructor's current profile data.",
            value={
                "id": 1,
                "first_name": "Jane",
                "last_name": "Doe",
                "birthdate": "1985-03-10",
                "email": "jane.doe@example.com",
                "mobile": "+10987654321",
                "is_admin": False,
                "is_active": True,
                "is_kyc_approved": False,
                "is_mobile_approved": True,
                "create_date": "2024-02-01T12:00:00Z",
                "last_update_date": "2024-06-01T12:00:00Z",
                "updated_by": None,
                "status": "DRAFT",
                "failed_login_attempts": 0,
                "account_locked_until": None
            }
        ),
        OpenApiExample(
            name="Profile Update Request",
            summary="Request body for updating profile",
            description="Provide fields to be updated. Password cannot be updated here.",
            value={
                "first_name": "Janet",
                "last_name": "Doe-Smith",
                "birthdate": "1985-04-15"
            }
        ),
        OpenApiExample(
            name="Profile Update Success Response",
            summary="Successful profile update response",
            description="Returns the updated profile data.",
            value={
                "id": 1,
                "first_name": "Janet",
                "last_name": "Doe-Smith",
                "birthdate": "1985-04-15",
                "email": "jane.doe@example.com",
                "mobile": "+10987654321",
                "is_admin": False,
                "is_active": True,
                "is_kyc_approved": True,
                "is_mobile_approved": True,
                "create_date": "2024-02-01T12:00:00Z",
                "last_update_date": "2024-06-02T14:30:00Z",
                "updated_by": 1,
                "status": "DRAFT",
                "failed_login_attempts": 0,
                "account_locked_until": None
            }
        ),
        OpenApiExample(
            name="Profile Update Failure Response",
            summary="Failed profile update response",
            description="Error message when validation fails or forbidden fields are attempted to be updated.",
            value={
                "email": ["This field cannot be updated."]
            }
        )
    ]
)
class InstructorProfileView(BaseProfileView):
    serializer_class = InstructorProfileSerializer
    permission_classes = [IsAuthenticated, IsInstructor]
