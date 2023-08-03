from django.test import TestCase
from django.contrib.auth import get_user_model
from .CRUDpermissions import get_permissions_for_model, add_permissions_to_dict
from ..models import Worksite, Employee

User = get_user_model()


class PermissionsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.worksite = Worksite.objects.create(name="Test Worksite")
        self.employee = Employee.objects.create(user=self.user, position="director")

    def test_generate_permissions(self):
        model_permissions = get_permissions_for_model(Worksite)
        permissions_dict = {}
        add_permissions_to_dict(model_permissions, permissions_dict)

        self.assertEqual(permissions_dict["WorksiteCreateObject"], False)
        self.assertEqual(permissions_dict["WorksiteViewList"], False)
        self.assertEqual(permissions_dict["WorksiteRetrieveObject"], False)
        self.assertEqual(permissions_dict["WorksiteUpdateObject"], False)
        self.assertEqual(permissions_dict["WorksiteDeleteObject"], False)

    def test_permissions_for_employee(self):
        employee_permissions = self.employee.get_permissions()

        self.assertEqual(employee_permissions["WorksiteCreateObject"], False)
        self.assertEqual(employee_permissions["WorksiteViewList"], False)
        self.assertEqual(employee_permissions["WorksiteRetrieveObject"], False)
        self.assertEqual(employee_permissions["WorksiteUpdateObject"], False)
        self.assertEqual(employee_permissions["WorksiteDeleteObject"], False)
