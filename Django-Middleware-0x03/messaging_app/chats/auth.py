from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        # Optionally customize token retrieval or validation
        user_auth_tuple = super().authenticate(request)
        if user_auth_tuple is None:
            raise AuthenticationFailed('Invalid or missing token')
        return user_auth_tuple
