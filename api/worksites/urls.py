from django.urls import path, include
from rest_framework import routers
from .views import (
    WorksiteUpdateObjectAPI,
    WorksiteCreateObjectAPI,
    WorksiteDeleteObjectAPI,
    WorksiteRetrieveObjectAPI,
    WorksiteViewListAPI,
)

router = routers.DefaultRouter()

urlpatterns = [
    path("", WorksiteViewListAPI.as_view(), name="worksites"),
    path("create", WorksiteCreateObjectAPI.as_view(), name="worksite_create"),
    path("<int:pk>/get", WorksiteRetrieveObjectAPI.as_view(), name="worksite-get"),
    path("<int:pk>/update", WorksiteUpdateObjectAPI.as_view(), name="worksite-update"),
    path("<int:pk>/delete", WorksiteDeleteObjectAPI.as_view(), name="worksite-delete"),
    path("", include(router.urls)),
]
