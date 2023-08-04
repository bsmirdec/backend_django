from django.core.exceptions import ObjectDoesNotExist

from ..models import CustomUser
from api.employees.models import Employee


def user_list():
    return CustomUser.objects.all()


def user_get(pk):
    try:
        user = CustomUser.objects.get(pk=pk)
        return user
    except CustomUser.DoesNotExist:
        raise ObjectDoesNotExist


def user_get_employee(pk):
    """Récupération de l'employé. Cependant, si la fusion n'est pas validée,
    l'utilisateur ne peut pas récupérer ses informations, et donc ses permissions"""
    user = user_get(pk)
    if user.is_validated:  # La fusion est-elle validée par un admin ?
        if user.employee is not None:
            return user.employee
    else:  # Sans validation, pas possible de récupérer son compte salarié
        return None


def user_get_permissions(pk):
    try:
        employee = user_get_employee(pk)
        if employee is not None:
            permissions = employee.get_permissions()
            return permissions
        else:
            return "La fusion n'est pas encore validée"
    except Employee.DoesNotExist:
        raise ObjectDoesNotExist
    except CustomUser.DoesNotExist:
        raise ObjectDoesNotExist
