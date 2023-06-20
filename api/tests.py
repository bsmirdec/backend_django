from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Worksite, Client


class Test_Create_Worksite(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        test_client = Client.objects.create(name="django")
        # testuser1 = User.objects.create_user(username="test_user1", password="123456789")
        test_worksite = Worksite.newobjects.create(
            sector="GO", name="test_name", client_id=1, city="test_city", adress="test_adress", started=timezone.now(), status="etudes"
        )

    def test_worksite_content(self):
        worksite = Worksite.newobjects.get(worksite_id=1)
        client = Client.objects.get(id=1)
        sector = f"{worksite.sector}"
        name = f"{worksite.name}"
        city = f"{worksite.city}"
        adress = f"{worksite.adress}"
        self.assertEqual(client.name, "django")
        self.assertEqual(name, "test_name")
        self.assertEqual(sector, "GO")
        self.assertEqual(city, "test_city")
        self.assertEqual(adress, "test_adress")
        self.assertEqual(str(worksite), "test_city - test_name")
        self.assertEqual(str(client), "django")


class WorksiteTests(APITestCase):
    def test_view_worksites(self):
        self.test_client = Client.objects.create(name="django")
        self.testuser1 = User.objects.create_superuser(username="test_user1", password="123456789")
        self.client.login(username=self.testuser1.username, password="123456789")

        url = reverse("worksitelist")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_worksite(self):
        self.test_client = Client.objects.create(name="django")
        self.testuser1 = User.objects.create_superuser(username="test_user1", password="123456789")
        self.client.login(username=self.testuser1.username, password="123456789")

        data = {"sector": "GO", "name": "test_name", "client_id": 1, "city": "test_city", "adress": "test_adress", "started": timezone.now()}
        url = reverse("worksitelistcreate")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_update_worksite(self):
    #     client = APIClient()

    #     self.test_client = Client.objects.create(name="django")
    #     self.testuser1 = User.objects.create_user(username="test_user1", password="123456789")
    #     self.testuser2 = User.objects.create_superuser(username="test_user1", password="123456789")
    #     self.client.login(username=self.testuser1.username, password="123456789")
