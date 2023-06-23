# from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import CustomUser
from .serializers import UserSerializer
from .permissions import UpdateOwnAccount


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
    permission_classes = [UpdateOwnAccount, IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        "first_name",
        "last_name",
    )

    # def get_queryset(self):
    #     return CustomUser.objects.all()

    # def get_object(self, queryset=None, **kwargs):
    #     item = self.kwargs.get("pk")
    #     return get_object_or_404(CustomUser, worksite_id=item)

    # def post(self, request):
    #     reg_serializer = RegisterUserSerializer(data=request.data)
    #     if reg_serializer.is_valid():
    #         newuser = reg_serializer.save()
    #         if newuser:
    #             return Response(status=status.HTTP_201_CREATED)
    #     return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
