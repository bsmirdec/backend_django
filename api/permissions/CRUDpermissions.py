import re
from rest_framework.permissions import BasePermission

from authentication.tokens.authentication import MyCustomJWTAuthentication

from ..employees.models import Employee


def camel_case_to_snake_case(name):
    result = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
    return result.lower()


class CustomPermissionMixin(BasePermission):
    authentication_classes = [MyCustomJWTAuthentication]

    def get_employee(self, request):
        try:
            return Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            return None

    def has_permission(self, request, view):
        employee = self.get_employee(request)
        if not employee:
            return False
        permission_name = camel_case_to_snake_case(view.__class__.__name__)
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
