from rest_framework.permissions import BasePermission, SAFE_METHODS


class UpdateOwnAccount(BasePermission):
    """Allow users to edit their own account"""

    def has_object_permission(self, request, view, obj):
        """check user is trying to edit their own account"""

        if request.method in SAFE_METHODS:
            return True

        return obj.id == request.user.id
