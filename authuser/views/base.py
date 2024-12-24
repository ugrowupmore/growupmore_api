# authuser/views/base.py

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
import jwt
import logging
import requests
from datetime import datetime, timedelta

from utils.email_utils import send_custom_email
from authuser.authentication import UnifiedJWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from authuser.permissions import IsStudent, IsEmployee, IsInstructor, IsInstitute

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from rest_framework import serializers

logger = logging.getLogger(__name__)


class BaseRegisterView(generics.CreateAPIView):
    """
    Abstract base class for user registration.
    """
    user_model = None
    serializer_class = None  # To be defined in subclasses
    email_subject = 'Activate your account'
    email_template = '''
    <p>Dear {name},</p>
    <p>Thank you for registering. Please click the link below to activate your account:</p>
    <p><a href="{activation_link}">Activate Account</a></p>
    <p>If you did not register, please ignore this email.</p>
    '''
    activation_url_name = 'activate-account'  # Default, to be overridden

    permission_classes = [AllowAny]
    authentication_classes = []  # No authentication needed for registration

    def perform_create(self, serializer):
        user = serializer.save()
        logger.debug(f"User saved: {user.email}")

        user_type = self.get_user_type(user)
        token = jwt.encode(
            {'user_id': user.id, 'user_type': user_type, 'exp': datetime.utcnow() + timedelta(hours=24)},
            settings.SECRET_KEY, algorithm='HS256'
        )
        # activation_link = f"{settings.FRONTEND_BASE_URL}/activate/{token}/"
        activation_link = self.request.build_absolute_uri(reverse(self.activation_url_name, kwargs={'token': token}))
        html_content = self.email_template.format(name=user.first_name or 'User', activation_link=activation_link)
        subject = self.email_subject
        logger.debug(f"Preparing to send activation email to: {user.email}")
        
        try:
            send_custom_email(subject, html_content, [user.email])
            logger.info(f"Activation email sent to: {user.email}")
        except Exception as e:
            logger.error(f"Error sending activation email to {user.email}: {str(e)}", exc_info=True)

        logger.info(f"New user registered: {user.email}")

    def get_user_type(self, user):
        if hasattr(user, 'student_ptr'):
            return 'student'
        elif hasattr(user, 'employee_ptr'):
            return 'employee'
        elif hasattr(user, 'instructor_ptr'):
            return 'instructor'
        elif hasattr(user, 'institute_ptr'):
            return 'institute'
        return 'unknown'


