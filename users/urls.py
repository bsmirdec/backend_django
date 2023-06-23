from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, BlacklistTokenView

app_name = "users"

router = DefaultRouter()
router.register("", UserViewSet, basename="users")
# router.register("login", LoginViewSet, basename="login")

urlpatterns = [
    *router.urls,
    path("logout/blacklist/", BlacklistTokenView.as_view(), name="blacklist"),
]
