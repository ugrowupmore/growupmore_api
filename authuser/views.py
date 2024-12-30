# authuser/views.py

import logging  # Add this import
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import (
    UserRegistrationSerializer,
    ResendEmailOTPSerializer,
    ResendMobileOTPSerializer,
    UserVerificationSerializer,
    UserProfileSerializer,
    UserLoginSerializer,
    UserProfileSerializer,  
    UpdateEmailSerializer, 
    UpdateEmailVerifySerializer,
    UpdateMobileSerializer,
    UpdateMobileVerifySerializer,
    ChangePasswordSerializer,    
    ForgotPasswordSerializer,   
    ResetNewPasswordSerializer 
)
from .models import User
from utils.models import OTP
from utils.email_utils import send_custom_email
from utils.sms_otp_utils import send_otp_sms
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
import random

from master.models import Country

logger = logging.getLogger(__name__)  # Define the logger

# Utility function to generate OTP
def generate_otp():
    """Generates a 6-digit random OTP."""
    return str(random.randint(100000, 999999))

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Register a new user and send OTP.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"detail": "OTP sent to email and mobile."}, status=status.HTTP_201_CREATED)

class ResendEmailOTPView(generics.GenericAPIView):
    serializer_class = ResendEmailOTPSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')

        user = User.objects.get(email=email)

        # Check if resend OTP is locked
        if user.otp_resend_locked_until and timezone.now() < user.otp_resend_locked_until:
            lock_time_remaining = (user.otp_resend_locked_until - timezone.now()).seconds // 60  # in minutes
            return Response(
                {"detail": f"Resend OTP limit reached. Try again in {lock_time_remaining} minutes."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        # Check if resend attempts exceeded
        if user.resend_otp_attempts >= settings.MAX_RESEND_OTP_ATTEMPTS:
            user.otp_resend_locked_until = timezone.now() + timezone.timedelta(minutes=settings.RESEND_OTP_LOCK_DURATION_MINUTES)
            user.save()
            return Response(
                {"detail": "Resend OTP limit reached. Try again later."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        # Resend Email OTP
        self.resend_email_otp(user)
        return Response({"detail": "Email OTP resent."}, status=status.HTTP_200_OK)

    def resend_email_otp(self, user):
        """
        Generates and sends a new email OTP without affecting mobile OTP.
        """
        # Fetch the latest OTP
        try:
            otp = OTP.objects.filter(user=user).latest('created_at')
        except OTP.DoesNotExist:
            # Create a new OTP entry with both OTPs
            otp_email = generate_otp()
            otp_mobile = generate_otp()
            expiry_time = timezone.now() + timezone.timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
            otp = OTP.objects.create(
                user=user,
                email_otp=otp_email,
                mobile_otp=otp_mobile,
                expiry_time=expiry_time,
                is_verified=False,
                attempts=0
            )
        else:
            # Update only email_otp
            otp.email_otp = generate_otp()
            otp.expiry_time = timezone.now() + timezone.timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
            otp.is_verified = False
            otp.attempts = 0
            otp.save()

        # Increment resend attempts
        user.resend_otp_attempts += 1

        # If resend attempts reach max, lock resend OTP
        if user.resend_otp_attempts >= settings.MAX_RESEND_OTP_ATTEMPTS:
            user.otp_resend_locked_until = timezone.now() + timezone.timedelta(minutes=settings.RESEND_OTP_LOCK_DURATION_MINUTES)

        user.save()

        # Send OTP via email
        if user.email:
            subject = "Your Email OTP Code - Resend"
            html_content = f"<p>Your OTP code is {otp.email_otp}</p>"
            send_custom_email(subject, html_content, [user.email])

# View for Resending Mobile OTP
class ResendMobileOTPView(generics.GenericAPIView):
    serializer_class = ResendMobileOTPSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data.get('mobile')

        user = User.objects.get(mobile=mobile)

        # Check if resend OTP is locked
        if user.otp_resend_locked_until and timezone.now() < user.otp_resend_locked_until:
            lock_time_remaining = (user.otp_resend_locked_until - timezone.now()).seconds // 60  # in minutes
            return Response(
                {"detail": f"Resend OTP limit reached. Try again in {lock_time_remaining} minutes."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        # Check if resend attempts exceeded
        if user.resend_otp_attempts >= settings.MAX_RESEND_OTP_ATTEMPTS:
            user.otp_resend_locked_until = timezone.now() + timezone.timedelta(minutes=settings.RESEND_OTP_LOCK_DURATION_MINUTES)
            user.save()
            return Response(
                {"detail": "Resend OTP limit reached. Try again later."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        # Resend Mobile OTP
        self.resend_mobile_otp(user)
        return Response({"detail": "Mobile OTP resent."}, status=status.HTTP_200_OK)

    def resend_mobile_otp(self, user):
        """
        Generates and sends a new mobile OTP without affecting email OTP.
        """
        # Fetch the latest OTP
        try:
            otp = OTP.objects.filter(user=user).latest('created_at')
        except OTP.DoesNotExist:
            # Create a new OTP entry with both OTPs
            otp_email = generate_otp()
            otp_mobile = generate_otp()
            expiry_time = timezone.now() + timezone.timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
            otp = OTP.objects.create(
                user=user,
                email_otp=otp_email,
                mobile_otp=otp_mobile,
                expiry_time=expiry_time,
                is_verified=False,
                attempts=0
            )
        else:
            # Update only mobile_otp
            otp.mobile_otp = generate_otp()
            otp.expiry_time = timezone.now() + timezone.timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
            otp.is_verified = False
            otp.attempts = 0
            otp.save()

        # Increment resend attempts
        user.resend_otp_attempts += 1

        # If resend attempts reach max, lock resend OTP
        if user.resend_otp_attempts >= settings.MAX_RESEND_OTP_ATTEMPTS:
            user.otp_resend_locked_until = timezone.now() + timezone.timedelta(minutes=settings.RESEND_OTP_LOCK_DURATION_MINUTES)

        user.save()

        # Send OTP via SMS
        if user.mobile and user.country:
            full_mobile = f"{user.country.code}{user.mobile}"
            send_otp_sms(full_mobile, otp.mobile_otp)

# View for Verifying OTP
class UserVerificationView(generics.GenericAPIView):
    serializer_class = UserVerificationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Verify OTP and activate user.
        """
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            otp = OTP.objects.filter(user=user).latest('created_at')

            # Mark user as active
            user.is_active = True
            user.save()

            # Send welcome email
            if user.email:
                subject = 'Welcome to GrowUpMore'
                html_content = '<p>Your account has been successfully created.</p>'
                send_custom_email(subject, html_content, [user.email])

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)  # Now properly imported

            # Set JWT tokens in HttpOnly cookies
            response = Response({"detail": "User verified successfully."}, status=status.HTTP_200_OK)
            response.set_cookie(
                key='access',
                value=str(refresh.access_token),
                httponly=True,
                secure=not settings.DEBUG,  # Set to True in production
                samesite='Lax',
                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
            )
            response.set_cookie(
                key='refresh',
                value=str(refresh),
                httponly=True,
                secure=not settings.DEBUG,  # Set to True in production
                samesite='Lax',
                max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
            )
            return response
        except ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update the authenticated user's profile.
    Admin users can retrieve any profile by modifying the view as needed.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Return the authenticated user
        return self.request.user

class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handle user login.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        identifier = serializer.validated_data.get('identifier')
        password = serializer.validated_data.get('password')
        user_obj = serializer.validated_data.get('user')  # User object from serializer

        logger.debug(f"Login attempt for identifier: {identifier}")  # Now defined

        # Check if user is locked due to failed login attempts
        if user_obj.is_locked():
            lock_time_remaining = (user_obj.lock_until - timezone.now()).seconds // 60  # in minutes
            return Response(
                {"detail": f"Account locked due to multiple failed login attempts. Try again in {lock_time_remaining} minutes."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Authenticate user
        authenticated_user = authenticate(username=user_obj.email if user_obj.email else user_obj.mobile, password=password)

        if authenticated_user:
            logger.debug(f"User {authenticated_user} authenticated successfully.")
            if not authenticated_user.is_active:
                # User is not active, send OTP for verification
                self.send_verification_otp(authenticated_user)
                return Response(
                    {"detail": "Account is not active. OTP sent to email and mobile for verification."},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Reset failed login attempts on successful login
            authenticated_user.failed_login_attempts = 0
            authenticated_user.lock_until = None
            authenticated_user.save()

            # Generate JWT tokens
            refresh = RefreshToken.for_user(authenticated_user)

            # Determine KYC status
            kyc_status = "updated" if authenticated_user.is_kyc_updated else "not updated"

            # Set JWT tokens in HttpOnly cookies and include KYC status in response
            response = Response({"detail": "Login successful.", "kyc": kyc_status}, status=status.HTTP_200_OK)
            response.set_cookie(
                key=settings.SIMPLE_JWT['TOKEN_COOKIE'],
                value=str(refresh.access_token),
                httponly=True,
                secure=not settings.DEBUG,  # Set secure=True in production
                samesite='Strict',
                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
            )
            response.set_cookie(
                key=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE'],
                value=str(refresh),
                httponly=True,
                secure=not settings.DEBUG,  # Set secure=True in production
                samesite='Strict',
                max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
            )
            return response
        else:
            # Failed login attempt
            user_obj.failed_login_attempts += 1
            remaining_attempts = settings.MAX_LOGIN_ATTEMPTS - user_obj.failed_login_attempts

            if user_obj.failed_login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
                user_obj.lock_until = timezone.now() + timezone.timedelta(hours=settings.LOGIN_LOCK_DURATION_HOURS)
                user_obj.save()
                logger.warning(f"User {identifier} account locked due to multiple failed login attempts.")
                return Response(
                    {"detail": "Account locked due to multiple failed login attempts. Try again after 24 hours."},
                    status=status.HTTP_403_FORBIDDEN
                )

            user_obj.save()
            logger.warning(f"Failed login attempt for user: {identifier}. Attempts remaining: {remaining_attempts}")
            return Response(
                {"detail": f"Invalid credentials. {remaining_attempts} attempts remaining."},
                status=status.HTTP_401_UNAUTHORIZED
            )

    def send_verification_otp(self, user):
        """
        Sends OTP via email and SMS for account activation.
        """
        otp_email = generate_otp()
        otp_mobile = generate_otp()
        expiry_time = timezone.now() + timezone.timedelta(minutes=settings.OTP_EXPIRY_MINUTES)

        # Save OTP
        OTP.objects.create(user=user, email_otp=otp_email, mobile_otp=otp_mobile, expiry_time=expiry_time)

        # Send OTP via email
        if user.email:
            subject = "Your OTP Code for Account Activation"
            html_content = f"<p>Your OTP code is {otp_email}</p>"
            send_custom_email(subject, html_content, [user.email])

        # Send OTP via SMS
        if user.mobile and user.country:
            full_mobile = f"{user.country.code}{user.mobile}"
            send_otp_sms(full_mobile, otp_mobile)

# Add LogoutView
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handle user logout by clearing JWT cookies.
        """
        response = Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)
        response.delete_cookie(settings.SIMPLE_JWT['TOKEN_COOKIE'])
        response.delete_cookie(settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE'])
        return response
    
class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update the authenticated user's profile.
    Admin users can retrieve any profile by modifying the view as needed.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Return the authenticated user
        return self.request.user
    

class UpdateEmailView(generics.GenericAPIView):
    serializer_class = UpdateEmailSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Send OTP to new email for email update.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_email = serializer.validated_data.get('new_email')

        user = request.user

        # Check if resend OTP is locked
        if user.otp_resend_locked_until and timezone.now() < user.otp_resend_locked_until:
            lock_time_remaining = (user.otp_resend_locked_until - timezone.now()).seconds // 60  # in minutes
            return Response(
                {"detail": f"Resend OTP limit reached. Try again in {lock_time_remaining} minutes."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        # Check if resend attempts exceeded
        if user.resend_otp_attempts >= settings.MAX_RESEND_OTP_ATTEMPTS:
            user.otp_resend_locked_until = timezone.now() + timezone.timedelta(minutes=settings.RESEND_OTP_LOCK_DURATION_MINUTES)
            user.save()
            return Response(
                {"detail": "Resend OTP limit reached. Try again later."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        # Generate OTP
        email_otp = generate_otp()

        # Create or update OTP record
        otp_record, created = OTP.objects.get_or_create(user=user)
        otp_record.new_email = new_email
        otp_record.new_email_otp = email_otp
        otp_record.expiry_time = timezone.now() + timezone.timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
        otp_record.is_verified = False
        otp_record.attempts = 0
        otp_record.save()

        # Increment resend attempts
        user.resend_otp_attempts += 1
        if user.resend_otp_attempts >= settings.MAX_RESEND_OTP_ATTEMPTS:
            user.otp_resend_locked_until = timezone.now() + timezone.timedelta(minutes=settings.RESEND_OTP_LOCK_DURATION_MINUTES)
        user.save()

        # Send OTP via email
        subject = "Your Email Update OTP Code"
        html_content = f"<p>Your OTP code for updating your email is {email_otp}</p>"
        send_custom_email(subject, html_content, [new_email])

        logger.debug(f"Sent email OTP to {new_email} for user {user}")

        return Response({"detail": "OTP sent to new email."}, status=status.HTTP_200_OK)

class UpdateEmailVerifyView(generics.GenericAPIView):
    serializer_class = UpdateEmailVerifySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Verify OTP and update user's email. Logout immediately after.
        """
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data.get('otp')
        new_email = serializer.validated_data.get('new_email')

        user = request.user

        # Update user's email
        user.email = new_email
        user.save()

        # Mark OTP as verified
        otp.is_verified = True
        otp.save()

        # Logout user by clearing cookies
        response = Response({"detail": "Email updated successfully and you have been logged out."}, status=status.HTTP_200_OK)
        response.delete_cookie(settings.SIMPLE_JWT['TOKEN_COOKIE'])
        response.delete_cookie(settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE'])

        logger.debug(f"User {user} updated email to {new_email} and logged out.")

        return response

class UpdateMobileView(generics.GenericAPIView):
    serializer_class = UpdateMobileSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Send OTP to new mobile for mobile update.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_mobile = serializer.validated_data.get('new_mobile')
        country_id = serializer.validated_data.get('country')

        user = request.user

        # Check if resend OTP is locked
        if user.otp_resend_locked_until and timezone.now() < user.otp_resend_locked_until:
            lock_time_remaining = (user.otp_resend_locked_until - timezone.now()).seconds // 60  # in minutes
            return Response(
                {"detail": f"Resend OTP limit reached. Try again in {lock_time_remaining} minutes."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        # Check if resend attempts exceeded
        if user.resend_otp_attempts >= settings.MAX_RESEND_OTP_ATTEMPTS:
            user.otp_resend_locked_until = timezone.now() + timezone.timedelta(minutes=settings.RESEND_OTP_LOCK_DURATION_MINUTES)
            user.save()
            return Response(
                {"detail": "Resend OTP limit reached. Try again later."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        # Generate OTP
        mobile_otp = generate_otp()

        # Create or update OTP record
        otp_record, created = OTP.objects.get_or_create(user=user)
        otp_record.new_mobile = new_mobile
        otp_record.new_mobile_otp = mobile_otp
        otp_record.country = Country.objects.get(id=country_id)  # Ensure country exists
        otp_record.expiry_time = timezone.now() + timezone.timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
        otp_record.is_verified = False
        otp_record.attempts = 0
        otp_record.save()

        # Increment resend attempts
        user.resend_otp_attempts += 1
        if user.resend_otp_attempts >= settings.MAX_RESEND_OTP_ATTEMPTS:
            user.otp_resend_locked_until = timezone.now() + timezone.timedelta(minutes=settings.RESEND_OTP_LOCK_DURATION_MINUTES)
        user.save()

        # Send OTP via SMS
        full_mobile = f"{user.country.code}{new_mobile}"
        send_otp_sms(full_mobile, mobile_otp)

        logger.debug(f"Sent mobile OTP to {new_mobile} for user {user}")

        return Response({"detail": "OTP sent to new mobile."}, status=status.HTTP_200_OK)

class UpdateMobileVerifyView(generics.GenericAPIView):
    serializer_class = UpdateMobileVerifySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Verify OTP and update user's mobile. Logout immediately after.
        """
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data.get('otp')
        new_mobile = serializer.validated_data.get('new_mobile')
        country_id = serializer.validated_data.get('country')

        user = request.user

        # Update user's mobile and country
        user.mobile = new_mobile
        user.country = Country.objects.get(id=country_id)
        user.save()

        # Mark OTP as verified
        otp.is_verified = True
        otp.save()

        # Logout user by clearing cookies
        response = Response({"detail": "Mobile updated successfully and you have been logged out."}, status=status.HTTP_200_OK)
        response.delete_cookie(settings.SIMPLE_JWT['TOKEN_COOKIE'])
        response.delete_cookie(settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE'])

        logger.debug(f"User {user} updated mobile to {new_mobile} and logged out.")

        return response
    
class ChangePasswordView(generics.GenericAPIView):
    """
    View to change the user's password.
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to change password.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data.get('new_password')

        user = request.user
        user.set_password(new_password)
        user.save()

        # Logout user by clearing JWT cookies
        response = Response(
            {"detail": "Password changed successfully and you have been logged out."}, 
            status=status.HTTP_200_OK
        )
        response.delete_cookie(settings.SIMPLE_JWT['TOKEN_COOKIE'])
        response.delete_cookie(settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE'])

        logger.debug(f"User {user} changed password and was logged out.")

        return response
    
class ForgotPasswordView(generics.GenericAPIView):
    """
    View to handle password reset requests by sending OTPs to email and mobile.
    """
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        new_email = serializer.validated_data.get('email')
        new_mobile = serializer.validated_data.get('mobile')

        # Check if resend OTP is locked
        if user.otp_resend_locked_until and timezone.now() < user.otp_resend_locked_until:
            lock_time_remaining = (user.otp_resend_locked_until - timezone.now()).seconds // 60  # in minutes
            return Response(
                {"detail": f"Resend OTP limit reached. Try again in {lock_time_remaining} minutes."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        # Check if resend attempts exceeded
        if user.resend_otp_attempts >= settings.MAX_RESEND_OTP_ATTEMPTS:
            user.otp_resend_locked_until = timezone.now() + timezone.timedelta(minutes=settings.RESEND_OTP_LOCK_DURATION_MINUTES)
            user.save()
            return Response(
                {"detail": "Resend OTP limit reached. Try again later."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        # Generate OTPs
        email_otp = generate_otp()
        mobile_otp = generate_otp()

        # Create or update OTP record
        otp_record, created = OTP.objects.get_or_create(user=user)
        otp_record.email_otp = email_otp
        otp_record.mobile_otp = mobile_otp
        otp_record.expiry_time = timezone.now() + timezone.timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
        otp_record.is_verified = False
        otp_record.attempts = 0
        otp_record.save()

        # Increment resend attempts
        user.resend_otp_attempts += 1
        if user.resend_otp_attempts >= settings.MAX_RESEND_OTP_ATTEMPTS:
            user.otp_resend_locked_until = timezone.now() + timezone.timedelta(minutes=settings.RESEND_OTP_LOCK_DURATION_MINUTES)
        user.save()

        # Send OTP via email
        subject = "Your Password Reset OTP Code"
        html_content = f"<p>Your OTP code for resetting your password is {email_otp}</p>"
        send_custom_email(subject, html_content, [new_email])

        # Send OTP via SMS
        full_mobile = f"{user.country.code}{new_mobile}"
        send_otp_sms(full_mobile, mobile_otp)

        logger.debug(f"Sent password reset OTPs to email {new_email} and mobile {new_mobile} for user {user}")

        return Response({"detail": "OTPs sent to your email and mobile."}, status=status.HTTP_200_OK)

class ResetNewPasswordView(generics.GenericAPIView):
    """
    View to handle setting a new password after verifying OTPs.
    """
    serializer_class = ResetNewPasswordSerializer
    permission_classes = [AllowAny]  # AllowAny since user is not authenticated during password reset

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        otp_record = serializer.validated_data.get('otp_record')
        new_password = serializer.validated_data.get('password')

        # Update user's password
        user.set_password(new_password)
        user.save()

        # Mark OTP as verified
        otp_record.is_verified = True
        otp_record.save()

        # Logout user by clearing JWT cookies (if any are present)
        response = Response({"detail": "Password reset successfully. You have been logged out."}, status=status.HTTP_200_OK)
        response.delete_cookie(settings.SIMPLE_JWT['TOKEN_COOKIE'])
        response.delete_cookie(settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE'])

        logger.debug(f"User {user} reset their password and was logged out.")

        return response