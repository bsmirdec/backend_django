from django.urls import path, include
from rest_framework import routers
from .views import (
    EmployeeCreateObjectAPI,
    EmployeeDeleteObjectAPI,
    EmployeeRetrieveObjectAPI,
    EmployeeUpdateObjectAPI,
    EmployeeViewListAPI,
)

router = routers.DefaultRouter()

urlpatterns = [
    path("", EmployeeViewListAPI.as_view(), name="employees-list"),
    path("create", EmployeeCreateObjectAPI.as_view(), name="employee-create"),
    path("<int:employee_id>/", EmployeeRetrieveObjectAPI.as_view(), name="employee-delete"),
    path("<int:employee_id>/update", EmployeeUpdateObjectAPI.as_view(), name="employee-update"),
    path("<int:employee_id>/delete", EmployeeDeleteObjectAPI.as_view(), name="employee-update"),
    path("", include(router.urls)),
]
