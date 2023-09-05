from django.urls import path, include
from rest_framework import routers
from .views import (
    CreateEmployeesNotificationAPI,
    CreateWorksiteNotificationAPI,
    NotificationsViewListAPI,
    NotificationDeleteAPI,
    NotificationIsReadAPI,
)

router = routers.DefaultRouter()

urlpatterns = [
    path("<int:user_id>", NotificationsViewListAPI.as_view(), name="notifications-list"),
    path("create", CreateEmployeesNotificationAPI.as_view(), name="notification-employees-create"),
    path("<int:worksite_id>/create", CreateWorksiteNotificationAPI.as_view(), name="notifications-worksite-create"),
    path("<int:pk>/delete", NotificationDeleteAPI.as_view(), name="notifications-delete"),
    path("<int:pk>/read", NotificationIsReadAPI.as_view(), name="notifications-read"),
    path("", include(router.urls)),
]
