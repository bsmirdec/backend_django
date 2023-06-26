from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Worksite, Client, Management, WorkingPosition
from .serializers import WorksiteSerializer, ClientSerializer, ManagementSerializer
from .permissions import IsAdministrator, IsSiteDirector, IsSiteSupervisor


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsAdministrator | IsAdminUser]


class WorksiteViewSet(viewsets.ModelViewSet):
    queryset = Worksite.objects.all()
    serializer_class = WorksiteSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            permission_classes = [IsAuthenticated | IsAdminUser]
        elif self.action == "update":
            permission_classes = [IsAuthenticated, IsSiteDirector | IsAdministrator | IsSiteSupervisor | IsAdminUser]
        elif self.action == "destroy":
            permission_classes = [IsAuthenticated, IsAdministrator, IsAdminUser]
        elif self.action == "create":
            permission_classes = [IsAuthenticated, IsSiteDirector | IsAdministrator | IsAdminUser]
        else:
            permission_classes = [IsAuthenticated | IsAdminUser]
        return [permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response("Le chantier a été supprimé avec succès.", status=status.HTTP_204_NO_CONTENT)


class ManagementViewSet(viewsets.ModelViewSet):
    queryset = Management.objects.all()
    serializer_class = ManagementSerializer
    permission_classes = [IsAuthenticated, IsSiteDirector | IsAdministrator | IsAdminUser]

    def create_staff(self, request, *args, **kwargs):
        management_id = kwargs.get("pk")
        management = self.get_object()
        staff_id = request.data.get("staff_id")

        if staff_id is None:
            return Response("Le paramètre staff_id est manquant", status=status.HTTP_400_BAD_REQUEST)

        staff_model = management.get_staff_model()
        try:
            staff = staff_model.objects.get(id=staff_id)
        except staff_model.DoesNotExist:
            return Response("Le staff spécifié n'existe pas", status=status.HTTP_404_NOT_FOUND)

        if management.staff is not None:
            return Response("Un staff est déjà affecté à ce chantier", status=status.HTTP_400_BAD_REQUEST)

        management.staff = staff
        management.save()

        serializer = self.get_serializer(management)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update_staff(self, request, *args, **kwargs):
        management_id = kwargs.get("pk")
        management = self.get_object()
        staff_id = request.data.get("staff_id")

        if staff_id is None:
            return Response("Le paramètre staff_id est manquant", status=status.HTTP_400_BAD_REQUEST)

        staff_model = management.get_staff_model()
        try:
            staff = staff_model.objects.get(id=staff_id)
        except staff_model.DoesNotExist:
            return Response("Le staff spécifié n'existe pas", status=status.HTTP_404_NOT_FOUND)

        if management.staff != staff:
            return Response("Le staff spécifié ne correspond pas à celui affecté à ce chantier", status=status.HTTP_400_BAD_REQUEST)

        management.save()

        serializer = self.get_serializer(management)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete_staff(self, request, *args, **kwargs):
        management_id = kwargs.get("pk")
        management = self.get_object()

        if management.staff is None:
            return Response("Aucun staff n'est affecté à ce chantier", status=status.HTTP_400_BAD_REQUEST)

        management.staff = None
        management.save()

        serializer = self.get_serializer(management)
        return Response(serializer.data, status=status.HTTP_200_OK)
