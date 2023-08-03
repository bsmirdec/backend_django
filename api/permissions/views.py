from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .PERMISSIONS import PERMISSIONS


class PermissionsViewListAPI(APIView):
    def get(self, request, *args, **kwargs):
        return Response(PERMISSIONS, status=status.HTTP_200_OK)
