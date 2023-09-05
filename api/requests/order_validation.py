from .selectors import order_lines_get_list
from ..notifications.services import create_notification_for_employees, create_notification_for_worksite
from ..managements.selectors import get_validators
from ..deliveries.models import Delivery
from ..deliveries.services import delivery_line_create, send_delivery_scheduled_notification
from ..deliveries.serializers import DeliveryInputSerializer


def get_next_validation(order):
    """Renvoie le seuil de validation requis à l'instant t"""
    current_threshold = order.threshold
    current_validation = order.validation
    if current_threshold == 0:
        return None
    elif current_threshold <= current_validation:
        return None
    elif current_validation == 0:
        next_validation = 1
    else:
        next_validation = current_threshold

    return next_validation


def get_next_validator(order, validation_threshold):
    worksite_validators = get_validators(order.worksite.worksite_id)
    print("chantier :", worksite_validators)
    validators = None

    if validation_threshold == 1:
        validators = worksite_validators.filter(threshold=1)
        print("1 :", validators)
    elif validation_threshold == 2 or (validation_threshold == 1 and not validators):
        validators = worksite_validators.filter(threshold=2)
        print("2 :", validators)
    elif validation_threshold == 3 or (validation_threshold == 2 and not validators):
        validators = worksite_validators.filter(threshold=3)
        print("3 :", validators)

    return validators


def send_creation_notification(order, employee):
    notif_message = f"Commande n°{order.order_id} créée avec succès pour le chantier: {order.worksite.name} - {order.worksite.city}"
    notif_link = f"/request/order/{order.order_id}"
    employees_ids = [employee.employee_id]
    create_notification_for_employees(employees_ids=employees_ids, content=notif_message, link=notif_link)


def send_validation_notification(order, validation_number):
    validators = get_next_validator(order, validation_number)
    print("valideurs :", validators)
    validators_id = list(map(lambda employee: employee.employee_id, validators))
    notif_message = f"Vous avez une commande à valider pour le chantier: {order.worksite.name} - {order.worksite.city}"
    notif_link = f"/request/order/{order.order_id}"
    create_notification_for_employees(employees_ids=validators_id, content=notif_message, link=notif_link)


def send_success_notification(order, employee):
    notif_message = f"Commande validée par {employee.first_name} et envoyée pour le chantier: {order.worksite.name} - {order.worksite.city}"
    notif_link = f"/request/order/{order.order_id}"
    create_notification_for_worksite(worksite_id=order.worksite.worksite_id, content=notif_message, link=notif_link)


def order_validate(order, employee):
    """Validation de la commande par l'employé.
    Si la commande est créée par un employé n'ayant pas d'autorisation, les premiers valideurs doivent valider avant diffusion.
    Si l'employé a un seuil de validation supérieur au seuil de la commande, la commande est validée.
    A l'inverse, la commande est envoyée au bon valideur"""
    order_threshold = order.threshold
    employee_threshold = employee.threshold
    validation = order.validation

    # Si la commande est créée sans autorisation, elle passe obligatoirement par les plus bas valideur
    if employee_threshold == 0:
        order.status = "validation"
        order.save()
        send_validation_notification(order, 1)
        return order

    # Si l'employé peut valider la commande, on envoie la commande ainsi qu'une notif de succès:
    if validation <= employee_threshold and employee_threshold >= order_threshold:
        order.validation = employee_threshold
        order.status = "send"
        order.save()
        send_success_notification(order, employee)
        return order

    # Si l'employé ne peut pas valider, alors on envoie une notif aux bons valideurs
    elif order_threshold > employee_threshold:
        order.validation = employee_threshold
        order.status = "validation"
        order.save()
        send_validation_notification(order, order_threshold)
        return order


def order_confirm(order):
    order.status = "confirmed"
    order.save()
    delivery_data = {}
    delivery_data["order"] = order.order_id
    delivery_data["worksite"] = order.worksite.worksite_id
    delivery_data["expected_date_time"] = order.date_time
    serializer = DeliveryInputSerializer(data=delivery_data)
    if serializer.is_valid():
        delivery = Delivery.objects.create(
            order=serializer.validated_data["order"],
            worksite=serializer.validated_data["worksite"],
            expected_date_time=serializer.validated_data["expected_date_time"],
        )
        order_lines = order_lines_get_list(order.order_id)
        delivery_lines = []
        if delivery is not None:
            for order_line in order_lines:
                delivery_line = delivery_line_create(delivery=delivery, order_line=order_line)
                delivery_lines.append(delivery_line)
            if len(delivery_lines) > 0:
                send_delivery_scheduled_notification(delivery)
                return True
            else:
                return False
        else:
            return False
    else:
        return False
