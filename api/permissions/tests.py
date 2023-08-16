from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .CRUDpermissions import get_permissions_for_model, add_permissions_to_dict
from ..worksites.models import Worksite
from ..employees.models import Employee

User = get_user_model()


# class PermissionsTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username="testuser", password="testpassword")
#         self.worksite = Worksite.objects.create(name="Test Worksite")
#         self.employee = Employee.objects.create(user=self.user, position="director")

#     def test_generate_permissions(self):
#         model_permissions = get_permissions_for_model(Worksite)
#         permissions_dict = {}
#         add_permissions_to_dict(model_permissions, permissions_dict)

#         self.assertEqual(permissions_dict["WorksiteCreateObject"], False)
#         self.assertEqual(permissions_dict["WorksiteViewList"], False)
#         self.assertEqual(permissions_dict["WorksiteRetrieveObject"], False)
#         self.assertEqual(permissions_dict["WorksiteUpdateObject"], False)
#         self.assertEqual(permissions_dict["WorksiteDeleteObject"], False)

#     def test_permissions_for_employee(self):
#         employee_permissions = self.employee.get_permissions()

#         self.assertEqual(employee_permissions["WorksiteCreateObject"], False)
#         self.assertEqual(employee_permissions["WorksiteViewList"], False)
#         self.assertEqual(employee_permissions["WorksiteRetrieveObject"], False)
#         self.assertEqual(employee_permissions["WorksiteUpdateObject"], False)
#         self.assertEqual(employee_permissions["WorksiteDeleteObject"], False)


# class CustomPermissionMixinTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.employee_data = {
#             "first_name": "John",
#             "last_name": "Doe",
#             "position": "site_foreman",
#         }
#         self.employee = Employee.objects.create(**self.employee_data)
#         self.user = get_user_model().objects.create_user(email="testuser@example.com", password="testpassword", employee=self.employee)

#     def test_has_permission_with_valid_employee(self):
#         url = reverse("employee-update", kwargs={"pk": self.employee.pk})
#         self.client.force_authenticate(user=self.user)

#         update_data = {
#             "first_name": "Jane",
#             "last_name": "Smith",
#             "position": "manager",
#         }

#         response = self.client.put(url, data=update_data)

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_has_permission_with_invalid_employee(self):
#         """
#         Vérifie que la permission est refusée si l'employé est invalide ou n'existe pas.
#         """
#         url = reverse("employee-update", kwargs={"pk": 999})  # ID invalide pour l'employé
#         self.client.force_authenticate(user=self.user)

#         response = self.client.put(url, data={"..."})  # Données de mise à jour de l'employé

#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         # Vérifier le contenu de la réponse si nécessaire

#     def test_has_permission_with_unauthenticated_user(self):
#         """
#         Vérifie que la permission est refusée si l'utilisateur n'est pas authentifié.
#         """
#         url = reverse("employee-update", kwargs={"pk": self.employee.pk})

#         response = self.client.put(url, data={"..."})  # Données de mise à jour de l'employé

#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         # Vérifier le contenu de la réponse si nécessaire


class LoginAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",
            password="testpassword",
        )

    def test_login(self):
        url = reverse("token_obtain_pair")
        data = {
            "email": "testuser@example.com",
            "password": "testpassword",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        return response.data["access_token"]


class EmployeeUpdateObjectAPIPermissionTests(APITestCase):
    def setUp(self):
        self.employee_data = {
            "first_name": "John",
            "last_name": "Doe",
            "position": "site_foreman",
        }
        self.employee = Employee.objects.create(**self.employee_data)
        self.user = get_user_model().objects.create_user(email="testuser@example.com", password="testpassword", employee=self.employee)

    def test_has_permission_with_valid_employee(self):
        token = LoginAPITestCase.test_login(self)

        url = reverse("employee-update", kwargs={"pk": self.employee.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {token}")

        update_data = {
            "employee_id": self.employee.employee_id,
            "first_name": "Jane",
            "last_name": "Smith",
            "position": "Directeur",
            "is_current": self.employee.is_current,
            "permissions": self.employee.permissions,
        }
        response = self.client.put(url, data=update_data, format="json")
        print("Response status code:", response.status_code)
        print("Response data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_has_permission_with_invalid_employee(self):
        url = reverse("employee-update", kwargs={"pk": 999})  # ID invalide pour l'employé
        token = LoginAPITestCase.test_login(self)
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {token}")

        update_data = {
            "employee_id": 999,
            "first_name": "Jane",
            "last_name": "Smith",
            "position": "Directeur",
            "is_current": True,
            "permissions": [],  # Remplacer par les permissions appropriées
        }

        response = self.client.put(url, data=update_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Vérifier le contenu de la réponse si nécessaire

    def test_has_permission_with_unauthenticated_user(self):
        url = reverse("employee-update", kwargs={"pk": self.employee.pk})
        # Pas d'authentification

        update_data = {
            "employee_id": self.employee.employee_id,
            "first_name": "Jane",
            "last_name": "Smith",
            "position": "Directeur",
            "is_current": self.employee.is_current,
            "permissions": self.employee.permissions,
        }

        response = self.client.put(url, data=update_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Vérifier le contenu de la réponse si nécessaire
