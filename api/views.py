from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, filters
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS, IsAdminUser, AllowAny, IsAuthenticated, BasePermission, DjangoModelPermissionsOrAnonReadOnly
from .models import Worksite, Client
from .serializers import WorksiteSerializer, ClientSerializer


# class WorksiteUserCreatePermission(BasePermission):
#     message = "Creating and editing is restricted to the boss"

#     def has_object_permission(self, request, view, obj):
#         if request.method in SAFE_METHODS:
#             return True


class ClientList(viewsets.ViewSet):
    queryset = Client.objects.all()
    permission_classes = [AllowAny]

    def list(self, request):
        serializer_class = ClientSerializer(self.queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        client = get_object_or_404(self.queryset, pk=pk)
        serializer_class = ClientSerializer(client)
        return Response(serializer_class.data)


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    pass


class WorksiteList(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WorksiteSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get("pk")
        return get_object_or_404(Worksite, worksite_id=item)

    def get_queryset(self):
        return Worksite.objects.all()


# class WorksiteList(generics.ListAPIView):
#     queryset = Worksite.objects.all()
#     serializer_class = WorksiteSerializer
#     permission_classes = [IsAuthenticated]


# class WorksiteListCreate(generics.ListCreateAPIView):
#     queryset = Worksite.objects.all()
#     serializer_class = WorksiteSerializer
#     permission_classes = [IsAdminUser]


# class WorksiteDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Worksite.objects.all()
#     serializer_class = WorksiteSerializer
#     permission_classes = [IsAdminUser]
