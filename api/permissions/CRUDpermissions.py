import re
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status

from authentication.tokens.authentication import MyCustomJWTAuthentication

from ..employees.models import Employee


def camel_case_to_snake_case(name):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


class CustomPermissionMixin(BasePermission):
    def get_user_from_token(self, request):
        jwt_authentication = MyCustomJWTAuthentication()
        user_and_token = jwt_authentication.authenticate(request)
        if user_and_token is not None:
            user, _ = user_and_token
            return user
        return None

    def get_employee(self, request):
        user = self.get_user_from_token(request)
        if user is not None:
            try:
                return Employee.objects.get(employee_id=user.employee.pk)
            except Employee.DoesNotExist:
                return None
        return None

    def has_permission(self, request, view):
        user = self.get_user_from_token(request)
        if user is None:
            return Response({"detail": "Votre jeton d'accès n'est plus valide."}, status=status.HTTP_401_UNAUTHORIZED)
        employee = self.get_employee(request)
        if not employee:
            return False
        permission_name = camel_case_to_snake_case(view.__class__.__name__)[:-4]
        return employee.has_permission(permission_name=permission_name)


def get_permissions_for_model(model_name):
    actions = ["create_object", "view_list", "retrieve_object", "update_object", "delete_object"]
    permissions = [f"{model_name}_{action}" for action in actions]
    return permissions


def add_permissions_to_dict(permissions_list, permissions_dict):
    for permission in permissions_list:
        permissions_dict[permission] = False


def fill_permissions_dict_from_tuple(permissions_dict, permissions_tuple):
    for i, permission_value in enumerate(permissions_tuple):
        permission_name = permissions_dict[i]
        permissions_dict[permission_name] = bool(permission_value)
    return permissions_dict
