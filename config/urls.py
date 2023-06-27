from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from users.views import MyTokenObtainPairView, user_permissions


urlpatterns = [
    path("api/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("admin/", admin.site.urls),
    path("api/users/permissions/", user_permissions, name="user_permissions"),
    path("api/", include("api.urls"), name="api"),
    path("api/users/", include("users.urls", namespace="users")),
    path("docs/", include_docs_urls(title="CobApp-API")),
    path(
        "schema/",
        get_schema_view(
            title="CobApp-API",
            description="API for CobApp",
            version="1.0.0",
        ),
        name="coreapi-schema",
    ),
]
