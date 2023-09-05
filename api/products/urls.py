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
