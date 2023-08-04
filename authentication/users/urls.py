from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserListAPI,
    UserRetrieveAPI,
    UserCreateObjectAPI,
    UserMatchEmployeeAPI,
    UserGetPermissions,
    UserGetEmployee,
    UserUpdateAPI,
    UserDeleteAPI,
)

router = DefaultRouter()

urlpatterns = [
    path("list/", UserListAPI.as_view(), name="users"),
    path("create/", UserCreateObjectAPI.as_view(), name="user-create"),
    path("match/", UserMatchEmployeeAPI.as_view(), name="user-match-employee"),
    path("<int:pk>/get", UserRetrieveAPI.as_view(), name="user-get"),
    path("<int:pk>/permissions", UserGetPermissions.as_view(), name="user-permissions"),
    path("<int:pk>/employee", UserGetEmployee.as_view(), name="user-employee"),
    path("<int:pk>/update", UserUpdateAPI.as_view(), name="user-update"),
    path("<int:pk>/delete", UserDeleteAPI.as_view(), name="user-delete"),
    path("", include(router.urls)),
]
