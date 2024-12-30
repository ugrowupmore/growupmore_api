# authuser/models.py

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from master.models import Country, State, City  # Ensure State and City are imported
from django.utils import timezone

USER_TYPE_CHOICES = (
    ('student', 'Student'),
    ('instructor', 'Instructor'),
    ('institute', 'Institute'),
)

class UserManager(BaseUserManager):
    def create_user(self, email=None, mobile=None, password=None, user_type=None, country=None, **extra_fields):
        if not email and not mobile:
            raise ValueError('Users must have either an email or mobile number.')
        
        if email:
            email = self.normalize_email(email)
            user = self.model(email=email, mobile=mobile, user_type=user_type, country=country, **extra_fields)
        else:
            user = self.model(mobile=mobile, user_type=user_type, country=country, **extra_fields)
        
        user.set_password(password)
        # Initialize tracking fields
        user.failed_login_attempts = 0
        user.lock_until = None
        user.resend_otp_attempts = 0
        user.otp_resend_locked_until = None
        # Initialize new fields
        user.first_name = ''
        user.last_name = ''
        user.is_kyc_updated = False
        user.birth_date = None
        user.gender = 'Male'
        user.nationality = 'NA'
        user.address = 'NA'
        user.state = None
        user.city = None
        user.postal_code = '0'
        user.institute_name = 'NA'
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email=email, password=password, is_superuser=True, is_staff=True, user_type='admin', **extra_fields)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True, blank=True)
    mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)  # New Field
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)    # New Field
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)  # Activated after OTP verification
    date_joined = models.DateTimeField(auto_now_add=True)

    # New fields for login attempts
    failed_login_attempts = models.IntegerField(default=0)
    lock_until = models.DateTimeField(null=True, blank=True)

    # New fields for OTP resend attempts
    resend_otp_attempts = models.IntegerField(default=0)
    otp_resend_locked_until = models.DateTimeField(null=True, blank=True)

    # New fields added
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_kyc_updated = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)  # New Field
    gender = models.CharField(
        max_length=10,
        choices=(('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')),
        default='Male'
    )  # New Field
    nationality = models.CharField(max_length=50, default='NA')  # New Field
    address = models.TextField(default='NA')  # New Field
    postal_code = models.CharField(max_length=10, default='0')  # New Field
    institute_name = models.CharField(max_length=100, default='NA', null=True, blank=True)  # New Field

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile']

    objects = UserManager()

    def __str__(self):
        return self.email if self.email else self.mobile

    def is_locked(self):
        """
        Check if the user account is currently locked.
        """
        if self.lock_until and timezone.now() < self.lock_until:
            return True
        return False

    def can_resend_otp(self):
        """
        Check if the user can resend OTP.
        """
        if self.otp_resend_locked_until and timezone.now() < self.otp_resend_locked_until:
            return False
        if self.resend_otp_attempts >= settings.MAX_RESEND_OTP_ATTEMPTS:
            return False
        return True
