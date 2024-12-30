# utils/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='utils_otp_set')  # Unique related_name
    email_otp = models.CharField(max_length=6, blank=True, null=True)
    mobile_otp = models.CharField(max_length=6, blank=True, null=True)
    new_email = models.EmailField(blank=True, null=True)             # New field for email update
    new_email_otp = models.CharField(max_length=6, blank=True, null=True)  # OTP for new email
    new_mobile = models.CharField(max_length=15, blank=True, null=True)     # New field for mobile update
    new_mobile_otp = models.CharField(max_length=6, blank=True, null=True)  # OTP for new mobile
    is_verified = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    expiry_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.user.email or self.user.mobile}"
