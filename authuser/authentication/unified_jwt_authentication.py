# authuser/authentication/unified_jwt_authentication.py

import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from authuser.models import (
    Student, Employee, Instructor, Institute,
    StudentBlacklistedToken, EmployeeBlacklistedToken,
    InstructorBlacklistedToken, InstituteBlacklistedToken
)
from django.contrib.auth import get_user_model
from utils.authentication_wrappers import GenericUserWrapper  # Import the wrapper

User = get_user_model()

USER_MODELS = {
    'student': (Student, StudentBlacklistedToken),
    'employee': (Employee, EmployeeBlacklistedToken),
    'instructor': (Instructor, InstructorBlacklistedToken),
    'institute': (Institute, InstituteBlacklistedToken),
}

class UnifiedJWTAuthentication(authentication.BaseAuthentication):
    """
    Custom JWT Authentication supporting multiple user types, including superusers.
    """

    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header or auth_header[0].lower() != b'bearer':
            return None

        if len(auth_header) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth_header) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth_header[1].decode()
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            user_type = payload.get('user_type')

            if user_type in USER_MODELS:
                user_model, _ = USER_MODELS[user_type]
                user = user_model.objects.get(id=user_id)
            elif user_type == 'superuser':
                user = User.objects.get(id=user_id)
            else:
                raise exceptions.AuthenticationFailed('Invalid user type.')

            if not user.is_active:
                raise exceptions.AuthenticationFailed('User account is inactive.')

            wrapped_user = GenericUserWrapper(user)  # Wrap the user
            return (wrapped_user, token)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired.')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token.')
        except (Employee.DoesNotExist, Institute.DoesNotExist, Instructor.DoesNotExist, Student.DoesNotExist, User.DoesNotExist):
            raise exceptions.AuthenticationFailed('User not found.')
