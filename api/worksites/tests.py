from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError
from datetime import date
from .models import Worksite


class WorksiteModelTests(TestCase):
    def setUp(self):
        self.worksite_data = {
            "sector": "GO",
            "name": "Example Worksite",
            "address": "Example Address",
            "postal_code": 12345,
            "city": "Example City",
            "started": date(2023, 7, 1),
            "finished": date(2023, 7, 31),
            "status": "etudes",
        }
        self.worksite = Worksite.objects.create(**self.worksite_data)

    def test_worksite_str_representation(self):
        self.assertEqual(str(self.worksite), "Example City - Example Worksite")

    def test_clean_dates_valid(self):
        # Vérifiez si aucune erreur de validation n'est levée pour les dates valides
        worksite_data = {
            "sector": "GO",
            "name": "Valid Worksite",
            "address": "Example Address",
            "postal_code": 12345,
            "city": "Example City",
            "started": date(2023, 7, 1),
            "finished": date(2023, 7, 31),
            "status": "etudes",
        }
        worksite = Worksite(**worksite_data)
        worksite.full_clean()  # Lève une exception ValidationError si une erreur est trouvée

    def test_clean_dates_invalid(self):
        # Vérifiez si une exception ValidationError est levée pour les dates invalides
        worksite_data = {
            "sector": "GO",
            "name": "Invalid Worksite",
            "address": "Example Address",
            "postal_code": 12345,
            "city": "Example City",
            "started": date(2023, 8, 1),
            "finished": date(2023, 7, 31),  # La date de début est postérieure à la date de fin
            "status": "etudes",
        }
        worksite = Worksite(**worksite_data)
        with self.assertRaises(ValidationError) as context:
            worksite.full_clean()

        self.assertIn("__all__", str(context.exception))
        self.assertEqual(context.exception.message_dict["__all__"][0], "La date de début ne peut pas être postérieure à la date de fin.")

    def test_clean_status_terminated_without_finished_date(self):
        # Vérifiez si une exception ValidationError est levée lorsque le statut est 'Terminé' sans date de fin
        worksite_data = {
            "sector": "GO",
            "name": "Terminated Worksite",
            "address": "Example Address",
            "postal_code": 12345,
            "city": "Example City",
            "started": date(2023, 7, 1),
            "status": "termine",  # Statut 'Terminé' sans date de fin
        }
        worksite = Worksite(**worksite_data)
        with self.assertRaises(ValidationError) as context:
            worksite.full_clean()

        self.assertIn("__all__", str(context.exception))
        self.assertEqual(context.exception.message_dict["__all__"][0], "Le statut 'Terminé' nécessite une date de fin spécifiée.")

    def test_clean_postal_code_valid(self):
        # Vérifiez si aucune erreur de validation n'est levée pour un code postal valide
        worksite_data = {
            "sector": "GO",
            "name": "Postal Code Test",
            "address": "Example Address",
            "postal_code": 54321,  # Code postal valide (5 chiffres)
            "city": "Example City",
            "started": date(2023, 7, 1),
            "finished": date(2023, 7, 31),
            "status": "etudes",
        }
        worksite = Worksite(**worksite_data)
        worksite.full_clean()  # Lève une exception ValidationError si une erreur est trouvée

    def test_clean_postal_code_invalid(self):
        # Vérifiez si une exception ValidationError est levée pour un code postal invalide
        worksite_data = {
            "sector": "GO",
            "name": "Postal Code Test",
            "address": "Example Address",
            "postal_code": 5432,  # Code postal invalide (moins de 5 chiffres)
            "city": "Example City",
            "started": date(2023, 7, 1),
            "finished": date(2023, 7, 31),
            "status": "etudes",
        }
        worksite = Worksite(**worksite_data)
        with self.assertRaises(ValidationError) as context:
            worksite.full_clean()

        self.assertIn("__all__", str(context.exception))
        self.assertEqual(context.exception.message_dict["__all__"][0], "Le code postal doit contenir exactement 5 chiffres.")

        worksite_data = {
            "sector": "GO",
            "name": "Postal Code Test",
            "address": "Example Address",
            "postal_code": "ABCDE",  # Code postal invalide (lettres au lieu de chiffres)
            "city": "Example City",
            "started": date(2023, 7, 1),
            "finished": date(2023, 7, 31),
            "status": "etudes",
        }
        worksite = Worksite(**worksite_data)
        with self.assertRaises(ValidationError) as context:
            worksite.full_clean()

        self.assertIn("__all__", str(context.exception))
        self.assertEqual(context.exception.message_dict["__all__"][0], "Le code postal doit être composé de chiffres uniquement.")


class WorksiteViewsTests(APITestCase):
    def setUp(self):
        # Créez ici les données de test nécessaires pour les tests
        self.worksite_data = {
            "sector": "Example Sector",
            "name": "Example Worksite",
            "address": "Example Address",
            "postal_code": 12345,
            "city": "Example City",
            "started": "2023-07-01",
            "finished": "2023-07-31",
            "status": "In Progress",
        }
        self.worksite = Worksite.objects.create(**self.worksite_data)

    def test_list_worksites_with_permission(self):
        url = reverse("worksites")  # Assurez-vous que "worksite-list" est le nom de l'URL pour la vue WorksiteViewListAPI
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_worksites_without_permission(self):
        url = reverse("worksites")
        # Effectuez une demande sans authentification pour tester le refus de la permission
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Testez également les autres vues en fonction de la présence ou de l'absence de permission

    def test_retrieve_worksite_with_permission(self):
        # ...
        pass

    def test_retrieve_worksite_without_permission(self):
        # ...
        pass

    def test_create_worksite_with_permission(self):
        # ...
        pass

    def test_create_worksite_without_permission(self):
        # ...
        pass

    def test_update_worksite_with_permission(self):
        # ...
        pass

    def test_update_worksite_without_permission(self):
        # ...
        pass

    def test_delete_worksite_with_permission(self):
        # ...
        pass

    def test_delete_worksite_without_permission(self):
        # ...
        pass
