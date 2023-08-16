from rest_framework import permissions
from .authentication import MyCustomJWTAuthentication


class IsJWTAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        authentication = MyCustomJWTAuthentication()
        user, _ = authentication.authenticate(request)
        print("Authenticated user:", user)
        return user is not None
