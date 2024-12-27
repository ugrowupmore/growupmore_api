# authapp/throttling.py

from rest_framework.throttling import SimpleRateThrottle

class LoginRateThrottle(SimpleRateThrottle):
    scope = 'login'

    def get_cache_key(self, request, view):
        # Throttle based on IP address
        return self.get_ident(request)

class OTPRateThrottle(SimpleRateThrottle):
    scope = 'otp'

    def get_cache_key(self, request, view):
        # Throttle based on IP address
        return self.get_ident(request)
