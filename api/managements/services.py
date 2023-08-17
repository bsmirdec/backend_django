from django.db import IntegrityError
from rest_framework.exceptions import APIException
from rest_framework import status

from .models import Management

from ..worksites.models import Worksite
from ..employees.models import Employee


def management_create(worksite_id, employee_id):
    try:
        worksite = Worksite.objects.get(pk=worksite_id)
        employee = Employee.objects.get(pk=employee_id)

        try:
            management = Management.objects.create(worksite=worksite, employee=employee)
            return management
        except IntegrityError:
            raise APIException("Cet employé est déjà affecté au chantier.", code="management_already_exists")

    except Worksite.DoesNotExist:
        raise Worksite.DoesNotExist("Le chantier spécifié n'existe pas.")
    except Employee.DoesNotExist:
        raise Employee.DoesNotExist("L'employé spécifié n'existe pas.")


def management_delete(worksite_id, employee_id):
    try:
        worksite = Worksite.objects.get(pk=worksite_id)
        try:
            employee = Employee.objects.get(pk=employee_id)
            Management.objects.filter(worksite=worksite, employee=employee).delete()
        except Employee.DoesNotExist:
            return None
    except Worksite.DoesNotExist:
        return None
