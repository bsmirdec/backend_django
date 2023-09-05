from .models import Notification
from ..employees.models import Employee
from ..managements.selectors import get_employee_for_worksite


def create_notification_for_employees(employees_ids, content, link):
    created_notifications = []

    for employee_id in employees_ids:
        notification = create_notification(employee_id, content, link)
        if notification:
            created_notifications.append(notification)

    return created_notifications


def create_notification(employee_id, content, link):
    try:
        employee = Employee.objects.filter(employee_id=employee_id).first()
        notification = Notification.objects.create(employee=employee, content=content, link=link)
        print("notification créée")
        return notification

    except Employee.DoesNotExist:
        return None

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return None


def create_notification_for_worksite(worksite_id, content, link):
    employees = get_employee_for_worksite(worksite_id)
    employees_ids = []
    for employee in employees:
        employees_ids.append(employee.employee_id)
    created_notifications = create_notification_for_employees(employees_ids, content, link)
    return created_notifications


def delete_notification(notification):
    notification.delete()


def notification_is_read(notification):
    notification.is_read = True
    notification.save()
    return notification
