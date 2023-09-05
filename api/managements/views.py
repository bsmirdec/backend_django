from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException

from .services import management_create, management_delete
from .selectors import management_list, management_get, get_employee_for_worksite, get_worksite_for_employee, get_validators
from ..permissions.CRUDpermissions import CustomPermissionMixin
from .serializers import ManagementSerializer
from ..worksites.models import Worksite
from ..worksites.serializers import WorksiteOutputSerializer
from ..employees.models import Employee
from ..employees.serializers import EmployeeOutputSerializer


class ManagementAlreadyExists(APIException):
    status_code = 400
    default_detail = "Un chantier avec ce nom et cette ville existe déjà."
    default_code = "worksite_already_exists"


class ManagementViewListAPI(CustomPermissionMixin, APIView):
    def get(self, request):
        if self.has_permission(self, request):
            managements = management_list()
            serializer = ManagementSerializer(managements, many=True)
            return Response(serializer.data)
        else:
            return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class ManagementRetrieveObjectAPI(CustomPermissionMixin, APIView):
    def get(self, request, worksite, employee):
        if self.has_permission(self, request):
            management = management_get(worksite, employee)
            serializer = ManagementSerializer(management)
            return Response(serializer.data)
        else:
            return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class ManagementCreateObjectAPI(CustomPermissionMixin, APIView):
    def post(self, request):
        if self.has_permission(request, self):
            serializer = ManagementSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            management = management_create(serializer.validated_data["worksite_id"], serializer.validated_data["employee_id"])

            if management is not None:
                response_data = ManagementSerializer(management).data
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response("Chantier ou employé introuvable.", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class ManagementDeleteObjectAPI(CustomPermissionMixin, APIView):
    def delete(self, request, worksite_id, employee_id):
        if self.has_permission(request, self):
            management_delete(worksite_id=worksite_id, employee_id=employee_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class GetWorksiteForEmployeeAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, employee_id):
        try:
            worksites = get_worksite_for_employee(employee_id=employee_id)
            serialized_worksites = WorksiteOutputSerializer(worksites, many=True).data
            return Response(serialized_worksites, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)


class GetEmployeeForWorksiteAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, worksite_id):
        try:
            employees = get_employee_for_worksite(worksite_id=worksite_id)
            serialized_employees = EmployeeOutputSerializer(employees, many=True).data
            return Response(serialized_employees, status=status.HTTP_200_OK)
        except Worksite.DoesNotExist:
            return Response({"error": "Worksite not found"}, status=status.HTTP_404_NOT_FOUND)


class GetValidatorForWorksiteAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, worksite_id):
        try:
            employees = get_validators(worksite_id=worksite_id)
            serialized_employees = EmployeeOutputSerializer(employees, many=True).data
            return Response(serialized_employees, status=status.HTTP_200_OK)
        except Worksite.DoesNotExist:
            return Response({"error": "Worksite not found"}, status=status.HTTP_404_NOT_FOUND)
