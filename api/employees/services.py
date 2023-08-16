from .models import Employee


def employee_create(validated_data):
    employee = Employee(**validated_data)

    employee.save()

    return employee


def employee_update(pk, validated_data):
    employee = Employee.objects.get(pk=pk)
    for key, value in validated_data.items():
        setattr(employee, key, value)
    employee.save()
    return employee


def employee_delete(employee):
    employee.delete()
