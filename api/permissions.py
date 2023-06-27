from rest_framework.permissions import BasePermission
from .models import SiteDirector, SiteSupervisor, SiteForeman, Administrator


class IsSiteDirector(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return SiteDirector.objects.filter(user=user).exists()

    def __str__(self):
        return "IsSiteDirector"


class IsSiteSupervisor(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return SiteSupervisor.objects.filter(user=user).exists()

    def __str__(self):
        return "IsSiteSupervisor"


class IsSiteForeman(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return SiteForeman.objects.filter(user=user).exists()

    def __str__(self):
        return "IsSiteForeman"


class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return Administrator.objects.filter(user=user).exists()

    def __str__(self):
        return "IsAdministrator"


class IsExternal(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return not (
            IsSiteDirector().has_permission(request, view)
            or IsSiteSupervisor().has_permission(request, view)
            or IsSiteForeman().has_permission(request, view)
            or Administrator().has_permission(request, view)
        )

    def __str__(self):
        return "IsExternal"