class BaseActivateView(generics.GenericAPIView):
    """
    Abstract base class for account activation.
    """
    user_model = None

    permission_classes = [AllowAny]
    authentication_classes = []  # No authentication needed for activation

    def get(self, request, token=None):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            user = self.user_model.objects.get(id=user_id)
            if user.is_active:
                logger.info(f"Account already activated: {user.email}")
                return Response({'message': 'Account already activated.'}, status=status.HTTP_200_OK)
            user.is_active = True
            user.save()
            logger.info(f"Account activated successfully: {user.email}")
            return Response({'message': 'Account activated successfully.'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            logger.warning("Activation token expired.")
            return Response({'error': 'Activation token has expired.'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            logger.warning("Invalid activation token.")
            return Response({'error': 'Invalid activation token.'}, status=status.HTTP_400_BAD_REQUEST)
        except self.user_model.DoesNotExist:
            logger.warning("User does not exist during activation.")
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)


class BaseLoginView(APIView):
    """
    Abstract base class for handling user login.
    """
    user_model = None
    blacklisted_token_model = None
    serializer_class = None  # To be defined in subclasses

    authentication_classes = [UnifiedJWTAuthentication]  # Correctly set as a list
    permission_classes = [AllowAny]

    @method_decorator(ratelimit(key='ip', rate='10/h', method='POST', block=True))
    def post(self, request):
        if not settings.DISABLE_RECAPTCHA:
            recaptcha_token = request.data.get('recaptcha_token')
            if not recaptcha_token:
                logger.warning("Login attempt without recaptcha_token.")
                return Response({'error': 'recaptcha_token is required.'}, status=status.HTTP_400_BAD_REQUEST)
            
            recaptcha_response = self.verify_recaptcha(recaptcha_token)
            if not recaptcha_response.get('success', False) or recaptcha_response.get('score', 0) < 0.5:
                logger.warning("Failed reCAPTCHA verification during login.")
                return Response({'error': 'reCAPTCHA verification failed.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.info("reCAPTCHA is disabled. Skipping verification for login.")

        identifier = request.data.get('identifier')  # Can be email or mobile
        password = request.data.get('password')  # Plain-text password

        if not identifier or not password:
            logger.warning("Login attempt with missing credentials.")
            return Response({'error': 'Please provide identifier and password.'}, status=status.HTTP_400_BAD_REQUEST)

        user = None

        # Attempt to retrieve the user by email
        try:
            user = self.user_model.objects.get(email=identifier)
        except self.user_model.DoesNotExist:
            # If not found by email, attempt to retrieve by mobile
            try:
                user = self.user_model.objects.get(mobile=identifier)
            except self.user_model.DoesNotExist:
                pass

        if not user:
            logger.warning(f"Invalid login credentials for identifier: {identifier}")
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if the account is locked
        if user.account_locked_until and timezone.now() < user.account_locked_until:
            remaining_lock_time = user.account_locked_until - timezone.now()
            remaining_minutes = int(remaining_lock_time.total_seconds() // 60) + 1  # Round up to the next minute
            logger.warning(f"Account locked for user: {user.email}")
            return Response({'error': f'Account is locked. Try again in {remaining_minutes} minutes.'}, status=status.HTTP_403_FORBIDDEN)

        # Check password
        if not user.check_password(password):
            user.failed_login_attempts += 1
            remaining_attempts = 3 - user.failed_login_attempts

            if user.failed_login_attempts >= 3:
                user.account_locked_until = timezone.now() + timedelta(hours=24)  # Lock for 24 hours
                user.failed_login_attempts = 0  # Reset after locking
                user.save()
                logger.warning(f"Account locked due to failed attempts: {user.email}")
                return Response({'error': 'Account locked due to too many failed login attempts. Try again after 24 hours.'}, status=status.HTTP_403_FORBIDDEN)

            user.save()
            logger.warning(f"Invalid password attempt for user: {user.email}")
            return Response({'error': f'Invalid credentials. {remaining_attempts} attempts left before account lock.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Reset failed attempts and lockout
        user.failed_login_attempts = 0
        user.account_locked_until = None
        user.save()

        # Check if the account is active
        if not user.is_active:
            logger.warning(f"Inactive account login attempt: {user.email}")
            return Response({'error': 'Account is not active.'}, status=status.HTTP_403_FORBIDDEN)

        # Generate JWT token with expiration time (7 days)
        refresh = self.serializer_class.generate_refresh_token(user)
        access_token = str(refresh.access_token)

        # Optionally, include a message about KYC status
        response_data = {
            'access': access_token,
            'refresh': str(refresh),  # Include refresh token
        }

        if not user.is_kyc_approved:
            response_data['message'] = 'KYC not approved. Please complete your profile.'

        logger.info(f"User logged in successfully: {user.email}")
        return Response(response_data, status=status.HTTP_200_OK)

    def verify_recaptcha(self, token):
        url = 'https://www.google.com/recaptcha/api/siteverify'
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': token
        }
        try:
            response = requests.post(url, data=data)
            return response.json()
        except Exception as e:
            logger.error(f"Error verifying reCAPTCHA: {str(e)}")
            return {'success': False, 'score': 0}


class BaseLogoutView(APIView):
    """
    Abstract base class for user logout.
    """
    user_model = None
    blacklisted_token_model = None
    authentication_classes = [UnifiedJWTAuthentication]  # Correctly set as a list

    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = None
        auth_header = request.headers.get('Authorization', '').split()

        if len(auth_header) == 2 and auth_header[0].lower() == 'bearer':
            token = auth_header[1]

        if not token:
            logger.warning("Logout attempt without authentication token.")
            return Response({'error': 'Authentication token not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Decode the token to extract the jti
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            jti = payload.get('jti')
            if not jti:
                logger.warning("Logout attempt with token missing jti.")
                return Response({'error': 'Invalid token: Missing jti.'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            logger.warning("Logout attempt with invalid token.")
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the jti is already blacklisted
        if self.blacklisted_token_model.objects.filter(jti=jti).exists():
            logger.warning("Attempt to blacklist an already blacklisted token.")
            return Response({'error': 'Token already blacklisted.'}, status=status.HTTP_400_BAD_REQUEST)

        # Blacklist the jti
        self.blacklisted_token_model.objects.create(jti=jti)
        logger.info(f"Token blacklisted for user: {request.user.email}")

        return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)


class BaseChangePasswordView(APIView):  
    """
    Abstract base class for changing user password.
    """
    authentication_classes = [UnifiedJWTAuthentication]  # Correctly set as a list
    permission_classes = [IsAuthenticated]
    serializer_class = None  # To be defined in subclasses

    def post(self, request):
        user = request.user  # Get the authenticated user (GenericUserWrapper instance)
        old_password = request.data.get('old_password')  # Current password
        new_password = request.data.get('new_password')  # Desired new password

        if not old_password or not new_password:
            logger.warning(f"Password change attempt with missing fields by user: {user.email}")
            return Response({'error': 'Please provide old and new passwords.'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(old_password):
            logger.warning(f"Incorrect old password for user: {user.email}")
            return Response({'error': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        logger.info(f"Password changed successfully for user: {user.email}")
        return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)


class BaseForgotPasswordView(generics.GenericAPIView):
    """
    Abstract base class to initiate password reset.
    """
    user_model = None
    email_subject = 'Reset your password'
    email_template = '''
    <p>Dear {name},</p>
    <p>Please click the link below to reset your password:</p>
    <p><a href="{reset_link}">Reset Password</a></p>
    <p>If you did not request a password reset, please ignore this email.</p>
    '''

    password_reset_url_name = 'password-reset'  # To be overridden in subclasses

    permission_classes = [AllowAny]
    authentication_classes = []  # No authentication needed for forgot password
    serializer_class = None  # To be defined in subclasses

    def post(self, request):
        if not settings.DISABLE_RECAPTCHA:
            recaptcha_token = request.data.get('recaptcha_token')
            if not recaptcha_token:
                logger.warning("Forgot password attempt without recaptcha_token.")
                return Response({'error': 'recaptcha_token is required.'}, status=status.HTTP_400_BAD_REQUEST)
            
            recaptcha_response = self.verify_recaptcha(recaptcha_token)
            if not recaptcha_response.get('success', False) or recaptcha_response.get('score', 0) < 0.5:
                logger.warning("Failed reCAPTCHA verification during forgot password.")
                return Response({'error': 'reCAPTCHA verification failed.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.info("reCAPTCHA is disabled. Skipping verification for forgot password.")

        email = request.data.get('email')

        if not email:
            logger.warning("Forgot password attempt without email.")
            return Response({'error': 'Please provide email.'}, status=status.HTTP_400_BAD_REQUEST)

        user = None

        try:
            user = self.user_model.objects.get(email=email)
        except self.user_model.DoesNotExist:
            pass

        if not user:
            logger.warning(f"Forgot password attempt with non-existent email: {email}")
            return Response({'error': 'Email not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Generate password reset token with expiration time (1 hour)
        token = jwt.encode(
            {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=1)},
            settings.SECRET_KEY, algorithm='HS256'
        )

        # reset_link = f"{settings.FRONTEND_BASE_URL}/reset-password/{token}/"
        reset_link = self.request.build_absolute_uri(reverse(self.password_reset_url_name, kwargs={'token': token}))
        html_content = self.email_template.format(name=user.first_name or 'User', reset_link=reset_link)
        subject = self.email_subject
        send_custom_email(subject, html_content, [user.email])
        logger.info(f"Password reset link sent to user: {user.email}")

        return Response({'message': 'Password reset link sent to your email.'}, status=status.HTTP_200_OK)

    def verify_recaptcha(self, token):
        url = 'https://www.google.com/recaptcha/api/siteverify'
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': token
        }
        try:
            response = requests.post(url, data=data)
            return response.json()
        except Exception as e:
            logger.error(f"Error verifying reCAPTCHA: {str(e)}")
            return {'success': False, 'score': 0}


class BasePasswordResetView(APIView):
    """
    Abstract base class to handle password resetting.
    """
    user_model = None

    permission_classes = [AllowAny]
    authentication_classes = []  # No authentication needed for password reset
    serializer_class = None  # To be defined in subclasses

    def post(self, request, token=None):
        new_password = request.data.get('new_password')

        if not new_password:
            logger.warning("Password reset attempt without new password.")
            return Response({'error': 'Please provide new password.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            user = self.user_model.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()
            logger.info(f"Password reset successful for user: {user.email}")
            return Response({'message': 'Password reset successful.'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            logger.warning("Password reset token expired.")
            return Response({'error': 'Token expired.'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            logger.warning("Invalid password reset token.")
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        except self.user_model.DoesNotExist:
            logger.warning("Password reset attempt for non-existent user.")
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error during password reset: {str(e)}")
            return Response({'error': 'Something went wrong.'}, status=status.HTTP_400_BAD_REQUEST)


class BaseProfileView(generics.RetrieveUpdateAPIView):
    """
    Abstract base class for user profile view and update.
    """
    serializer_class = None  # To be defined in subclasses
    permission_classes = [IsAuthenticated]
    authentication_classes = [UnifiedJWTAuthentication]

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()

    def get_object(self):
        return self.request.user.user  # Assuming GenericUserWrapper has a 'user' attribute

    def perform_update(self, serializer):
        serializer.save()
        user = self.request.user.user
        user.is_kyc_approved = True  # Assuming KYC approval is part of profile update
        user.save()
        logger.info(f"Profile updated for user: {user.email}")


# Define TestCaptchaSerializer inside base.py or import it
class TestCaptchaSerializer(serializers.Serializer):
    recaptcha_token = serializers.CharField()


@extend_schema(
    summary="Test Captcha",
    description="Endpoint to test captcha functionality.",
    request=TestCaptchaSerializer,
    responses={
        200: OpenApiResponse(
            description="Captcha validated successfully.",
            examples=[
                OpenApiExample(
                    name="Captcha Success Response",
                    value={
                        "message": "Captcha validated successfully.",
                        "score": 0.9
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description="Invalid captcha.",
            examples=[
                OpenApiExample(
                    name="Captcha Failure Response",
                    value={
                        "error": "Invalid captcha token.",
                        "score": 0.3
                    }
                )
            ]
        )
    },
    tags=["Authentication"]
)
class TestCaptchaView(generics.GenericAPIView):
    """
    View to test Google reCAPTCHA v3.
    """
    serializer_class = TestCaptchaSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            recaptcha_token = serializer.validated_data.get('recaptcha_token')
            recaptcha_response = self.verify_recaptcha(recaptcha_token)
            if recaptcha_response.get('success', False) and recaptcha_response.get('score', 0) >= 0.5:
                return Response({'message': 'reCAPTCHA verification successful.', 'score': recaptcha_response.get('score', 0)}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'reCAPTCHA verification failed.', 'score': recaptcha_response.get('score', 0)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def verify_recaptcha(self, token):
        url = 'https://www.google.com/recaptcha/api/siteverify'
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': token
        }
        try:
            response = requests.post(url, data=data)
            return response.json()
        except Exception as e:
            logger.error(f"Error verifying reCAPTCHA: {str(e)}")
            return {'success': False, 'score': 0}
