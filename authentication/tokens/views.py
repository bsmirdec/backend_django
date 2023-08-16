from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ParseError

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


from ..users.models import CustomUser


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

        user.last_login = timezone.now()
        user.save()

        access_token, refresh_token = get_tokens_for_user(user)

        return Response({"access_token": access_token, "refresh_token": refresh_token})


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh["user_id"] = user.user_id
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    return access_token, refresh_token


class BlacklistTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            raise ParseError(_("Le token d'actualisation est manquant."))

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Déconnexion réussie."})
        except TokenError:
            raise ParseError(_("Le token d'actualisation est invalide ou a déjà été révoqué."))
