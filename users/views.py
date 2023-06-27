from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, OR
from rest_framework.decorators import api_view, permission_classes

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import CustomUser
from .serializers import UserSerializer
from .permissions import UpdateOwnAccount
from api.models import SiteDirector, SiteSupervisor, SiteForeman, Administrator


class MyTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "Nom d'utilisateur ou mot de passe incorrect."}, status=400)

        if not user.check_password(password):
            return Response({"error": "Nom d'utilisateur ou mot de passe incorrect."}, status=400)

        access_token, refresh_token = get_tokens_for_user(user)

        return Response({"access_token": access_token, "refresh_token": refresh_token})


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [OR(UpdateOwnAccount, IsAdminUser), IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        "first_name",
        "last_name",
    )

    def get_permissions(self):
        if self.action == "create":
            # Apply AllowAny permission only for the 'create' action
            permission_classes = [AllowAny]
        else:
            # Use the default permission classes for other actions
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_tokens(request):
    user = request.user  # Récupérer l'utilisateur authentifié depuis la requête
    access_token, refresh_token = get_tokens_for_user(user)
    # Faites quelque chose avec les tokens (par exemple, renvoyez-les en tant que réponse JSON)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh["user_id"] = user.id
    refresh["email"] = user.email
    refresh["first_name"] = user.first_name
    refresh["last_name"] = user.last_name
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    return access_token, refresh_token


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_permissions(request):
    user = request.user

    permissions = []

    if SiteDirector.objects.filter(user=user).exists():
        permissions.append("site_director")

    if SiteSupervisor.objects.filter(user=user).exists():
        permissions.append("site_supervisor")

    if SiteForeman.objects.filter(user=user).exists():
        permissions.append("site_foreman")

    if Administrator.objects.filter(user=user).exists():
        permissions.append("administrator")

    return Response(permissions)


class BlacklistTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Déconnexion réussie."})
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
