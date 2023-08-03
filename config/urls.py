from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    path("api/token/", include("authentication.tokens.urls"), name="tokens"),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls"), name="api"),
    path("api/users/", include("authentication.users.urls"), name="users"),
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
