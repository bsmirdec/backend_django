from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Employee


class EmployeeModelTests(TestCase):
    def setUp(self):
        self.employee_data = {
            "first_name": "John",
            "last_name": "Doe",
            "position": "site_foreman",
        }
        self.employee = Employee.objects.create(**self.employee_data)

    def test_employee_str_representation(self):
        self.assertEqual(str(self.employee), "John Doe site_foreman")

    def test_set_permissions(self):
        permission_list = {
            "employee_create_object": False,
            "employee_view_list": False,
            "employee_retrieve_object": True,
            "employee_update_object": True,
            "employee_delete_object": False,
            "worksite_create_object": False,
            "worksite_view_list": False,
            "worksite_retrieve_object": True,
            "worksite_update_object": False,
            "worksite_delete_object": False,
            "worksiteemployee_create_object": False,
            "worksiteemployee_view_list": False,
            "worksiteemployee_retrieve_object": True,
            "worksiteemployee_update_object": False,
            "worksiteemployee_delete_object": False,
        }
        self.employee.set_permissions(permission_list)
        self.employee.save()
        employee = Employee.objects.get(pk=self.employee.pk)
        self.assertEqual(employee.get_permissions(), permission_list)

    def test_set_permissions_empty(self):
        permissions = self.employee.set_permissions({})
        self.assertEqual(permissions, None)

    def test_get_permissions_not_empty(self):
        permission_list = {
            "employee_create_object": False,
            "employee_view_list": False,
            "employee_retrieve_object": True,
            "employee_update_object": True,
            "employee_delete_object": False,
            "worksite_create_object": False,
            "worksite_view_list": False,
            "worksite_retrieve_object": True,
            "worksite_update_object": False,
            "worksite_delete_object": False,
            "worksiteemployee_create_object": False,
            "worksiteemployee_view_list": False,
            "worksiteemployee_retrieve_object": True,
            "worksiteemployee_update_object": False,
            "worksiteemployee_delete_object": False,
        }
        self.employee.set_permissions(permission_list)
        self.employee.save()
        permissions = self.employee.get_permissions()
        self.assertEqual(permissions, permission_list)

    def test_has_permission_true(self):
        permission_list = {
            "employee_create_object": False,
            "employee_view_list": False,
            "employee_retrieve_object": True,
            "employee_update_object": True,
            "employee_delete_object": False,
            "worksite_create_object": False,
            "worksite_view_list": False,
            "worksite_retrieve_object": True,
            "worksite_update_object": False,
            "worksite_delete_object": False,
            "worksiteemployee_create_object": False,
            "worksiteemployee_view_list": False,
            "worksiteemployee_retrieve_object": True,
            "worksiteemployee_update_object": False,
            "worksiteemployee_delete_object": False,
        }
        self.employee.set_permissions(permission_list)
        self.employee.save()
        has_permission = self.employee.has_permission("employee_retrieve_object")
        self.assertTrue(has_permission)

    def test_has_permission_false(self):
        permission_list = {
            "employee_create_object": False,
            "employee_view_list": False,
            "employee_retrieve_object": True,
            "employee_update_object": True,
            "employee_delete_object": False,
            "worksite_create_object": False,
            "worksite_view_list": False,
            "worksite_retrieve_object": True,
            "worksite_update_object": False,
            "worksite_delete_object": False,
            "worksiteemployee_create_object": False,
            "worksiteemployee_view_list": False,
            "worksiteemployee_retrieve_object": True,
            "worksiteemployee_update_object": False,
            "worksiteemployee_delete_object": False,
        }
        self.employee.set_permissions(permission_list)
        self.employee.save()
        has_permission = self.employee.has_permission("worksiteemployee_delete_object")
        self.assertFalse(has_permission)

    def test_set_default_permissions(self):
        expected_permissions = {
            "employee_create_object": False,
            "employee_view_list": False,
            "employee_retrieve_object": True,
            "employee_update_object": True,
            "employee_delete_object": False,
            "worksite_create_object": False,
            "worksite_view_list": False,
            "worksite_retrieve_object": True,
            "worksite_update_object": False,
            "worksite_delete_object": False,
            "worksiteemployee_create_object": False,
            "worksiteemployee_view_list": False,
            "worksiteemployee_retrieve_object": True,
            "worksiteemployee_update_object": False,
            "worksiteemployee_delete_object": False,
        }
        self.employee.set_default_permissions()
        self.employee.save()
        employee = Employee.objects.get(pk=self.employee.pk)
        self.assertEqual(employee.get_permissions(), expected_permissions)


class EmployeeViewsTests(APITestCase):
    def setUp(self):
        self.employee_data = {
            "first_name": "TestName",
            "last_name": "TestName",
            "position": "site_director",
            "is_current": True,
            "manager": 1,
            "permissions": "",
        }
        self.employee = Employee.objects.create(**self.employee_data)

    def test_list_employees_with_permission(self):
        url = reverse("employees")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_employees_without_permission(self):
        url = reverse("employees")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_employee_with_permission(self):
        # ...
        pass

    def test_retrieve_employee_without_permission(self):
        # ...
        pass

    def test_create_employee_with_permission(self):
        # ...
        pass

    def test_create_employee_without_permission(self):
        # ...
        pass

    def test_update_employee_with_permission(self):
        # ...
        pass

    def test_update_employee_without_permission(self):
        # ...
        pass

    def test_delete_employee_with_permission(self):
        # ...
        pass

    def test_delete_employee_without_permission(self):
        # ...
        pass
