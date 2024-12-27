# authapp/views.py

from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from .serializers import (
    UserRegistrationSerializer,
    OTPSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    CountrySerializer,
    Model1Serializer,
    Model2Serializer,
    Model3Serializer,
    CustomTokenObtainPairSerializer
)
from .models import User, OTP, FailedLoginAttempt, Country, Model1, Model2, Model3
from utils.email_utils import send_custom_email
from utils.sms_utils import send_sms
from utils.recaptcha import validate_recaptcha
import random
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .permissions import RoleBasedPermission
from .throttling import LoginRateThrottle, OTPRateThrottle
from django.conf import settings
from rest_framework import serializers
import logging

# Initialize logger
logger = logging.getLogger('authuser')

# Helper function to generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Custom TokenObtainPairView to handle account lockouts, set tokens in HTTP-only cookies, and set CSRF token
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    throttle_classes = [LoginRateThrottle]  # Apply throttle to login

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        mobile = request.data.get('mobile', None)
        password = request.data.get('password', None)
        ip_address = self.get_client_ip(request)

        # Determine the user based on email or mobile
        try:
            if email:
                user = User.objects.get(email=email)
            elif mobile:
                user = User.objects.get(mobile=mobile)
            else:
                return Response({"detail": "Email or mobile required."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            # To prevent user enumeration, respond with generic message
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if user is locked
        if user.is_locked:
            if user.lockout_until and timezone.now() < user.lockout_until:
                remaining = user.lockout_until - timezone.now()
                minutes = int(remaining.total_seconds() // 60)
                seconds = int(remaining.total_seconds() % 60)
                return Response({"detail": f"Account is locked. Try again in {minutes} minutes and {seconds} seconds."},
                                status=status.HTTP_403_FORBIDDEN)
            else:
                # Unlock the account
                user.is_locked = False
                user.lockout_until = None
                user.save()

        # Validate reCAPTCHA if not disabled
        if not settings.DISABLE_RECAPTCHA:
            recaptcha_token = request.data.get('recaptcha_token', None)
            if not recaptcha_token:
                return Response({"detail": "reCAPTCHA token is required."}, status=status.HTTP_400_BAD_REQUEST)
            if not validate_recaptcha(recaptcha_token):
                return Response({"detail": "Invalid reCAPTCHA. Please try again."}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate the user
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError:
            # Log the failed attempt
            FailedLoginAttempt.objects.create(user=user, ip_address=ip_address)
            # Check if the number of failed attempts exceeds threshold
            threshold = LOCKOUT_THRESHOLD
            time_window = LOCKOUT_DURATION

            recent_attempts = FailedLoginAttempt.objects.filter(
                user=user,
                timestamp__gte=timezone.now() - time_window
            ).count()

            if recent_attempts >= threshold:
                user.is_locked = True
                user.lockout_until = timezone.now() + time_window
                user.save()
                return Response({"detail": f"Account locked due to too many failed login attempts. Try again in {int(time_window.total_seconds() // 3600)} hours."},
                                status=status.HTTP_403_FORBIDDEN)
            else:
                remaining_attempts = threshold - recent_attempts
                return Response({"detail": f"Invalid credentials. You have {remaining_attempts} attempt(s) remaining before account lock."},
                                status=status.HTTP_401_UNAUTHORIZED)

        # Successful authentication; reset failed attempts
        FailedLoginAttempt.objects.filter(user=user).delete()

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)

        if response.status_code == status.HTTP_200_OK:
            # Set the access and refresh tokens in HTTP-only cookies
            access_token = serializer.validated_data.get('access')
            refresh_token = serializer.validated_data.get('refresh')
            
            # Set access token cookie
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=not request.is_secure(),
                samesite='Lax',
                max_age=15 * 60  # 15 minutes
            )
            # Set refresh token cookie
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=not request.is_secure(),
                samesite='Lax',
                max_age=24 * 60 * 60  # 1 day
            )
            
            # Remove tokens from response body for security
            response.data.pop('access', None)
            response.data.pop('refresh', None)
        
        return response

    def get_client_ip(self, request):
        """Utility method to get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

# Token Refresh View to set new access tokens in cookies
class CustomTokenRefreshView(TokenRefreshView):
    throttle_classes = [AnonRateThrottle]  # Apply throttle to refresh

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_200_OK:
            access_token = response.data.get('access')
            
            # Set the new access token in HTTP-only cookie
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=not request.is_secure(),
                samesite='Lax',
                max_age=15 * 60  # 15 minutes
            )
            
            # Remove access token from response body for security
            response.data.pop('access', None)
        
        return response

# User Registration
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    throttle_classes = [OTPRateThrottle]  # Apply throttling for OTP requests

    def perform_create(self, serializer):
        # Validate reCAPTCHA if not disabled
        if not settings.DISABLE_RECAPTCHA:
            recaptcha_token = self.request.data.get('recaptcha_token', None)
            if not recaptcha_token:
                raise serializers.ValidationError({"detail": "reCAPTCHA token is required."})
            if not validate_recaptcha(recaptcha_token):
                raise serializers.ValidationError({"detail": "Invalid reCAPTCHA. Please try again."})
        
        user = serializer.save()
        email_otp = generate_otp()
        mobile_otp = generate_otp()
        OTP.objects.create(user=user, code=email_otp, type='email')
        OTP.objects.create(user=user, code=mobile_otp, type='mobile')
        subject_email = "Verify your email"
        html_content_email = f"<p>Your Email OTP is {email_otp}. It is valid for 15 minutes.</p>"
        if user.email:
            send_custom_email(subject_email, html_content_email, [user.email])
        # Send OTP via SMS
        if user.country and user.mobile:
            destination = f"{user.country.code}{user.mobile}"
            sms_sent = send_sms(destination, mobile_otp, campaign_name="otp_verification")
            if not sms_sent:
                logger.error(f"Failed to send SMS OTP to {destination}")

    def get_serializer_context(self):
        return {'request': self.request}

# Resend OTP for Email or Mobile
class ResendOTPView(generics.GenericAPIView):
    serializer_class = OTPSerializer
    permission_classes = [AllowAny]
    throttle_classes = [OTPRateThrottle]  # Apply throttling for OTP requests

    def post(self, request):
        email = request.data.get('email', None)
        mobile = request.data.get('mobile', None)
        otp_type = request.data.get('type', None)

        if not otp_type or otp_type not in ['email', 'mobile']:
            return Response({"detail": "OTP type ('email' or 'mobile') is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if email and otp_type == 'email':
                user = User.objects.get(email=email)
                recipient = [user.email]
                subject = "Resend Email OTP"
                email_otp = generate_otp()
                html_content = f"<p>Your new Email OTP is {email_otp}. It is valid for 15 minutes.</p>"
                # Invalidate previous OTPs
                user.otps.filter(type='email').update(is_verified=True)
                OTP.objects.create(user=user, code=email_otp, type='email')
                send_custom_email(subject, html_content, recipient)
                return Response({"detail": "Email OTP resent successfully."}, status=status.HTTP_200_OK)
            elif mobile and otp_type == 'mobile':
                user = User.objects.get(mobile=mobile)
                if user.country and user.mobile:
                    destination = f"{user.country.code}{user.mobile}"
                    # Invalidate previous OTPs
                    user.otps.filter(type='mobile').update(is_verified=True)
                    mobile_otp = generate_otp()
                    OTP.objects.create(user=user, code=mobile_otp, type='mobile')
                    sms_sent = send_sms(destination, mobile_otp, campaign_name="otp_verification")
                    if sms_sent:
                        return Response({"detail": "Mobile OTP resent successfully."}, status=status.HTTP_200_OK)
                    else:
                        return Response({"detail": "Failed to send Mobile OTP."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({"detail": "Country or mobile number not set for user."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Invalid request data."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"detail": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)

# Verify OTP for Email and Mobile Together
class VerifyOTPView(generics.GenericAPIView):
    serializer_class = OTPSerializer
    permission_classes = [AllowAny]
    throttle_classes = [OTPRateThrottle]  # Apply throttling for OTP verification

    def post(self, request):
        email = request.data.get('email', None)
        mobile = request.data.get('mobile', None)
        email_code = request.data.get('email_code', None)
        mobile_code = request.data.get('mobile_code', None)

        # Ensure both email and mobile are provided
        if not email or not mobile:
            return Response({"detail": "Both email and mobile are required."}, status=status.HTTP_400_BAD_REQUEST)
        if not email_code or not mobile_code:
            return Response({"detail": "Both email_code and mobile_code are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email, mobile=mobile)
            
            # Verify Email OTP
            try:
                email_otp = user.otps.filter(code=email_code, is_verified=False, type='email').latest('created_at')
                if email_otp and (timezone.now() - email_otp.created_at) < timedelta(minutes=15):
                    email_otp.is_verified = True
                    email_otp.save()
                else:
                    return Response({"detail": "Invalid or expired Email OTP."}, status=status.HTTP_400_BAD_REQUEST)
            except OTP.DoesNotExist:
                return Response({"detail": "Email OTP not found."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Verify Mobile OTP
            try:
                mobile_otp = user.otps.filter(code=mobile_code, is_verified=False, type='mobile').latest('created_at')
                if mobile_otp and (timezone.now() - mobile_otp.created_at) < timedelta(minutes=15):
                    mobile_otp.is_verified = True
                    mobile_otp.save()
                else:
                    return Response({"detail": "Invalid or expired Mobile OTP."}, status=status.HTTP_400_BAD_REQUEST)
            except OTP.DoesNotExist:
                return Response({"detail": "Mobile OTP not found."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if both OTPs are verified
            email_verified = user.otps.filter(type='email', is_verified=True).exists()
            mobile_verified = user.otps.filter(type='mobile', is_verified=True).exists()

            if email_verified and mobile_verified:
                user.is_active = True
                user.save()
                return Response({"detail": "All OTPs verified successfully. Account activated."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Both Email and Mobile OTPs need to be verified."}, status=status.HTTP_400_BAD_REQUEST)
        
        except User.DoesNotExist:
            return Response({"detail": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)

# Activate Account (Resend OTPs for inactive users)
class ActivateAccountView(generics.GenericAPIView):
    serializer_class = OTPSerializer
    permission_classes = [AllowAny]
    throttle_classes = [OTPRateThrottle]  # Apply throttling for OTP requests

    def post(self, request):
        email = request.data.get('email', None)
        mobile = request.data.get('mobile', None)
        if not email or not mobile:
            return Response({"detail": "Both email and mobile are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email, mobile=mobile)
            if user.is_active:
                return Response({"detail": "Account is already active."}, status=status.HTTP_400_BAD_REQUEST)
            # Invalidate previous OTPs
            user.otps.update(is_verified=True)
            email_otp = generate_otp()
            mobile_otp = generate_otp()
            OTP.objects.create(user=user, code=email_otp, type='email')
            OTP.objects.create(user=user, code=mobile_otp, type='mobile')
            subject_email = "Activate your email"
            html_content_email = f"<p>Your new Email OTP is {email_otp}. It is valid for 15 minutes.</p>"
            send_custom_email(subject_email, html_content_email, [user.email])
            # Send OTP via SMS
            if user.country and user.mobile:
                destination = f"{user.country.code}{user.mobile}"
                sms_sent = send_sms(destination, mobile_otp, campaign_name="activation")
                if not sms_sent:
                    logger.error(f"Failed to send SMS OTP to {destination}")
            return Response({"detail": "Activation OTPs sent."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)

# Forgot Password
class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny]
    throttle_classes = [OTPRateThrottle]  # Apply throttling for OTP requests

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                # Invalidate previous OTPs
                user.otps.update(is_verified=True)
                email_otp = generate_otp()
                mobile_otp = generate_otp()
                OTP.objects.create(user=user, code=email_otp, type='email')
                OTP.objects.create(user=user, code=mobile_otp, type='mobile')
                subject_email = "Password Reset OTP for Email"
                html_content_email = f"<p>Your Password Reset Email OTP is {email_otp}. It is valid for 15 minutes.</p>"
                send_custom_email(subject_email, html_content_email, [user.email])
                # Send OTP via SMS
                if user.country and user.mobile:
                    destination = f"{user.country.code}{user.mobile}"
                    sms_sent = send_sms(destination, mobile_otp, campaign_name="password_reset")
                    if not sms_sent:
                        logger.error(f"Failed to send SMS OTP to {destination}")
                return Response({"detail": "Password reset OTPs sent to email and mobile."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"detail": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Reset Password
class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]
    throttle_classes = [OTPRateThrottle]  # Apply throttling for OTP verification

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            email_code = serializer.validated_data['email_code']
            mobile_code = serializer.validated_data['mobile_code']
            new_password = serializer.validated_data['new_password']
            try:
                user = User.objects.get(email=email)
                # Verify Email OTP
                try:
                    email_otp = user.otps.filter(code=email_code, is_verified=False, type='email').latest('created_at')
                    if email_otp and (timezone.now() - email_otp.created_at) < timedelta(minutes=15):
                        email_otp.is_verified = True
                        email_otp.save()
                    else:
                        return Response({"detail": "Invalid or expired Email OTP."}, status=status.HTTP_400_BAD_REQUEST)
                except OTP.DoesNotExist:
                    return Response({"detail": "Email OTP not found."}, status=status.HTTP_400_BAD_REQUEST)
                
                # Verify Mobile OTP
                try:
                    mobile_otp = user.otps.filter(code=mobile_code, is_verified=False, type='mobile').latest('created_at')
                    if mobile_otp and (timezone.now() - mobile_otp.created_at) < timedelta(minutes=15):
                        mobile_otp.is_verified = True
                        mobile_otp.save()
                    else:
                        return Response({"detail": "Invalid or expired Mobile OTP."}, status=status.HTTP_400_BAD_REQUEST)
                except OTP.DoesNotExist:
                    return Response({"detail": "Mobile OTP not found."}, status=status.HTTP_400_BAD_REQUEST)

                # Set new password
                user.set_password(new_password)
                user.save()
                return Response({"detail": "Password reset successfully."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"detail": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Change Password
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]  # Apply throttling for password changes

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()

        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Check if current_password is correct
            if not self.object.check_password(serializer.validated_data['current_password']):
                return Response({"current_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            # Set new password
            self.object.set_password(serializer.validated_data['new_password'])
            self.object.save()
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Profile View
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_object(self):
        return self.request.user

# Logout View
class LogoutView(generics.GenericAPIView):
    """
    Logout the user by clearing the access and refresh tokens from the cookies.
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        response.delete_cookie('csrftoken')  # Optionally delete CSRF token as well
        return response

# Additional Model Views with Permissions using RoleBasedPermission

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [RoleBasedPermission]
    throttle_classes = [UserRateThrottle]

class Model1ViewSet(viewsets.ModelViewSet):
    queryset = Model1.objects.all()
    serializer_class = Model1Serializer
    permission_classes = [RoleBasedPermission]
    throttle_classes = [UserRateThrottle]

class Model2ViewSet(viewsets.ModelViewSet):
    queryset = Model2.objects.all()
    serializer_class = Model2Serializer
    permission_classes = [RoleBasedPermission]
    throttle_classes = [UserRateThrottle]

class Model3ViewSet(viewsets.ModelViewSet):
    queryset = Model3.objects.all()
    serializer_class = Model3Serializer
    permission_classes = [RoleBasedPermission]
    throttle_classes = [UserRateThrottle]
