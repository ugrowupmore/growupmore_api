# authuser/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from utils.models import OTP

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'mobile', 'user_type', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'mobile')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'mobile', 'password')}),
        ('Personal Info', {'fields': ('user_type', 'country')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'mobile', 'password1', 'password2'),
        }),
    )

admin.site.register(User, UserAdmin)
