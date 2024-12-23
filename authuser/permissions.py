# authuser/permissions.py

from rest_framework.permissions import BasePermission

class IsSuperUser(BasePermission):
    """
    Allows access only to superusers.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)

class IsStudent(BasePermission):
    """
    Allows access only to student users.
    """
    def has_permission(self, request, view):
        user = request.user
        return hasattr(user, 'user_type') and user.user_type == 'student'


class IsEmployee(BasePermission):
    """
    Allows access only to employee users.
    """
    def has_permission(self, request, view):
        user = request.user
        return hasattr(user, 'user_type') and user.user_type == 'employee'


class IsInstructor(BasePermission):
    """
    Allows access only to instructor users.
    """
    def has_permission(self, request, view):
        user = request.user
        return hasattr(user, 'user_type') and user.user_type == 'instructor'


class IsInstitute(BasePermission):
    """
    Allows access only to institute users.
    """
    def has_permission(self, request, view):
        user = request.user
        return hasattr(user, 'user_type') and user.user_type == 'institute'
