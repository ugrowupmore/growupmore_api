# authuser/authentication/unified_jwt_authentication.py

import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from authuser.models import (
    Student, Employee, Instructor, Institute,
    StudentBlacklistedToken, EmployeeBlacklistedToken,
    InstructorBlacklistedToken, InstituteBlacklistedToken
)
from utils.authentication_wrappers import GenericUserWrapper

USER_MODELS = {
    'student': (Student, StudentBlacklistedToken),
    'employee': (Employee, EmployeeBlacklistedToken),
    'instructor': (Instructor, InstructorBlacklistedToken),
    'institute': (Institute, InstituteBlacklistedToken),
}

class UnifiedJWTAuthentication(authentication.BaseAuthentication):
    """
    Unified JWT Authentication class to handle multiple user types.
    """

    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header or auth_header[0].lower() != b'bearer':
            return None  # No authentication attempted

        if len(auth_header) == 1:
            raise exceptions.AuthenticationFailed('Invalid token header. No credentials provided.')
        elif len(auth_header) > 2:
            raise exceptions.AuthenticationFailed('Invalid token header. Token string should not contain spaces.')

        try:
            token = auth_header[1].decode()
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            jti = payload.get('jti')
            if not jti:
                raise exceptions.AuthenticationFailed('Invalid token: Missing jti.')

            user_id = payload.get('user_id')
            user_type = payload.get('user_type')
            if user_type not in USER_MODELS:
                raise exceptions.AuthenticationFailed('Invalid user type.')

            user_model, blacklisted_token_model = USER_MODELS[user_type]
            user = user_model.objects.get(id=user_id)

            # Check if the jti is blacklisted
            if blacklisted_token_model.objects.filter(jti=jti).exists():
                raise exceptions.AuthenticationFailed('Token has been blacklisted. Please login again.')

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired.')
        except (jwt.InvalidTokenError, user_model.DoesNotExist):
            raise exceptions.AuthenticationFailed('Invalid token.')

        # Use GenericUserWrapper
        return (GenericUserWrapper(user), token)
