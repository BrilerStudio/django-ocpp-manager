from django.middleware.csrf import get_token
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class PermissionsView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    ]

    def get(self, request, *args, **kwargs):
        return Response(self.request.user.permissions)


class CsrfView(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def get(self, request, *args, **kwargs):
        get_token(self.request)
        return Response({'success': True})
