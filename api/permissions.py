from rest_framework.permissions import BasePermission
from .models import SiteDirector, SiteSupervisor, SiteForeman, Administrator


class IsSiteDirector(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return SiteDirector.objects.filter(user=user).exists()


class IsSiteSupervisor(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return SiteSupervisor.objects.filter(user=user).exists()


class IsSiteForeman(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return SiteForeman.objects.filter(user=user).exists()


class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return Administrator.objects.filter(user=user).exists()


class IsExternal(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return not (
            IsSiteDirector().has_permission(request, view)
            or IsSiteSupervisor().has_permission(request, view)
            or IsSiteForeman().has_permission(request, view)
            or Administrator().has_permission(request, view)
        )
