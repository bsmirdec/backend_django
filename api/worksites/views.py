from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException

from .services import worksite_create, worksite_update, worksite_delete
from .selectors import worksite_list, worksite_get
from ..permissions.CRUDpermissions import CustomPermissionMixin
from .serializers import WorksiteInputSerializer, WorksiteOutputSerializer
from .models import Worksite


class WorksiteAlreadyExists(APIException):
    status_code = 400
    default_detail = "Un chantier avec ce nom et cette ville existe déjà."
    default_code = "worksite_already_exists"


class WorksiteViewListAPI(CustomPermissionMixin, APIView):
    def get(self, request):
        if self.has_permission(request, self):
            worksites = worksite_list()
            serializer = WorksiteOutputSerializer(worksites, many=True)
            return Response(serializer.data)
        else:
            return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class WorksiteRetrieveObjectAPI(CustomPermissionMixin, APIView):
    def get(self, request, pk):
        if self.has_permission(request, self):
            worksite = worksite_get(pk)
            serializer = WorksiteOutputSerializer(worksite)
            return Response(serializer.data)
        else:
            return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class WorksiteCreateObjectAPI(CustomPermissionMixin, APIView):
    def post(self, request):
        if self.has_permission(request, self):
            serializer = WorksiteInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            existing_worksite = Worksite.objects.filter(name=serializer.validated_data["name"], city=serializer.validated_data["city"]).first()
            if existing_worksite:
                raise WorksiteAlreadyExists()

            worksite = worksite_create(serializer.data)

            response_data = {
                "worksite_id": worksite.worksite_id,
                "sector": worksite.sector,
                "name": worksite.name,
                "address": worksite.address,
                "postal_code": worksite.postal_code,
                "city": worksite.city,
                "started": worksite.started,
                "status": worksite.status,
            }
            return Response(response_data, status=201)
        else:
            return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class WorksiteUpdateObjectAPI(CustomPermissionMixin, APIView):
    def put(self, request, pk):
        if self.has_permission(request, self):
            worksite = worksite_get(pk)
            serializer = WorksiteInputSerializer(worksite, data=request.data)
            serializer.is_valid(raise_exception=True)
            worksite = worksite_update(worksite, serializer.validated_data)
            response_data = WorksiteOutputSerializer(worksite).data
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class WorksiteDeleteObjectAPI(CustomPermissionMixin, APIView):
    def delete(self, request, pk):
        if self.has_permission(request, self):
            worksite = worksite_get(pk=pk)
            worksite_delete(worksite)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class WorksiteOptionsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            sectors = Worksite.sector_options
            status_options = Worksite.status_options
            response_data = {
                "sectors": sectors,
                "status_options": status_options,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "An error occurred while fetching options."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
