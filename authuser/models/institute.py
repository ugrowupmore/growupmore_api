from django.utils.timezone import now 
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

from utils.enums import StatusType


class Institute(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=False)    
    is_kyc_approved = models.BooleanField(default=False)
    is_mobile_approved = models.BooleanField(default=False)    
    is_active = models.BooleanField(default=False)        
    is_mobile_approved = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(null=True)    
    status = models.CharField(max_length=10, choices=StatusType.choices, default=StatusType.DRAFT)
    failed_login_attempts = models.IntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = '"authuser"."institutes"'
        indexes = [
            models.Index(fields=['name']),            
            models.Index(fields=['email', 'mobile', 'password']),                        
            models.Index(fields=['is_active','is_kyc_approved']),
        ]

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return f"{self.id} - {self.name}"
    
class InstituteBlacklistedToken(models.Model):
    """
    Model to store blacklisted JWT tokens.
    """
    jti = models.CharField(max_length=36, unique=True)  # UUID4 has 36 characters
    blacklisted_at = models.DateTimeField(default=now)  # Use Django's timezone-aware now

    class Meta:
        db_table = '"authuser"."InstituteBlacklistedTokens"'

    def __str__(self):
        return f"InstituteBlacklistedToken(jti={self.jti}, blacklisted_at={self.blacklisted_at})"