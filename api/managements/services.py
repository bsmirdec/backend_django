from django.db import IntegrityError

from .models import Management

from ..worksites.models import Worksite
from ..employees.models import Employee


class ManagementAlreadyExists(Exception):
    def __init__(self, message="Un gestionnaire pour ce chantier et cet employé existe déjà."):
        self.message = message
        super().__init__(self.message)


def management_create(worksite_id, employee_id):
    try:
        worksite = Worksite.objects.get(pk=worksite_id)
        employee = Employee.objects.get(pk=employee_id)

        try:
            management = Management.objects.create(worksite=worksite, employee=employee)
            return management
        except IntegrityError:
            raise ManagementAlreadyExists("Un gestionnaire pour ce chantier et cet employé existe déjà.")

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
