from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from .models import Employee

from .services import employee_create, employee_delete, employee_update
from .selectors import employee_get, employee_list, get_staff_for_manager
from ..permissions.CRUDpermissions import CustomPermissionMixin
from .serializers import EmployeeInputSerializer, EmployeeOutputSerializer


class EmployeeViewListAPI(CustomPermissionMixin, APIView):
    class EmployeeOutputSerializer(serializers.Serializer):
        employee_id = serializers.IntegerField()
        first_name = serializers.CharField()
        last_name = serializers.CharField()
        position = serializers.ChoiceField(choices=Employee.positions_options)
        manager = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
        permissions = serializers.DictField()

    def get(self, request, user):
        if self.has_permission(self, request, user):
            employees = employee_list(user)
            serializer = self.EmployeeOutputSerializer(employees, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class EmployeeRetrieveObjectAPI(CustomPermissionMixin, APIView):
    class EmployeeOutputSerializer(serializers.Serializer):
        employee_id = serializers.IntegerField()
        first_name = serializers.CharField()
        last_name = serializers.CharField()
        position = serializers.ChoiceField(choices=Employee.positions_options)
        manager = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
        permissions = serializers.DictField()

    def get(self, request, pk, user):
        if self.has_permission(self, request, pk, user):
            employee = employee_get(pk)
            serializer = self.EmployeeOutputSerializer(employee)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class EmployeeCreateObjectAPI(CustomPermissionMixin, APIView):
    class EmployeeInputSerializer(serializers.Serializer):
        first_name = serializers.CharField()
        last_name = serializers.CharField()
        position = serializers.ChoiceField(choices=Employee.positions_options)
        manager = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
        permissions = serializers.DictField()

    def post(self, request):
        if self.has_permission(self, request):
            serializer = EmployeeInputSerializer(data=request.data)
            if serializer.is_valid():
                employee = employee_create(validated_data=serializer.validated_data)
                response_data = EmployeeOutputSerializer(employee).data
                return Response(response_data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class EmployeeUpdateObjectAPI(CustomPermissionMixin, APIView):
    class EmployeeOutputSerializer(serializers.Serializer):
        employee_id = serializers.IntegerField()
        first_name = serializers.CharField()
        last_name = serializers.CharField()
        position = serializers.ChoiceField(choices=Employee.positions_options)
        manager = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
        permissions = serializers.DictField()

    def put(self, request, pk):
        if self.has_permission(self, request):
            serializer = EmployeeInputSerializer(data=request.data)
            if serializer.is_valid():
                employee = employee_update(pk=pk, validated_data=serializer.validated_data)
                response_data = EmployeeOutputSerializer(employee).data
                return Response(response_data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class EmployeeDeleteObjectAPI(CustomPermissionMixin, APIView):
    def delete(self, request, pk):
        if self.has_permission(self, request):
            employee = employee_get(pk=pk)
            employee_delete(employee)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class GetStaffAPI(EmployeeViewListAPI):
    def get(self, request):
        user = request.user  # Obtenez l'utilisateur en cours à partir de la requête
        employees = get_staff_for_manager(user)
        serializer = self.EmployeeOutputSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
