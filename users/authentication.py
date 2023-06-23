from rest_framework.authentication import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication


UserModel = get_user_model()


class MyCustomJWTAuthentication(JWTAuthentication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = UserModel
