# utils/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OTPViewSet

router = DefaultRouter()
router.register(r'otps', OTPViewSet, basename='otp')

urlpatterns = [
    path('', include(router.urls)),
]
