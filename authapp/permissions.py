# authapp/permissions.py

from rest_framework import permissions
from permissions_config import permissions_mapping

class RoleBasedPermission(permissions.BasePermission):
    """
    Generic permission class that checks permissions based on a permissions mapping.
    """

    def has_permission(self, request, view):
        # Determine the model name
        if hasattr(view, 'get_queryset'):
            try:
                model = view.get_queryset().model.__name__
            except AttributeError:
                return False
        else:
            return False

        # Determine the action
        action = getattr(view, 'action', None)
        if not action:
            return False

        # Map view action to method
        action_map = {
            'list': 'read',
            'retrieve': 'read',
            'create': 'create',
            'update': 'update',
            'partial_update': 'update',
            'destroy': 'delete',
        }

        method = action_map.get(action, None)
        if not method:
            return False  # Unsupported action

        # Get the permissions for this model
        model_permissions = permissions_mapping.get(model, {})

        # Determine the user's role
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.user_type == 'admin':
                role = 'admin'
            elif request.user.is_staff:
                role = 'employee'
            else:
                role = request.user.user_type  # e.g., 'student', 'instructor', etc.
        else:
            role = 'anonymous'

        # Get allowed actions for the role
        allowed_actions = model_permissions.get(role, [])

        # Check if the action is allowed
        if method in allowed_actions:
            return True
        else:
            return False
