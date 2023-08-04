import json
from django.test import TestCase
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from .models import CustomUser
from api.employees.models import Employee
from .services import user_create, user_link_to_employee, user_update, user_delete
from .selectors import user_list, user_get, user_get_employee, user_get_permissions
from api.permissions.PERMISSIONS_BY_POSITION import PERMISSIONS_BY_POSITION
from .views import UserUpdateAPI


class CustomUserModelTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "test@example.com",
            "password": "testpassword",
        }

    def test_create_superuser(self):
        user = CustomUser.objects.create_superuser(**self.user_data)

        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_user(self):
        user = CustomUser.objects.create_user(**self.user_data)

        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email="", password="testpassword")

    def test_create_user_without_password(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email="test@example.com", password="")

    def test_create_user_with_existing_email(self):
        CustomUser.objects.create_user(**self.user_data)
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(**self.user_data)

    def test_validate_unique_email(self):
        user1 = CustomUser.objects.create_user(email="test@example.com", password="testpassword")
        user2 = CustomUser(email="test@example.com", password="testpassword")

        with self.assertRaises(ValidationError):
            user2.full_clean()


class CustomUserServiceTestCase(TestCase):
    def test_user_create(self):
        data = {
            "email": "test@example.com",
            "password": "password",
        }
        user = user_create(data)
        self.assertEqual(user.email, "test@example.com")

    def test_user_link_to_employee(self):
        self.employee_data = {
            "first_name": "John",
            "last_name": "Doe",
            "position": "site_foreman",
        }
        data = {
            "email": "test@example.com",
            "password": "password",
        }
        user = user_create(data)
        user_id = user.user_id
        first_name = "John"
        last_name = "Doe"
        employee = Employee.objects.create(**self.employee_data)
        user = user_link_to_employee(user_id, first_name, last_name)
        self.assertEqual(user.employee.first_name, first_name)
        self.assertEqual(user.employee.last_name, last_name)

    def test_user_link_to_employee_with_non_existing_employee(self):
        self.employee_data = {
            "first_name": "John",
            "last_name": "Doe",
            "position": "site_foreman",
        }
        data = {
            "email": "test@example.com",
            "password": "password",
        }
        user = user_create(data)
        user_id = user.user_id
        first_name = "NonExisting"
        last_name = "Employee"
        user = user_link_to_employee(user_id, first_name, last_name)
        self.assertIsNone(user)

    def test_user_update(self):
        user = CustomUser.objects.create_user(email="test@example.com", password="password")
        data = {
            "is_validated": True,
            "is_staff": True,
        }
        user = user_update(user, data)
        self.assertEqual(user.is_validated, True)
        self.assertEqual(user.is_staff, True)

    def test_user_delete(self):
        user = CustomUser.objects.create_user(email="test@example.com", password="password")
        user_delete(user)
        with self.assertRaises(CustomUser.DoesNotExist):
            CustomUser.objects.get(email="test@example.com")


class CustomUserSelectorTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email="test@example.com", password="password")

    def test_user_list(self):
        users = user_list()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0], self.user)

    def test_user_get(self):
        user = user_get(pk=self.user.pk)
        self.assertEqual(user, self.user)

        with self.assertRaises(ObjectDoesNotExist):
            user_get(pk=100)

    def test_user_get_employee(self):
        self.user.is_validated = True
        self.user.save()

        employee = Employee.objects.create(first_name="John", last_name="Doe", position="site_foreman")
        self.user.employee = employee
        self.user.save()

        result_employee = user_get_employee(pk=self.user.pk)
        self.assertEqual(result_employee, employee)

    def test_user_get_permissions(self):
        self.user.is_validated = True
        self.user.save()

        employee = Employee.objects.create(
            first_name="John", last_name="Doe", position="site_foreman", permissions=json.dumps({"can_view": True, "can_edit": False})
        )
        self.user.employee = employee
        print(employee)
        self.user.save()

        permissions = user_get_permissions(pk=self.user.pk)
        self.assertEqual(permissions, {"can_view": True, "can_edit": False})


class CustomUserViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = CustomUser.objects.create_superuser(
            email="admin@example.com",
            password="adminpassword",
            is_validated=True,
        )
        self.admin_token = self.get_auth_token(self.admin_user)

    def get_auth_token(self, user):
        response = self.client.post(reverse("token_obtain_pair"), {"email": user.email, "password": "adminpassword"})
        return response.data["access_token"]

    def test_create_user(self):
        url = reverse("user-create")
        data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = CustomUser.objects.get(email=data["email"])
        self.assertEqual(user.email, data["email"])

    def test_create_user_with_existing_email(self):
        url = reverse("user-create")
        data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        self.client.post(url, data, format="json")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_match_employee(self):
        url = reverse("user-match-employee")
        data = {
            "user_id": self.admin_user.pk,
            "first_name": "John",
            "last_name": "Doe",
        }
        self.employee_data = {
            "first_name": "John",
            "last_name": "Doe",
            "position": "administrator",
        }
        employee = Employee.objects.create(**self.employee_data)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = CustomUser.objects.get(pk=self.admin_user.pk)
        self.assertIsNotNone(user.employee)
        self.assertEqual(user.employee.first_name, "John")
        self.assertEqual(user.employee.last_name, "Doe")

    def test_user_match_employee_with_invalid_data(self):
        url = reverse("user-match-employee")
        data = {
            "user_id": self.admin_user.pk,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_get_permissions(self):
        data = {
            "user_id": self.admin_user.pk,
            "first_name": "John",
            "last_name": "Doe",
        }
        self.employee_data = {
            "first_name": "John",
            "last_name": "Doe",
            "position": "administrator",
        }
        employee = Employee.objects.create(**self.employee_data)
        url = reverse("user-match-employee")
        response = self.client.post(url, data, format="json")
        url = reverse("user-permissions", args=[self.admin_user.pk])
        response = self.client.get(url, format="json", HTTP_AUTHORIZATION=f"JWT {self.admin_token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, employee.get_permissions())

    def test_user_list(self):
        url = reverse("users")
        response = self.client.get(url, format="json", HTTP_AUTHORIZATION=f"JWT {self.admin_token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_retrieve(self):
        user = CustomUser.objects.create_user(
            email="test@example.com",
            password="testpassword",
        )
        url = reverse("user-get", args=[user.pk])
        response = self.client.get(url, format="json", HTTP_AUTHORIZATION=f"JWT {self.admin_token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update(self):
        user = CustomUser.objects.create_user(
            email="test@example.com",
            password="testpassword",
        )
        url = reverse("user-update", args=[user.pk])
        data = {"is_active": True, "is_staff": False, "is_validated": True}
        response = self.client.put(url, data, format="json", HTTP_AUTHORIZATION=f"JWT {self.admin_token}")
        serializer = UserUpdateAPI.UserUpdateSerializer(user, data=data)
        if not serializer.is_valid():
            print(serializer.errors)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_user = CustomUser.objects.get(pk=user.pk)
        self.assertEqual(updated_user.is_validated, True)

    def test_user_delete(self):
        user = CustomUser.objects.create_user(
            email="test@example.com",
            password="testpassword",
        )
        url = reverse("user-delete", args=[user.pk])
        response = self.client.delete(url, format="json", HTTP_AUTHORIZATION=f"JWT {self.admin_token}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(CustomUser.DoesNotExist):
            CustomUser.objects.get(pk=user.pk)
