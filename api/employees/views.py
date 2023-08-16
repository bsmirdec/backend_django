from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .services import employee_create, employee_delete, employee_update
from .selectors import employee_get, employee_list, get_staff_for_manager
from ..permissions.CRUDpermissions import CustomPermissionMixin
from .serializers import EmployeeInputSerializer, EmployeeOutputSerializer


class EmployeeViewListAPI(CustomPermissionMixin, APIView):
    def get(self, request):
        if self.has_permission(request, self):
            employees = employee_list()
            serializer = EmployeeOutputSerializer(employees, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class SiteDirectorsViewListAPI(CustomPermissionMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employees = employee_list().filter(position="site_director")
        serializer = EmployeeOutputSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployeeRetrieveObjectAPI(CustomPermissionMixin, APIView):
    def get(self, request, pk):
        if self.has_permission(request, self):
            employee = employee_get(pk)
            serializer = EmployeeOutputSerializer(employee)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class EmployeeCreateObjectAPI(CustomPermissionMixin, APIView):
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
    def put(self, request, pk):
        if self.has_permission(request, self):
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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        employees = get_staff_for_manager(user)
        serializer = EmployeeOutputSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
