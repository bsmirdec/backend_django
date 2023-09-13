from .models import Delivery, DeliveryLine
from .serializers import DeliveryLineInputSerializer, DeliveryLineOutputSerializer
from .selectors import delivery_lines_get_list

from ..notifications.services import create_notification_for_worksite
from ..stocks.services import stock_create


def send_delivery_scheduled_notification(delivery):
    if delivery.status == "scheduled":
        notif_message = f"Livraison planifiée pour la {delivery.order}."
        create_notification_for_worksite(worksite_id=delivery.worksite.worksite_id, content=notif_message, link=f"/delivery/{delivery.delivery_id}")
        print("notif envoyée")
    else:
        return None


def send_delivery_status_notification(delivery):
    status = delivery.get_status_display()
    notif_message = f"Livraison en cours pour le chantier: {delivery.worksite.name} - {delivery.worksite.city}. Statut : {status}"
    create_notification_for_worksite(worksite_id=delivery.worksite.worksite_id, content=notif_message, link=f"/delivery/{delivery.delivery_id}")


def delivery_create(validated_data):
    delivery = Delivery(**validated_data)
    send_delivery_scheduled_notification(delivery)
    return delivery


def delivery_update(delivery, data):
    for key, value in data.items():
        setattr(delivery, key, value)
    delivery.save()
    return delivery


def delivery_confirm(delivery):
    delivery_lines_list = delivery_lines_get_list(delivery_id=delivery.delivery_id)
    print("delivery :", delivery)
    for delivery_line in delivery_lines_list:
        stock = stock_create(worksite=delivery.worksite.worksite_id, delivery_line=delivery_line)
        if not stock:
            return False
    send_delivery_status_notification(delivery)
    return True


def delivery_delete(delivery):
    delivery.delete()


def delivery_lines_create(delivery_lines_data, delivery_id):
    delivery_lines_instance = []
    for delivery_line in delivery_lines_data:
        product = delivery_line["product"]["product_id"]
        delivery_line["product"] = product
        delivery_line["order"] = delivery_id
        delivery_line_serializer = DeliveryLineInputSerializer(data=delivery_line)
        if delivery_line_serializer.is_valid():
            delivery_line_instance = DeliveryLine.objects.create(
                product=delivery_line_serializer.validated_data["product"],
                quantity=delivery_line_serializer.validated_data["quantity"],
                delivery=delivery_line_serializer.validated_data["delivery"],
            )
            delivery_line_data = DeliveryLineOutputSerializer(delivery_line_instance).data
            delivery_lines_instance.append(delivery_line_data)
        else:
            return None
    return delivery_lines_instance


def delivery_line_create(delivery, order_line):
    delivery_line = {}
    delivery_line["delivery"] = delivery.delivery_id
    delivery_line["product"] = order_line.product.product_id
    delivery_line["quantity"] = order_line.quantity
    delivery_line_serializer = DeliveryLineInputSerializer(data=delivery_line)
    if delivery_line_serializer.is_valid():
        delivery_line_instance = DeliveryLine.objects.create(**delivery_line_serializer.validated_data)
        if delivery_line_instance:
            return delivery_line_instance
        else:
            return None
    else:
        return None


def delivery_lines_delete(delivery_id):
    delivery_lines = delivery_lines_get_list(delivery_id=delivery_id)
    delivery_lines.delete()
    return True
