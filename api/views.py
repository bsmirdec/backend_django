from rest_framework import generics
from rest_framework.permissions import SAFE_METHODS, IsAdminUser, IsAuthenticated, BasePermission, DjangoModelPermissionsOrAnonReadOnly
from .models import Worksite, Client
from .serializers import WorksiteSerializer, ClientSerializer


# class WorksiteUserCreatePermission(BasePermission):
#     message = "Creating and editing is restricted to the boss"

#     def has_object_permission(self, request, view, obj):
#         if request.method in SAFE_METHODS:
#             return True


class ClientList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    pass


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    pass


class WorksiteList(generics.ListAPIView):
    queryset = Worksite.objects.all()
    serializer_class = WorksiteSerializer
    permission_classes = [IsAuthenticated]


class WorksiteListCreate(generics.ListCreateAPIView):
    queryset = Worksite.objects.all()
    serializer_class = WorksiteSerializer
    permission_classes = [IsAdminUser]


class WorksiteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Worksite.objects.all()
    serializer_class = WorksiteSerializer
    permission_classes = [IsAdminUser]
