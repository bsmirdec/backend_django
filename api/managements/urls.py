from django.urls import path, include
from rest_framework import routers
from .views import (
    ManagementCreateObjectAPI,
    ManagementDeleteObjectAPI,
    ManagementRetrieveObjectAPI,
    ManagementViewListAPI,
    GetEmployeeForWorksiteAPI,
    GetWorksiteForEmployeeAPI,
)

router = routers.DefaultRouter()

urlpatterns = [
    path("", ManagementViewListAPI.as_view(), name="managements"),
    path("create", ManagementCreateObjectAPI.as_view(), name="management-create"),
    path("<int:worksite_id>/<int:employee_id>/get", ManagementRetrieveObjectAPI.as_view(), name="management-get"),
    path("<int:worksite_id>/<int:employee_id>/delete", ManagementDeleteObjectAPI.as_view(), name="management-delete"),
    path("get-worksite-for-employee/<int:employee_id>/", GetWorksiteForEmployeeAPI.as_view(), name="get-worksite-for-employee"),
    path("get-employee-for-worksite/<int:worksite_id>/", GetEmployeeForWorksiteAPI.as_view(), name="get-employee-for-worksite"),
    path("", include(router.urls)),
]
