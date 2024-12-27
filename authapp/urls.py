# authapp/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationView, ResendOTPView, VerifyOTPView, 
    ActivateAccountView, ForgotPasswordView, ResetPasswordView,
    ChangePasswordView, ProfileView, CountryViewSet, Model1ViewSet, 
    Model2ViewSet, Model3ViewSet, CustomTokenObtainPairView, CustomTokenRefreshView,
    LogoutView
)

router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'model1', Model1ViewSet, basename='model1')
router.register(r'model2', Model2ViewSet, basename='model2')
router.register(r'model3', Model3ViewSet, basename='model3')

urlpatterns = [
    # Authentication endpoints
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('activate-account/', ActivateAccountView.as_view(), name='activate-account'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    
    # Logout endpoint
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # JWT Token endpoints
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login endpoint
    path('login/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    
    # Profile endpoint
    path('profile/', ProfileView.as_view(), name='profile'),
    
    # Other model endpoints
    path('', include(router.urls)),
]
