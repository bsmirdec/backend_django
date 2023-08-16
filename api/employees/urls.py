from django.urls import path, include
from rest_framework import routers
from .views import (
    EmployeeCreateObjectAPI,
    EmployeeDeleteObjectAPI,
    EmployeeRetrieveObjectAPI,
    EmployeeUpdateObjectAPI,
    EmployeeViewListAPI,
    SiteDirectorsViewListAPI,
)

router = routers.DefaultRouter()

urlpatterns = [
    path("", EmployeeViewListAPI.as_view(), name="employees-list"),
    path("site-directors", SiteDirectorsViewListAPI.as_view(), name="site-directors-list"),
    path("create", EmployeeCreateObjectAPI.as_view(), name="employee-create"),
    path("<int:pk>/", EmployeeRetrieveObjectAPI.as_view(), name="employee-delete"),
    path("<int:pk>/update", EmployeeUpdateObjectAPI.as_view(), name="employee-update"),
    path("<int:pk>/delete", EmployeeDeleteObjectAPI.as_view(), name="employee-delete"),
    path("", include(router.urls)),
]
