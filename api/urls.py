from django.urls import path, include
from rest_framework import routers
from .permissions.views import PermissionsViewListAPI

router = routers.DefaultRouter()

urlpatterns = [
    path("permissions", PermissionsViewListAPI.as_view(), name="permissions"),
    path("worksites/", include("api.worksites.urls"), name="worksites"),
    path("employees/", include("api.employees.urls"), name="employees"),
    path("", include(router.urls)),
]
