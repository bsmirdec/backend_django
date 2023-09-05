from django.urls import path, include
from rest_framework import routers
from .views import (
    DeliveryViewListAPI,
    DeliveryLinesViewListAPI,
    DeliveryRetrieveObjectAPI,
    DeliveryCreateObjectAPI,
    DeliveryLinesCreateObject,
    DeliveryLinesDeleteObject,
    DeliveryUpdateObjectAPI,
    DeliveryConfirmObjectAPI,
    DeliveryDeleteObjectAPI,
)

router = routers.DefaultRouter()

urlpatterns = [
    path("", DeliveryViewListAPI.as_view(), name="deliveries"),
    path("list/<int:employee_id>", DeliveryViewListAPI.as_view(), name="delivery-for-employee"),
    path("create", DeliveryCreateObjectAPI.as_view(), name="delivery-create"),
    path("<int:delivery_id>", DeliveryRetrieveObjectAPI.as_view(), name="delivery-get"),
    path("<int:delivery_id>/update", DeliveryUpdateObjectAPI.as_view(), name="delivery-update"),
    path("<int:delivery_id>/confirm", DeliveryConfirmObjectAPI.as_view(), name="delivery-update"),
    path("<int:delivery_id>/delete", DeliveryDeleteObjectAPI.as_view(), name="delivery-delete"),
    path("lines/create", DeliveryLinesCreateObject.as_view(), name="delivery-lines-create"),
    path("lines/<int:delivery_id>", DeliveryLinesViewListAPI.as_view(), name="delivery-lines-for-order"),
    path("lines/<int:delivery_id>/delete", DeliveryLinesDeleteObject.as_view(), name="delivery-lines-create"),
    path("", include(router.urls)),
]
