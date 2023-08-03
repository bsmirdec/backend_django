from rest_framework.permissions import BasePermission


def create_crud_permissions(model):
    """Décorateur pour créer les permissions CRUD de base pour un modèle donné"""

    class CRUDPermissions(BasePermission):
        def has_permission(self, request, view):
            return True

        def has_objet_permission(self, request, view, obj):
            return True

    permissions = {
        "create": CRUDPermissions().has_permission,
        "read": CRUDPermissions().has_permission,
        "update": CRUDPermissions().has_object_permission,
        "delete": CRUDPermissions().has_object_permission,
    }

    model.permissions = list(permissions.values())

    return model
