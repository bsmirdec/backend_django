from django.db import IntegrityError

from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser, BasePermission, SAFE_METHODS


from .models import CustomUser
from .services import user_create, user_update, user_delete, user_link_to_employee
from .selectors import user_get, user_list, user_get_employee, user_get_permissions, user_get_staff
from .serializers import UserInputSerializer, UserOutputSerializer
from api.employees.serializers import EmployeeOutputSerializer
from ..tokens.permissions import IsJWTAuthenticated


class UpdateOwnAccount(BasePermission):
    def has_object_permission(self, request, view, obj):
        """check user is trying to edit their own account"""
        if request.method in SAFE_METHODS:
            return True
        return obj.id == request.user.user_id


class UserCreateObjectAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = user_create(serializer.validated_data)
            response_data = {
                "user_id": user.user_id,
                "email": user.email,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            response_data = {"message": "Cet e-mail est déjà utilisé par un autre utilisateur."}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class UserMatchEmployeeAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_id = request.data.get("user_id", None)
        first_name = request.data.get("first_name", None)
        last_name = request.data.get("last_name", None)

        if not first_name or not last_name:
            return Response({"error": "Le nom et le prénom sont requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(user_id=user_id)
            result = user_link_to_employee(user_id=user_id, first_name=first_name, last_name=last_name)

            if result is not None:
                # send_confirmation_email(user=user, email=EMAIL_ADMIN)
                response_data = UserOutputSerializer(user).data
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Aucune correspondance trouvée avec un employé."}, status=status.HTTP_404_NOT_FOUND)
        except CustomUser.DoesNotExist:
            return Response({"message": "L'utilisateur avec l'ID fourni n'existe pas."}, status=status.HTTP_404_NOT_FOUND)


class UserConfirmAccountAPI(APIView):
    pass


class UserGetPermissions(APIView):
    permission_classes = [IsJWTAuthenticated]

    class PermissionsSerializer(serializers.JSONField):
        def to_representation(self, value):
            # Convertir le JSON en dictionnaire Python
            permissions_dict = super().to_representation(value)
            return permissions_dict

        def to_internal_value(self, data):
            # Convertir le dictionnaire Python en JSON
            return super().to_internal_value(data)

    def get(self, request, pk):
        try:
            permissions = user_get_permissions(pk=pk)
            response_data = self.PermissionsSerializer(permissions)
            return Response(response_data)
        except CustomUser.DoesNotExist:
            return Response({"message": "L'utilisateur avec l'ID fourni n'existe pas."}, status=status.HTTP_404_NOT_FOUND)


class UserGetEmployee(APIView):
    permission_classes = [IsJWTAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        try:
            employee = user_get_employee(pk=pk)
            if employee is not None:
                serializer = EmployeeOutputSerializer(employee)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "La création du compte n'a pas été validée par un administrateur."}, status=status.HTTP_404_NOT_FOUND)
        except CustomUser.DoesNotExist:
            return Response({"message": "L'utilisateur avec l'ID fourni n'existe pas."}, status=status.HTTP_404_NOT_FOUND)


class UserGetStaff(APIView):
    permission_classes = [IsJWTAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        try:
            staff = user_get_staff(pk=pk)
            if staff is not None:
                serializer = EmployeeOutputSerializer(staff, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "L'utilisateur n'est pas manager"}, status=status.HTTP_404_NOT_FOUND)
        except CustomUser.DoesNotExist:
            return Response({"message": "L'utilisateur avec l'ID fourni n'existe pas."}, status=status.HTTP_404_NOT_FOUND)


class UserListAPI(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = user_list()

        serializer = UserOutputSerializer(users, many=True)

        return Response(serializer.data)


class UserRetrieveAPI(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        user = user_get(pk)
        serializer = UserOutputSerializer(user)
        return Response(serializer.data)


class UserUpdateAPI(APIView):
    permission_classes = [IsAdminUser]

    class UserUpdateSerializer(serializers.Serializer):
        is_active = serializers.BooleanField()
        is_staff = serializers.BooleanField()
        is_validated = serializers.BooleanField()

    def put(self, request, pk):
        user = user_get(pk)
        serializer = self.UserUpdateSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = user_update(user, serializer.validated_data)
        response_data = UserOutputSerializer(user).data
        return Response(response_data)


class UserDeleteAPI(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        user = user_get(pk=pk)
        user_delete(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
