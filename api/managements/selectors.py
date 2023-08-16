from .models import Management

from ..worksites.models import Worksite
from ..employees.models import Employee

from ..employees.serializers import EmployeeOutputSerializer
from ..worksites.serializers import WorksiteOutputSerializer


def management_list():
    managements = Management.objects.all()
    return managements


def management_get(worksite_id, employee_id):
    try:
        worksite = Worksite.objects.get(pk=worksite_id)
        try:
            employee = Employee.objects.get(pk=employee_id)
            management = Management.objects.get(worksite=worksite, employee=employee)
            return management
        except Employee.DoesNotExist:
            return None
    except Worksite.DoesNotExist:
        return None


def get_worksite_for_employee(employee_id):
    try:
        worksites = Management.objects.filter(employee_id=employee_id).values("worksite")
        worksites_ids = [worksite["worksite"] for worksite in worksites]
        worksites_instances = Worksite.objects.filter(pk__in=worksites_ids)
        serialized_worksites = WorksiteOutputSerializer(worksites_instances, many=True).data
        return serialized_worksites
    except Employee.DoesNotExist:
        return None


def get_employee_for_worksite(worksite_id):
    try:
        employees = Management.objects.filter(worksite_id=worksite_id).values("employee")
        employee_ids = [employee["employee"] for employee in employees]
        employees_instances = Employee.objects.filter(pk__in=employee_ids)
        serialized_employees = EmployeeOutputSerializer(employees_instances, many=True).data
        return serialized_employees
    except Worksite.DoesNotExist:
        return None
