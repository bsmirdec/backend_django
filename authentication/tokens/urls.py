from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import MyTokenObtainPairView, BlacklistTokenView

router = DefaultRouter()

urlpatterns = [
    path("obtain/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("blacklist/", BlacklistTokenView.as_view(), name="token_blacklist"),
    path("", include(router.urls)),
]
