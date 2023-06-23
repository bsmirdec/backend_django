from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, filters
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS, IsAdminUser, IsAuthenticated, BasePermission, DjangoModelPermissionsOrAnonReadOnly
from .models import Worksite, Client
from .serializers import WorksiteSerializer, ClientSerializer


# class WorksiteUserCreatePermission(BasePermission):
#     message = "Creating and editing is restricted to the boss"

#     def has_object_permission(self, request, view, obj):
#         if request.method in SAFE_METHODS:
#             return True


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == "retrieve" and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ClientList(viewsets.ViewSet):
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request):
        serializer_class = ClientSerializer(self.queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        client = get_object_or_404(self.queryset, pk=pk)
        serializer_class = ClientSerializer(client)
        return Response(serializer_class.data)


class WorksiteList(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WorksiteSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get("pk")
        return get_object_or_404(Worksite, worksite_id=item)

    def get_queryset(self):
        return Worksite.objects.all()
