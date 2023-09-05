from django.urls import path, include
from rest_framework import routers
from .views import (
    OrderViewListAPI,
    OrderLinesViewListAPI,
    RetourViewListAPI,
    OrderRetrieveObjectAPI,
    RetourRetrieveObjectAPI,
    OrderCreateObjectAPI,
    OrderLinesCreateObject,
    OrderLinesDeleteObject,
    OrderUpdateObjectAPI,
    OrderDeleteObjectAPI,
    OrderConfirmAPI,
)

router = routers.DefaultRouter()

urlpatterns = [
    path("orders", OrderViewListAPI.as_view(), name="orders"),
    path("orders/<int:employee_id>", OrderViewListAPI.as_view(), name="order-for-employee"),
    path("order/create", OrderCreateObjectAPI.as_view(), name="order-create"),
    path("order/<int:order_id>", OrderRetrieveObjectAPI.as_view(), name="order-get"),
    path("order/<int:order_id>/update", OrderUpdateObjectAPI.as_view(), name="order-update"),
    path("order/<int:order_id>/delete", OrderDeleteObjectAPI.as_view(), name="order-delete"),
    path("order/<int:order_id>/confirm", OrderConfirmAPI.as_view(), name="order-confirm"),
    path("order/lines/create", OrderLinesCreateObject.as_view(), name="order-lines-create"),
    path("order/lines/<int:order_id>", OrderLinesViewListAPI.as_view(), name="order-lines-for-order"),
    path("order/lines/<int:order_id>/delete", OrderLinesDeleteObject.as_view(), name="order-lines-create"),
    path("retours", RetourViewListAPI.as_view(), name="retours"),
    path("retour/<int:pk>", RetourRetrieveObjectAPI.as_view(), name="retour_get"),
    path("", include(router.urls)),
]
