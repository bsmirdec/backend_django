from .models import Employee


def employee_list(user):
    user.get
    return Employee.objects.all()


def employee_get(pk):
    try:
        employee = Employee.objects.get(pk=pk)
        return employee
    except Employee.DoesNotExist:
        return None


def get_staff_for_manager(self, manager):
    employees = Employee.objects.filter(manager=manager)
    return employees
