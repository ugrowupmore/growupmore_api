# utils/views.py

from rest_framework import viewsets
from .models import OTP
from .serializers import OTPCustomSerializer
from rest_framework.permissions import IsAdminUser

class OTPViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OTP.objects.all()
    serializer_class = OTPCustomSerializer
    permission_classes = [IsAdminUser]
