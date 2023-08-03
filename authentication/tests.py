from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserCreateObjectAPITest(APITestCase):
    def test_user_create_object_api(self):
        url = reverse("user_create_object")
        data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user_id", response.data)
        self.assertIn("email", response.data)


# class UserMatchEmployeeAPITest(APITestCase):
#     def test_user_match_employee_api(self):
#         # Assume that you have created a user with an ID (user_id) here.
#         url = reverse("user_match_employee")
#         data = {
#             "user_id": 1,
#             "first_name": "John",
#             "last_name": "Doe",
#         }
#         response = self.client.post(url, data=data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


class MyTokenObtainPairViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("token_obtain_pair")
        self.user_data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        self.user = User.objects.create_user(email=self.user_data["email"], password=self.user_data["password"])

    def test_token_obtain_pair_view(self):
        data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = self.client.post(self.url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

    def test_token_obtain_pair_view_invalid_credentials(self):
        data = {
            "email": "test@example.com",
            "password": "incorrectpassword",
        }
        response = self.client.post(self.url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("error", response.data)


class BlacklistTokenViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="testpassword")
        self.refresh = RefreshToken.for_user(self.user)
        self.token = str(self.refresh.access_token)
        self.url = reverse("blacklist_token")

    def test_blacklist_token_view_success(self):
        data = {
            "refresh_token": self.token,
        }
        try:
            response = self.client.post(self.url, data=data, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except Exception as e:
            print("Exception occurred:", e)
            raise

    def test_blacklist_token_view_invalid_token(self):
        data = {
            "refresh_token": "invalidtoken",
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
