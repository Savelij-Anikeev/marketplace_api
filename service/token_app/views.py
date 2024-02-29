from djoser.views import TokenCreateView, TokenDestroyView
from django.conf import settings
from rest_framework.request import Request

from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from datetime import timedelta


class TokenCustomCreateView(TokenCreateView):
    def _action(self, serializer):
        response = Response()
        refresh = RefreshToken.for_user(serializer.user)
        response.delete_cookie("access_token")
        response.set_cookie(
            key = "refresh",
            value = refresh,
            max_age = timedelta(days=30),
            secure = not settings.DEBUG,
            httponly = True,
            samesite = "Strict"
        )
        response.data = {"access": str(refresh.access_token)}
        response.status_code = status.HTTP_200_OK
        return response


class TokenCustomDestroyView(TokenDestroyView):
    pass


class TokenCustomRefreshView(TokenRefreshView):
    pass
