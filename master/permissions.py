# master/permissions.py

from rest_framework import permissions

class CustomModelPermission(permissions.BasePermission):
    """
    Custom permission class for Country, State, City models.
    - Admin: Full access
    - Employee: Read and Create
    - Anonymous: Read-only
    """

    def has_permission(self, request, view):
        # Allow read-only for any user
        if request.method in permissions.SAFE_METHODS:
            return True

        # If user is authenticated
        if request.user and request.user.is_authenticated:
            if request.user.is_superuser:
                return True  # Admin has full access
            elif request.user.is_staff:
                # Employee can read and create
                if request.method in ['POST']:
                    return True
                else:
                    return False
            else:
                # Other users have no access
                return False
        else:
            # Unauthenticated users cannot perform non-safe methods
            return False
