from .models import Order, OrderLine

from ..employees.selectors import employee_get
from .serializers import OrderLineInputSerializer, OrderLineOutputSerializer
from .selectors import order_lines_get_list
from .order_validation import order_validate, send_creation_notification


def order_create(validated_data, employee_id):
    order = Order(**validated_data)
    employee = employee_get(employee_id)
    # validation de la commande
    order_validate(order, employee)
    send_creation_notification(order, employee)
    return order


def order_lines_create(order_lines_data, order_id):
    order_lines_instance = []
    for order_line in order_lines_data:
        order_line["product"] = order_line["product"]["product_id"]
        order_line["order"] = order_id
        order_line_serializer = OrderLineInputSerializer(data=order_line)
        if order_line_serializer.is_valid():
            order_line_instance = OrderLine.objects.create(
                product=order_line_serializer.validated_data["product"],
                quantity=order_line_serializer.validated_data["quantity"],
                order=order_line_serializer.validated_data["order"],
            )
            order_line_data = OrderLineOutputSerializer(order_line_instance).data
            order_lines_instance.append(order_line_data)
        else:
            return None
    return order_lines_instance


def retour_create():
    pass


def order_update(order, data, employee_id):
    for key, value in data.items():
        setattr(order, key, value)
    # Récupérer l'étape de validation
    employee = employee_get(employee_id)
    # validation de la commande
    order_validate(order, employee)
    return order


def retour_update():
    pass


def order_delete(order):
    order.delete()


def retour_delete():
    pass


def order_lines_delete(order_id):
    order_lines = order_lines_get_list(order_id=order_id)
    order_lines.delete()
    return True
