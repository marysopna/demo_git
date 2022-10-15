from django.conf import settings

from rest_framework import authentication
from rest_framework import exceptions


class AuthenticationApi(authentication.BaseAuthentication):
    def authenticate(self, request, *args, **kwargs):
        token = request.query_params.get("key", False)

        if token and "HTTP_AUTHORIZATION" not in request.META:
            return None
        else:
            return super().authenticate(request)
