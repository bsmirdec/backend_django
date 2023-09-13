from django.urls import path, include
from rest_framework import routers
from .views import WorksiteStockViewListAPI, WorksiteMaxStockCreateAPI, WorksiteMaxStockViewListAPI

router = routers.DefaultRouter()

urlpatterns = [
    path("worksite/<int:worksite_id>", WorksiteStockViewListAPI.as_view(), name="worksite-stocks"),
    path("worksite/max/<int:worksite_id>", WorksiteMaxStockViewListAPI.as_view(), name="worksite-max-stocks"),
    path("worksite/max/create", WorksiteMaxStockCreateAPI.as_view(), name="worksite-max-stocks-create"),
    path("", include(router.urls)),
]
