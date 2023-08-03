from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..users.models import CustomUser


class AuthenticationTokenViewsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email="test@example.com",
            password="testpassword",
        )

    def test_token_obtain(self):
        url = reverse("token_obtain_pair")
        data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

    def test_token_refresh(self):
        refresh_token = RefreshToken.for_user(self.user)
        url = reverse("token_refresh")
        data = {"refresh": str(refresh_token)}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_token_blacklist(self):
        refresh_token = RefreshToken.for_user(self.user)
        refresh_token.blacklist()
        url = reverse("token_blacklist")
        data = {"refresh_token": str(refresh_token)}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
