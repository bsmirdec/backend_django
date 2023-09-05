from django.urls import path, include
from rest_framework import routers
from .views import WorksiteStockViewListAPI

router = routers.DefaultRouter()

urlpatterns = [
    path("worksite/<int:worksite_id>", WorksiteStockViewListAPI.as_view(), name="worksite-stocks"),
    path("", include(router.urls)),
]
