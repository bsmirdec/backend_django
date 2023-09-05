from django.urls import path, include
from rest_framework import routers
from .views import (
    EmployeeCreateObjectAPI,
    EmployeeDeleteObjectAPI,
    EmployeeRetrieveObjectAPI,
    EmployeeUpdateObjectAPI,
    EmployeeViewListAPI,
    SiteDirectorsViewListAPI,
    AdministratorsViewListAPI,
)

router = routers.DefaultRouter()

urlpatterns = [
    path("", EmployeeViewListAPI.as_view(), name="employees-list"),
    path("site-directors", SiteDirectorsViewListAPI.as_view(), name="site-directors-list"),
    path("administrators", AdministratorsViewListAPI.as_view(), name="administrators-list"),
    path("create", EmployeeCreateObjectAPI.as_view(), name="employee-create"),
    path("<int:pk>/", EmployeeRetrieveObjectAPI.as_view(), name="employee-get"),
    path("<int:pk>/update", EmployeeUpdateObjectAPI.as_view(), name="employee-update"),
    path("<int:pk>/delete", EmployeeDeleteObjectAPI.as_view(), name="employee-delete"),
    path("", include(router.urls)),
]
