from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings


from ..users.models import CustomUser


class MyCustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Obtenez le token du JWT dans l'en-tête de la requête
        auth_header = self.get_header(request)
        # print(
        #     "DEBUG: Auth header:",
        #     auth_header,
        # )
        if auth_header is None:
            return None

        raw_token = self.get_raw_token(auth_header)
        # print("DEBUG: Raw token:", raw_token)
        if raw_token is None:
            return None

        # Validez le token et obtenez le payload
        try:
            validated_token = self.get_validated_token(raw_token)
            # print("Validated token:", validated_token)
        except AuthenticationFailed as e:
            # print("ERROR: Token validation failed:", e)
            raise e

        user = self.get_user(validated_token)
        # print("DEBUG: User:", user)
        if user is None:
            return None

        return user, raw_token

    def get_user(self, validated_token):
        user_id = validated_token[api_settings.USER_ID_CLAIM]
        try:
            user = CustomUser.objects.get(user_id=user_id)
            return user
        except CustomUser.DoesNotExist:
            return None
