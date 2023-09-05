from django.urls import path, include
from rest_framework import routers
from .permissions.views import PermissionsViewListAPI

router = routers.DefaultRouter()

urlpatterns = [
    path("permissions", PermissionsViewListAPI.as_view(), name="permissions"),
    path("deliveries/", include("api.deliveries.urls"), name="deliveries"),
    path("employees/", include("api.employees.urls"), name="employees"),
    path("managements/", include("api.managements.urls"), name="managements"),
    path("notifications/", include("api.notifications.urls"), name="notifications"),
    path("products/", include("api.products.urls"), name="products"),
    path("requests/", include("api.requests.urls"), name="requests"),
    path("stocks/", include("api.stocks.urls"), name="stocks"),
    path("worksites/", include("api.worksites.urls"), name="worksites"),
    path("", include(router.urls)),
]
