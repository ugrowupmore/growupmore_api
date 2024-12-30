# authuser/permissions.py

from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class IsEmployeeUser(permissions.BasePermission):
    """
    Allows access only to employee users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object or admin to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Admin has access
        if request.user.is_superuser:
            return True
        # Otherwise, only the owner has access
        return obj == request.user
