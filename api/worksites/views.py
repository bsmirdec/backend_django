from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .services import worksite_create, worksite_update, worksite_delete
from .selectors import worksite_list, worksite_get
from ..permissions.CRUDpermissions import CustomPermissionMixin
from .serializers import WorksiteInputSerializer, WorksiteOutputSerializer


class WorksiteViewListAPI(CustomPermissionMixin, APIView):
    def get(self, request):
        worksites = worksite_list()
        serializer = WorksiteOutputSerializer(worksites, many=True)
        if self.has_permission(self, request):
            return Response(serializer.data)
        else:
            return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class WorksiteRetrieveObjectAPI(CustomPermissionMixin, APIView):
    def get(self, request, pk):
        if self.has_permission(self, request):
            worksite = worksite_get(pk)
            serializer = WorksiteOutputSerializer(worksite)
            return Response(serializer.data)
        else:
            return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class WorksiteCreateObjectAPI(CustomPermissionMixin, APIView):
    def post(self, request):
        if self.has_permission(self, request):
            serializer = WorksiteInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            worksite = worksite_create(serializer.data)

            response_data = {
                "worksite_id": worksite.worksite_id,
                "sector": worksite.sector,
                "name": worksite.name,
                "adress": worksite.adress,
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
        if self.has_permission(self, request):
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
        if self.has_permission(self, request):
            worksite = worksite_get(pk=pk)
            worksite_delete(worksite)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)
