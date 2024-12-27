# authapp/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from datetime import timedelta

USER_TYPE_CHOICES = (
    ('student', 'Student'),
    ('instructor', 'Instructor'),
    ('institute', 'Institute'),
    ('admin', 'Admin'),  # Added 'admin' for superusers
)

LOCKOUT_THRESHOLD = 5  # Number of allowed failed attempts
LOCKOUT_DURATION = timedelta(hours=24)  # Duration of account lockout

class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)  # Country code, e.g., +91

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    def create_user(self, email=None, mobile=None, password=None, user_type='student', country=None, **extra_fields):
        if not email and not mobile:
            raise ValueError('Users must have either an email or mobile number')
        email = self.normalize_email(email)
        user = self.model(email=email, mobile=mobile, user_type=user_type, country=country, **extra_fields)
        user.set_password(password)
        user.is_active = False  # User inactive until OTP verification
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email=email, password=password, is_superuser=True, is_staff=True, user_type='admin', country=None, **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True, blank=True)
    mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)  # Stored without country code
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    is_staff = models.BooleanField(default=False)  # Employee if True
    is_active = models.BooleanField(default=False)  # Active after OTP
    is_superuser = models.BooleanField(default=False)  # Admin if True
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, null=True, blank=True)
    is_locked = models.BooleanField(default=False)
    lockout_until = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile']

    objects = UserManager()

    def __str__(self):
        return self.email if self.email else self.mobile

class FailedLoginAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='failed_attempts')
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Failed login for {self.user} from {self.ip_address} at {self.timestamp}"

class OTP(models.Model):
    OTP_TYPE_CHOICES = (
        ('email', 'Email'),
        ('mobile', 'Mobile'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    code = models.CharField(max_length=6)
    type = models.CharField(max_length=10, choices=OTP_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email or self.user.mobile} - {self.code} ({self.type})"

# Additional Models for Permissions

class Model1(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Model2(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title

class Model3(models.Model):
    info = models.CharField(max_length=255)

    def __str__(self):
        return self.info
