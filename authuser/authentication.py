# authuser/authentication.py

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class that retrieves the JWT token from cookies.
    """

    def authenticate(self, request):
        # Retrieve the access token from the 'access' cookie
        access_token = request.COOKIES.get('access')  # Ensure this matches your cookie name

        if not access_token:
            return None  # No token found, proceed to other authentication methods

        # Create a temporary Authorization header to leverage JWTAuthentication's existing logic
        # Format: 'Bearer <token>'
        header = f'Bearer {access_token}'
        request.META['HTTP_AUTHORIZATION'] = header

        # Call the parent class's authenticate method
        return super().authenticate(request)
