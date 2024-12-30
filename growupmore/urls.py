# growupmore/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/master/', include('master.urls')),
    path('api/authuser/', include('authuser.urls')),
    path('api/utils/', include('utils.urls')),
]
