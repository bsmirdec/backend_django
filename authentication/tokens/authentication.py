from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings


from ..users.models import CustomUser


class MyCustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user_id = validated_token[api_settings.USER_ID_CLAIM]
        try:
            user = CustomUser.objects.get(user_id=user_id)
            return user
        except CustomUser.DoesNotExist:
            return None
