# authuser/urls.py

from django.urls import path
from .views import (
    UserRegistrationView,
    ResendEmailOTPView,    
    ResendMobileOTPView,   
    UserVerificationView,
    UserProfileView,
    LoginView,
    LogoutView,
    UpdateEmailView,       
    UpdateEmailVerifyView,
    UpdateMobileView,
    UpdateMobileVerifyView,
    ChangePasswordView,
    ForgotPasswordView,  
    ResetNewPasswordView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),    
    path('resend-email-otp/', ResendEmailOTPView.as_view(), name='resend-email-otp'),  # New endpoint
    path('resend-mobile-otp/', ResendMobileOTPView.as_view(), name='resend-mobile-otp'),  # New endpoint
    path('verify/', UserVerificationView.as_view(), name='verify'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('update_email/', UpdateEmailView.as_view(), name='update-email'),
    path('update_email_verify/', UpdateEmailVerifyView.as_view(), name='update-email-verify'),
    path('update_mobile/', UpdateMobileView.as_view(), name='update-mobile'),
    path('update_mobile_verify/', UpdateMobileVerifyView.as_view(), name='update-mobile-verify'),
    path('changes_password/', ChangePasswordView.as_view(), name='change-password'),
    path('forget_password/', ForgotPasswordView.as_view(), name='reset-password'),
    path('reset_new_password/', ResetNewPasswordView.as_view(), name='reset-new-password'),
]
