from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import CustomUser
from .models import Client, Worksite, Management, WorkingPosition, SiteDirector, SiteSupervisor, SiteForeman
from .serializers import (
    ClientSerializer,
    WorksiteSerializer,
    ManagementSerializer,
    SiteDirectorSerializer,
    SiteForemanSerializer,
    SiteSupervisorSerializer,
)

User = CustomUser


class ClientTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)
        self.client_1 = Client.objects.create(name="Client 1")

    def test_create_client(self):
        data = {"name": "New Client"}
        response = self.client.post("/api/clients/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(), 2)

    def test_retrieve_client(self):
        response = self.client.get(f"/api/clients/{self.client_1.id}/")
        client = Client.objects.get(id=self.client_1.id)
        serializer = ClientSerializer(client)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    # Add more tests for update, delete, list views


class WorksiteTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)
        self.client_1 = Client.objects.create(name="Client 1")
        self.worksite_1 = Worksite.objects.create(name="Worksite 1", client=self.client_1)

    def test_create_worksite(self):
        data = {"name": "New Worksite", "client": self.client_1.id}
        response = self.client.post("/api/worksites/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Worksite.objects.count(), 2)

    def test_retrieve_worksite(self):
        response = self.client.get(f"/api/worksites/{self.worksite_1.id}/")
        worksite = Worksite.objects.get(id=self.worksite_1.id)
        serializer = WorksiteSerializer(worksite)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    # Add more tests for update, delete, list views


class ManagementTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)
        self.client_1 = Client.objects.create(name="Client 1")
        self.worksite_1 = Worksite.objects.create(name="Worksite 1", client=self.client_1)
        self.management_1 = Management.objects.create(worksite=self.worksite_1)

    def test_create_management(self):
        data = {"worksite": self.worksite_1.id}
        response = self.client.post("/api/managements/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Management.objects.count(), 2)

    def test_retrieve_management(self):
        response = self.client.get(f"/api/managements/{self.management_1.id}/")
        management = Management.objects.get(id=self.management_1.id)
        serializer = ManagementSerializer(management)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_management(self):
        data = {"worksite": self.worksite_1.id}
        response = self.client.post("/api/managements/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Management.objects.count(), 2)

    def test_retrieve_management(self):
        response = self.client.get(f"/api/managements/{self.management_1.id}/")
        management = Management.objects.get(id=self.management_1.id)
        serializer = ManagementSerializer(management)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_staff(self):
        position_2 = WorkingPosition.objects.create(name="Position 2")
        data = {"staff_id": position_2.id}
        response = self.client.patch(f"/api/managements/{self.management_1.id}/update_staff/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        management = Management.objects.get(id=self.management_1.id)
        self.assertEqual(management.staff, position_2)

    def test_delete_staff(self):
        response = self.client.delete(f"/api/managements/{self.management_1.id}/delete_staff/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        management = Management.objects.get(id=self.management_1.id)
        self.assertIsNone(management.staff)


class WorkingPositionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)
        self.position_1 = SiteDirector.objects.create(name="Site Director 1")

    def test_create_working_position(self):
        data = {"name": "New Position"}
        response = self.client.post("/api/positions/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SiteDirector.objects.count(), 2)

    def test_retrieve_working_position(self):
        response = self.client.get(f"/api/positions/{self.position_1.id}/")
        position = SiteDirector.objects.get(id=self.position_1.id)
        serializer = SiteDirectorSerializer(position)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    # Add more tests for update, delete, list views


# Ajouter des tests supplémentaires pour les autres modèles (Staff, Shift, etc.)


class ManagementTestCase(TestCase):
    # ... setup précédent ...

    def test_create_management(self):
        data = {"worksite": self.worksite_1.id}
        response = self.client.post("/api/managements/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Management.objects.count(), 2)

    def test_retrieve_management(self):
        response = self.client.get(f"/api/managements/{self.management_1.id}/")
        management = Management.objects.get(id=self.management_1.id)
        serializer = ManagementSerializer(management)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_staff(self):
        position_2 = SiteSupervisor.objects.create(name="Site Supervisor 2")
        data = {"staff_id": position_2.id}
        response = self.client.patch(f"/api/managements/{self.management_1.id}/update_staff/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        management = Management.objects.get(id=self.management_1.id)
        self.assertEqual(management.staff, position_2)

    def test_delete_staff(self):
        response = self.client.delete(f"/api/managements/{self.management_1.id}/delete_staff/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        management = Management.objects.get(id=self.management_1.id)
        self.assertIsNone(management.staff)

        # Add more tests for create_staff, update_staff, delete_staff

        # Ajouter des tests supplémentaires pour les autres vues (ClientViewSet, WorksiteViewSet, etc.)

        # from django.test import TestCase
        # from django.utils import timezone
        # from django.urls import reverse
        # from rest_framework import status
        # from rest_framework.test import APITestCase
        # from .models import Worksite, Client
        # from users.models import CustomUser

        # class Test_Create_Worksite(TestCase):
        #     @classmethod
        #     def setUpTestData(cls) -> None:
        #         test_client = Client.objects.create(name="django")
        #         # testuser1 = User.objects.create_user(username="test_user1", password="123456789")
        #         test_worksite = Worksite.newobjects.create(
        #             sector="GO", name="test_name", client_id=1, city="test_city", adress="test_adress", started=timezone.now(), status="etudes"
        #         )

        #     def test_worksite_content(self):
        #         worksite = Worksite.newobjects.get(worksite_id=1)
        #         client = Client.objects.get(id=1)
        #         sector = f"{worksite.sector}"
        #         name = f"{worksite.name}"
        #         city = f"{worksite.city}"
        #         adress = f"{worksite.adress}"
        #         self.assertEqual(client.name, "django")
        #         self.assertEqual(name, "test_name")
        #         self.assertEqual(sector, "GO")
        #         self.assertEqual(city, "test_city")
        #         self.assertEqual(adress, "test_adress")
        #         self.assertEqual(str(worksite), "test_city - test_name")
        #         self.assertEqual(str(client), "django")

        # class WorksiteTests(APITestCase):
        #     def test_view_worksites(self):
        #         self.test_client = Client.objects.create(name="django")
        #         self.testuser1 = CustomUser.objects.create_superuser(
        #             email="test1@example.com", first_name="test_name", last_name="test_user1", password="123456789"
        #         )
        #         self.client.login(email=self.testuser1.email, password="123456789")

        #         url = reverse("api:worksite-list")
        #         response = self.client.get(url, format="json")
        #         self.assertEqual(response.status_code, status.HTTP_200_OK)

        #     def test_create_worksite(self):
        #         self.test_client = Client.objects.create(name="django")
        #         self.testuser1 = CustomUser.objects.create_superuser(
        #             email="test1@example.com", first_name="test_name", last_name="test_user1", password="123456789"
        #         )
        #         self.client.login(email=self.testuser1.email, password="123456789")

        #         data = {"sector": "GO", "name": "test_name", "client_id": 1, "city": "test_city", "adress": "test_adress", "started": timezone.now()}
        #         url = reverse("api:worksite-create")
        #         response = self.client.post(url, data, format="json")
        #         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #     # def test_update_worksite(self):
        #     #     client = APIClient()

        #     #     self.test_client = Client.objects.create(name="django")
        #     #     self.testuser1 = User.objects.create_user(username="test_user1", password="123456789")
        #     #     self.testuser2 = User.objects.create_superuser(username="test_user1", password="123456789")
        #     #     self.client.login(username=self.testuser1.username, password="123456789")
        # self.assertEqual(response.data, serializer.data)
