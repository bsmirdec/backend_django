from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
from .views import CategoryViewListAPI, TypeViewListAPI, ProductViewListAPI

router = routers.DefaultRouter()

urlpatterns = [
    path("", ProductViewListAPI.as_view(), name="products"),
    path("categories", CategoryViewListAPI.as_view(), name="categories"),
    path("types", TypeViewListAPI.as_view(), name="types"),
    path("", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
