from .models import Notification

from authentication.users.selectors import user_get_employee


def get_notifications_for_user(user_id):
    try:
        employee = user_get_employee(pk=user_id)
        notifications = Notification.objects.filter(employee=employee.employee_id)

        return notifications

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return None


def get_notification(notif_id):
    try:
        notification = Notification.objects.get(notif_id=notif_id)
        return notification
    except Notification.DoesNotExist:
        return None
