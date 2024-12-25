# growupmore/urls.py

from django.contrib import admin
from django.urls import path, include
from authuser.views.schema_views import (
    ProtectedSpectacularAPIView, 
    ProtectedSpectacularSwaggerView, 
    ProtectedSpectacularRedocView  # Correct import
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/authuser/', include('authuser.urls')),  
    path('api/master/', include('master.urls')),  
    path('api/hr/', include('hr.urls')),  
    path('api/curriculum/', include('curriculum.urls')),  

    # Protected Schema and Swagger UI
    path('api/schema/', ProtectedSpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', ProtectedSpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', ProtectedSpectacularRedocView.as_view(url_name='schema'), name='redoc'),  # Use ProtectedSpectacularRedocView
]

