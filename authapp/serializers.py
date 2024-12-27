# authapp/serializers.py

from rest_framework import serializers
from .models import User, OTP, Country, Model1, Model2, Model3
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    user_type = serializers.ChoiceField(choices=(
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('institute', 'Institute'),
    ), required=True)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), required=True)

    class Meta:
        model = User
        fields = ('email', 'mobile', 'password', 'user_type', 'country')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get('email'),
            mobile=validated_data.get('mobile'),
            password=validated_data.get('password'),
            user_type=validated_data.get('user_type'),
            country=validated_data.get('country')
        )
        return user

class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    mobile = serializers.CharField(required=False)
    email_code = serializers.CharField(max_length=4, required=False)
    mobile_code = serializers.CharField(max_length=4, required=False)
    type = serializers.ChoiceField(choices=(
        ('email', 'Email'),
        ('mobile', 'Mobile'),
    ), required=False)

    def validate(self, attrs):
        email = attrs.get('email', None)
        mobile = attrs.get('mobile', None)
        email_code = attrs.get('email_code', None)
        mobile_code = attrs.get('mobile_code', None)

        if (email and not email_code) or (mobile and not mobile_code):
            raise serializers.ValidationError("Both email and mobile OTP codes must be provided.")
        if (email_code and not email) or (mobile_code and not mobile):
            raise serializers.ValidationError("Both email and mobile must be provided when OTP codes are given.")
        return attrs

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    email_code = serializers.CharField(max_length=4)          # Email OTP
    mobile_code = serializers.CharField(max_length=4)         # Mobile OTP
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

class ProfileSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'mobile', 'user_type', 'country')

# Custom TokenObtainPairSerializer to include user data
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom data
        data.update({
            'user': {
                'email': self.user.email,
                'mobile': self.user.mobile,
                'user_type': self.user.user_type,
            }
        })

        return data

# Serializers for Additional Models

class Model1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Model1
        fields = '__all__'

class Model2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Model2
        fields = '__all__'

class Model3Serializer(serializers.ModelSerializer):
    class Meta:
        model = Model3
        fields = '__all__'
