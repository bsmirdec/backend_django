from django.urls import include, path
from rest_framework import routers
from .views import ClientViewSet, WorksiteViewSet, ManagementViewSet

app_name = "api"

router = routers.DefaultRouter()
router.register(r"clients", ClientViewSet)
router.register(r"worksites", WorksiteViewSet)
router.register(r"management", ManagementViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
