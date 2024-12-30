# authuser/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User
from master.models import Country, State, City
from utils.models import OTP
from django.contrib.auth import authenticate
from utils.email_utils import send_custom_email
from utils.sms_otp_utils import send_otp_sms
from django.conf import settings
from django.utils import timezone
import requests
from utils.utils import generate_otp 

User = get_user_model()

USER_TYPE_CHOICES = (
    ('student', 'Student'),
    ('instructor', 'Instructor'),
    ('institute', 'Institute'),
)

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=USER_TYPE_CHOICES)
    google_recaptcha_v3_token = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['email', 'mobile', 'password', 'user_type', 'country', 'google_recaptcha_v3_token']

    def validate(self, attrs):
        email = attrs.get('email', None)
        mobile = attrs.get('mobile', None)
        user_type = attrs.get('user_type', None)
        country = attrs.get('country', None)

        if not email and not mobile:
            raise serializers.ValidationError("Either email or mobile must be provided.")

        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists.")

        if mobile and User.objects.filter(mobile=mobile).exists():
            raise serializers.ValidationError("Mobile number already exists.")

        if user_type not in dict(USER_TYPE_CHOICES):
            raise serializers.ValidationError("Invalid user type.")

        if not Country.objects.filter(id=country.id).exists():
            raise serializers.ValidationError("Country does not exist.")

        # Validate reCAPTCHA if not disabled
        google_recaptcha_v3_token = attrs.get('google_recaptcha_v3_token', None)
        if not settings.DISABLE_RECAPTCHA:
            if not google_recaptcha_v3_token:
                raise serializers.ValidationError("Google reCAPTCHA token is required.")
            if not self.validate_recaptcha(google_recaptcha_v3_token):
                raise serializers.ValidationError("Invalid reCAPTCHA. Please try again.")

        return attrs

    def validate_recaptcha(self, token):
        """
        Validates Google reCAPTCHA v3 token.
        """
        secret_key = settings.GOOGLE_RECAPTCHA_SECRET_KEY
        data = {
            'secret': secret_key,
            'response': token
        }
        try:
            response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = response.json()
            return result.get('success', False)
        except Exception as e:
            raise serializers.ValidationError("reCAPTCHA validation failed.")

    def create(self, validated_data):
        google_recaptcha_v3_token = validated_data.pop('google_recaptcha_v3_token', None)
        user = User.objects.create_user(**validated_data)
        self.create_otp(user)
        return user

    def create_otp(self, user):
        """
        Generates OTPs, saves them, and sends via email and SMS.
        """
        otp_email = generate_otp()
        otp_mobile = generate_otp()
        expiry_time = timezone.now() + timezone.timedelta(minutes=settings.OTP_EXPIRY_MINUTES)

        # Save OTP
        OTP.objects.create(user=user, email_otp=otp_email, mobile_otp=otp_mobile, expiry_time=expiry_time)

        # Send OTP via email
        if user.email:
            subject = "Your OTP Code"
            html_content = f"<p>Your OTP code is {otp_email}</p>"
            send_custom_email(subject, html_content, [user.email])

        # Send OTP via SMS
        if user.mobile and user.country:
            full_mobile = f"{user.country.code}{user.mobile}"
            send_otp_sms(full_mobile, otp_mobile)

class ResendEmailOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    google_recaptcha_v3_token = serializers.CharField(
        write_only=True,
        required=not settings.DISABLE_RECAPTCHA,
        allow_blank=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        google_recaptcha_v3_token = attrs.get('google_recaptcha_v3_token', None)

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email does not exist.")

        # Validate reCAPTCHA if not disabled
        if not settings.DISABLE_RECAPTCHA:
            if not google_recaptcha_v3_token:
                raise serializers.ValidationError("Google reCAPTCHA token is required.")
            if not self.validate_recaptcha(google_recaptcha_v3_token):
                raise serializers.ValidationError("Invalid reCAPTCHA. Please try again.")

        return attrs

    def validate_recaptcha(self, token):
        secret_key = settings.GOOGLE_RECAPTCHA_SECRET_KEY
        data = {
            'secret': secret_key,
            'response': token
        }
        try:
            response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = response.json()
            return result.get('success', False)
        except Exception:
            raise serializers.ValidationError("reCAPTCHA validation failed.")

# Serializer for Resending Mobile OTP
class ResendMobileOTPSerializer(serializers.Serializer):
    mobile = serializers.CharField()
    google_recaptcha_v3_token = serializers.CharField(
        write_only=True,
        required=not settings.DISABLE_RECAPTCHA,
        allow_blank=True
    )

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        google_recaptcha_v3_token = attrs.get('google_recaptcha_v3_token', None)

        if not User.objects.filter(mobile=mobile).exists():
            raise serializers.ValidationError("User with this mobile does not exist.")

        # Validate reCAPTCHA if not disabled
        if not settings.DISABLE_RECAPTCHA:
            if not google_recaptcha_v3_token:
                raise serializers.ValidationError("Google reCAPTCHA token is required.")
            if not self.validate_recaptcha(google_recaptcha_v3_token):
                raise serializers.ValidationError("Invalid reCAPTCHA. Please try again.")

        return attrs

    def validate_recaptcha(self, token):
        secret_key = settings.GOOGLE_RECAPTCHA_SECRET_KEY
        data = {
            'secret': secret_key,
            'response': token
        }
        try:
            response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = response.json()
            return result.get('success', False)
        except Exception:
            raise serializers.ValidationError("reCAPTCHA validation failed.")
        
class UserLoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)
    google_recaptcha_v3_token = serializers.CharField(write_only=True, required=not settings.DISABLE_RECAPTCHA, allow_blank=True)

    def validate(self, attrs):
        identifier = attrs.get('identifier')
        password = attrs.get('password')
        google_recaptcha_v3_token = attrs.get('google_recaptcha_v3_token', None)

        if not settings.DISABLE_RECAPTCHA:
            if not google_recaptcha_v3_token:
                raise serializers.ValidationError("Google reCAPTCHA token is required.")
            if not self.validate_recaptcha(google_recaptcha_v3_token):
                raise serializers.ValidationError("Invalid reCAPTCHA. Please try again.")

        # Determine if identifier is email or mobile
        if '@' in identifier:
            try:
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid credentials.")
        else:
            try:
                user = User.objects.get(mobile=identifier)
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid credentials.")

        attrs['user'] = user
        return attrs

    def validate_recaptcha(self, token):
        """
        Validates Google reCAPTCHA v3 token.
        """
        secret_key = settings.GOOGLE_RECAPTCHA_SECRET_KEY
        data = {
            'secret': secret_key,
            'response': token
        }
        try:
            response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = response.json()
            return result.get('success', False)
        except Exception as e:
            raise serializers.ValidationError("reCAPTCHA validation failed.")

class UserVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_null=True)
    mobile = serializers.CharField(required=False, allow_null=True)
    email_otp = serializers.CharField(max_length=6, required=False, allow_blank=True)
    mobile_otp = serializers.CharField(max_length=6, required=False, allow_blank=True)
    google_recaptcha_v3_token = serializers.CharField(
        write_only=True,
        required=not settings.DISABLE_RECAPTCHA,
        allow_blank=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        mobile = attrs.get('mobile')
        email_otp = attrs.get('email_otp')
        mobile_otp = attrs.get('mobile_otp')
        google_recaptcha_v3_token = attrs.get('google_recaptcha_v3_token', None)

        # Validate reCAPTCHA if not disabled
        if not settings.DISABLE_RECAPTCHA:
            if not google_recaptcha_v3_token:
                raise serializers.ValidationError("Google reCAPTCHA token is required.")
            if not self.validate_recaptcha(google_recaptcha_v3_token):
                raise serializers.ValidationError("Invalid reCAPTCHA. Please try again.")

        if not email and not mobile:
            raise serializers.ValidationError("Either email or mobile must be provided for verification.")

        try:
            if email and mobile:
                user = User.objects.get(email=email, mobile=mobile)
            elif email:
                user = User.objects.get(email=email)
            elif mobile:
                user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with provided email or mobile does not exist.")

        try:
            # Fetch the latest OTP for the user
            otp = OTP.objects.filter(user=user).latest('created_at')
        except OTP.DoesNotExist:
            raise serializers.ValidationError("No OTP found for this user.")

        if otp.is_verified:
            raise serializers.ValidationError("OTP already verified.")

        if otp.expiry_time < timezone.now():
            raise serializers.ValidationError("OTP has expired.")

        if otp.attempts >= settings.OTP_MAX_ATTEMPTS:
            # Lock the account
            user.lock_until = timezone.now() + timezone.timedelta(hours=settings.LOGIN_LOCK_DURATION_HOURS)
            user.is_active = False
            user.save()
            raise serializers.ValidationError("Account locked due to multiple failed verification attempts. Try again after 24 hours.")

        # Validate Email OTP if provided
        if email:
            if not otp.email_otp or otp.email_otp != email_otp:
                otp.attempts += 1
                otp.save()
                remaining_attempts = settings.OTP_MAX_ATTEMPTS - otp.attempts
                raise serializers.ValidationError(f"Invalid Email OTP. {remaining_attempts} attempts remaining.")

        # Validate Mobile OTP if provided
        if mobile:
            if not otp.mobile_otp or otp.mobile_otp != mobile_otp:
                otp.attempts += 1
                otp.save()
                remaining_attempts = settings.OTP_MAX_ATTEMPTS - otp.attempts
                raise serializers.ValidationError(f"Invalid Mobile OTP. {remaining_attempts} attempts remaining.")

        # If all provided OTPs are correct, mark as verified
        otp.is_verified = True
        otp.save()

        attrs['user'] = user
        return attrs

    def validate_recaptcha(self, token):
        """
        Validates Google reCAPTCHA v3 token.
        """
        secret_key = settings.GOOGLE_RECAPTCHA_SECRET_KEY
        data = {
            'secret': secret_key,
            'response': token
        }
        try:
            response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = response.json()
            return result.get('success', False)
        except Exception:
            raise serializers.ValidationError("reCAPTCHA validation failed.")


class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    birth_date = serializers.DateField(required=False, allow_null=True)
    gender = serializers.ChoiceField(
        choices=(('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')),
        required=False,
        allow_blank=True
    )
    nationality = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    state = serializers.PrimaryKeyRelatedField(
        queryset=State.objects.all(),
        required=False,
        allow_null=True
    )
    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(),
        required=False,
        allow_null=True
    )
    postal_code = serializers.CharField(
        required=False,
        allow_blank=True
    )
    institute_name = serializers.CharField(required=False, allow_blank=True)

    is_kyc_updated = serializers.BooleanField(read_only=True)  # Users cannot modify this field directly

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'mobile',
            'user_type',
            'country',
            'state',
            'city',
            'is_active',
            'date_joined',
            'first_name',
            'last_name',
            'birth_date',
            'gender',
            'nationality',
            'address',
            'postal_code',
            'institute_name',
            'is_kyc_updated',
        ]
        read_only_fields = [
            'id',
            'email',
            'mobile',
            'user_type',
            'country',
            'state',
            'city',
            'is_active',
            'date_joined',
            'is_kyc_updated',
        ]

    def __init__(self, *args, **kwargs):
        super(UserProfileSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request:
            user = request.user
            user_type = user.user_type
            is_staff = user.is_staff

            if user_type in ['student', 'instructor'] or is_staff:
                # Exclude 'institute_name' for students, instructors, and employees
                self.fields.pop('institute_name', None)
            elif user_type == 'institute':
                # Exclude 'gender' for institutes
                self.fields.pop('gender', None)
            else:
                # For any other user types, you can define default behavior or exclude both
                self.fields.pop('institute_name', None)
                self.fields.pop('gender', None)

    def update(self, instance, validated_data):
        # Update the user instance with validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Determine if KYC should be updated
        user_type = instance.user_type
        kyc_fields = []
        if user_type in ['student', 'instructor'] or instance.is_staff:
            kyc_fields = [
                'first_name',
                'last_name',
                'birth_date',
                'gender',
                'nationality',
                'address',
                'country',
                'state',
                'city',
                'postal_code',
            ]
        elif user_type == 'institute':
            kyc_fields = [
                'first_name',
                'last_name',
                'institute_name',
                'birth_date',
                'nationality',
                'address',
                'country',
                'state',
                'city',
                'postal_code',
            ]

        # Check if all required KYC fields are filled
        kyc_completed = True
        for field in kyc_fields:
            value = getattr(instance, field)
            if value in [None, '', 'NA', 0]:
                kyc_completed = False
                break

        if kyc_completed and not instance.is_kyc_updated:
            instance.is_kyc_updated = True
            instance.save()
            # logger.info(f"KYC approved for user {instance.email if instance.email else instance.mobile}")

        return instance

class UpdateEmailSerializer(serializers.Serializer):
    new_email = serializers.EmailField()
    google_recaptcha_v3_token = serializers.CharField(
        write_only=True,
        required=not settings.DISABLE_RECAPTCHA,
        allow_blank=True
    )

    def validate_new_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate(self, attrs):
        google_recaptcha_v3_token = attrs.get('google_recaptcha_v3_token', None)
        if not settings.DISABLE_RECAPTCHA:
            if not google_recaptcha_v3_token:
                raise serializers.ValidationError("Google reCAPTCHA token is required.")
            if not self.validate_recaptcha(google_recaptcha_v3_token):
                raise serializers.ValidationError("Invalid reCAPTCHA. Please try again.")
        return attrs

    def validate_recaptcha(self, token):
        """
        Validates Google reCAPTCHA v3 token.
        """
        secret_key = settings.GOOGLE_RECAPTCHA_SECRET_KEY
        data = {
            'secret': secret_key,
            'response': token
        }
        try:
            response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = response.json()
            return result.get('success', False)
        except Exception as e:
            raise serializers.ValidationError("reCAPTCHA validation failed.")

class UpdateEmailVerifySerializer(serializers.Serializer):
    new_email = serializers.EmailField()
    email_otp = serializers.CharField(max_length=6)
    google_recaptcha_v3_token = serializers.CharField(
        write_only=True,
        required=not settings.DISABLE_RECAPTCHA,
        allow_blank=True
    )

    def validate(self, attrs):
        new_email = attrs.get('new_email')
        email_otp = attrs.get('email_otp')
        google_recaptcha_v3_token = attrs.get('google_recaptcha_v3_token', None)

        if User.objects.filter(email=new_email).exists():
            raise serializers.ValidationError("Email already exists.")

        if not settings.DISABLE_RECAPTCHA:
            if not google_recaptcha_v3_token:
                raise serializers.ValidationError("Google reCAPTCHA token is required.")
            if not self.validate_recaptcha(google_recaptcha_v3_token):
                raise serializers.ValidationError("Invalid reCAPTCHA. Please try again.")

        try:
            # Get the latest OTP record with new_email and new_email_otp
            otp = OTP.objects.filter(
                user=self.context['request'].user,
                new_email=new_email,
                new_email_otp=email_otp
            ).latest('created_at')
        except OTP.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP or email.")

        if otp.expiry_time < timezone.now():
            raise serializers.ValidationError("OTP has expired.")

        if otp.attempts >= settings.OTP_MAX_ATTEMPTS:
            user = self.context['request'].user
            user.lock_until = timezone.now() + timezone.timedelta(hours=settings.LOGIN_LOCK_DURATION_HOURS)
            user.is_active = False
            user.save()
            raise serializers.ValidationError("Account locked due to multiple failed verification attempts. Try again after 24 hours.")

        attrs['otp'] = otp
        return attrs

    def validate_recaptcha(self, token):
        """
        Validates Google reCAPTCHA v3 token.
        """
        secret_key = settings.GOOGLE_RECAPTCHA_SECRET_KEY
        data = {
            'secret': secret_key,
            'response': token
        }
        try:
            response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = response.json()
            return result.get('success', False)
        except Exception:
            raise serializers.ValidationError("reCAPTCHA validation failed.")

class UpdateMobileSerializer(serializers.Serializer):
    new_mobile = serializers.CharField(max_length=15)
    country = serializers.IntegerField()
    google_recaptcha_v3_token = serializers.CharField(
        write_only=True,
        required=not settings.DISABLE_RECAPTCHA,
        allow_blank=True
    )

    def validate_new_mobile(self, value):
        if User.objects.filter(mobile=value).exists():
            raise serializers.ValidationError("Mobile number already exists.")
        return value

    def validate_country(self, value):
        if not Country.objects.filter(id=value).exists():
            raise serializers.ValidationError("Country does not exist.")
        return value

    def validate(self, attrs):
        google_recaptcha_v3_token = attrs.get('google_recaptcha_v3_token', None)
        if not settings.DISABLE_RECAPTCHA:
            if not google_recaptcha_v3_token:
                raise serializers.ValidationError("Google reCAPTCHA token is required.")
            if not self.validate_recaptcha(google_recaptcha_v3_token):
                raise serializers.ValidationError("Invalid reCAPTCHA. Please try again.")
        return attrs

    def validate_recaptcha(self, token):
        """
        Validates Google reCAPTCHA v3 token.
        """
        secret_key = settings.GOOGLE_RECAPTCHA_SECRET_KEY
        data = {
            'secret': secret_key,
            'response': token
        }
        try:
            response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = response.json()
            return result.get('success', False)
        except Exception:
            raise serializers.ValidationError("reCAPTCHA validation failed.")

class UpdateMobileVerifySerializer(serializers.Serializer):
    new_mobile = serializers.CharField(max_length=15)
    country = serializers.IntegerField()
    mobile_otp = serializers.CharField(max_length=6)
    google_recaptcha_v3_token = serializers.CharField(
        write_only=True,
        required=not settings.DISABLE_RECAPTCHA,
        allow_blank=True
    )

    def validate(self, attrs):
        new_mobile = attrs.get('new_mobile')
        country = attrs.get('country')
        mobile_otp = attrs.get('mobile_otp')
        google_recaptcha_v3_token = attrs.get('google_recaptcha_v3_token', None)

        if User.objects.filter(mobile=new_mobile).exists():
            raise serializers.ValidationError("Mobile number already exists.")

        if not Country.objects.filter(id=country).exists():
            raise serializers.ValidationError("Country does not exist.")

        if not settings.DISABLE_RECAPTCHA:
            if not google_recaptcha_v3_token:
                raise serializers.ValidationError("Google reCAPTCHA token is required.")
            if not self.validate_recaptcha(google_recaptcha_v3_token):
                raise serializers.ValidationError("Invalid reCAPTCHA. Please try again.")

        try:
            # Get the latest OTP record with new_mobile and new_mobile_otp
            otp = OTP.objects.filter(
                user=self.context['request'].user,
                new_mobile=new_mobile,
                new_mobile_otp=mobile_otp
            ).latest('created_at')
        except OTP.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP or mobile number.")

        if otp.expiry_time < timezone.now():
            raise serializers.ValidationError("OTP has expired.")

        if otp.attempts >= settings.OTP_MAX_ATTEMPTS:
            user = self.context['request'].user
            user.lock_until = timezone.now() + timezone.timedelta(hours=settings.LOGIN_LOCK_DURATION_HOURS)
            user.is_active = False
            user.save()
            raise serializers.ValidationError("Account locked due to multiple failed verification attempts. Try again after 24 hours.")

        attrs['otp'] = otp
        return attrs

    def validate_recaptcha(self, token):
        """
        Validates Google reCAPTCHA v3 token.
        """
        secret_key = settings.GOOGLE_RECAPTCHA_SECRET_KEY
        data = {
            'secret': secret_key,
            'response': token
        }
        try:
            response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = response.json()
            return result.get('success', False)
        except Exception:
            raise serializers.ValidationError("reCAPTCHA validation failed.")
        
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True, 
        write_only=True, 
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True, 
        write_only=True, 
        style={'input_type': 'password'},
        min_length=8,
        help_text="Password must be at least 8 characters long."
    )

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")
        return value

    def validate_new_password(self, value):
        # Add additional password validations if necessary (e.g., complexity)
        return value
    
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    mobile = serializers.CharField(max_length=15, required=True)
    google_recaptcha_v3_token = serializers.CharField(
        write_only=True,
        required=not settings.DISABLE_RECAPTCHA,
        allow_blank=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        mobile = attrs.get('mobile')
        google_recaptcha_v3_token = attrs.get('google_recaptcha_v3_token', None)

        # Validate reCAPTCHA if enabled
        if not settings.DISABLE_RECAPTCHA:
            if not google_recaptcha_v3_token:
                raise serializers.ValidationError("Google reCAPTCHA token is required.")
            if not self.validate_recaptcha(google_recaptcha_v3_token):
                raise serializers.ValidationError("Invalid reCAPTCHA. Please try again.")

        # Check if the combination of email and mobile exists
        try:
            user = User.objects.get(email=email, mobile=mobile)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with the provided email and mobile.")

        attrs['user'] = user
        return attrs

    def validate_recaptcha(self, token):
        """
        Validates Google reCAPTCHA v3 token.
        """
        secret_key = settings.GOOGLE_RECAPTCHA_SECRET_KEY
        data = {
            'secret': secret_key,
            'response': token
        }
        try:
            response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = response.json()
            return result.get('success', False)
        except Exception:
            raise serializers.ValidationError("reCAPTCHA validation failed.")

class ResetNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    mobile = serializers.CharField(max_length=15, required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
        min_length=8,
        help_text="Password must be at least 8 characters long."
    )
    email_otp = serializers.CharField(max_length=6, required=True)
    mobile_otp = serializers.CharField(max_length=6, required=True)
    google_recaptcha_v3_token = serializers.CharField(
        write_only=True,
        required=not settings.DISABLE_RECAPTCHA,
        allow_blank=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        mobile = attrs.get('mobile')
        password = attrs.get('password')
        email_otp = attrs.get('email_otp')
        mobile_otp = attrs.get('mobile_otp')
        google_recaptcha_v3_token = attrs.get('google_recaptcha_v3_token', None)

        # Validate reCAPTCHA if enabled
        if not settings.DISABLE_RECAPTCHA:
            if not google_recaptcha_v3_token:
                raise serializers.ValidationError("Google reCAPTCHA token is required.")
            if not self.validate_recaptcha(google_recaptcha_v3_token):
                raise serializers.ValidationError("Invalid reCAPTCHA. Please try again.")

        # Check if the combination of email and mobile exists
        try:
            user = User.objects.get(email=email, mobile=mobile)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with the provided email and mobile.")

        # Retrieve the latest OTP record for password reset
        try:
            otp_record = OTP.objects.filter(
                user=user,
                email_otp=email_otp,
                mobile_otp=mobile_otp
            ).latest('created_at')
        except OTP.DoesNotExist:
            raise serializers.ValidationError("Invalid OTPs provided.")

        # Check OTP expiry
        if otp_record.expiry_time < timezone.now():
            raise serializers.ValidationError("OTP has expired.")

        # Check OTP attempts
        if otp_record.attempts >= settings.OTP_MAX_ATTEMPTS:
            user.lock_until = timezone.now() + timezone.timedelta(hours=settings.LOGIN_LOCK_DURATION_HOURS)
            user.is_active = False
            user.save()
            raise serializers.ValidationError("Account locked due to multiple failed verification attempts. Try again after 24 hours.")

        attrs['user'] = user
        attrs['otp_record'] = otp_record
        return attrs

    def validate_recaptcha(self, token):
        """
        Validates Google reCAPTCHA v3 token.
        """
        secret_key = settings.GOOGLE_RECAPTCHA_SECRET_KEY
        data = {
            'secret': secret_key,
            'response': token
        }
        try:
            response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = response.json()
            return result.get('success', False)
        except Exception:
            raise serializers.ValidationError("reCAPTCHA validation failed.")