from django.db.models import Q
from .models import Order, OrderLine
from ..products.models import Type
from ..managements.selectors import get_worksite_for_employee


def get_threshold_for_order(order_lines_data):
    highest_threshold = 0
    types_list = [line_data["product"]["type"]["type_id"] for line_data in order_lines_data]

    for type_id in types_list:
        try:
            type_instance = Type.objects.get(pk=type_id)
            if type_instance.threshold > highest_threshold:
                highest_threshold = type_instance.threshold
        except Type.DoesNotExist:
            pass

    return highest_threshold


def order_get_list(employee_id):
    worksites = get_worksite_for_employee(employee_id)
    worksite_ids = [worksite.worksite_id for worksite in worksites]
    orders = Order.objects.filter(Q(worksite_id__in=worksite_ids))
    return orders


def order_lines_get_list(order_id):
    order_lines = OrderLine.objects.filter(order=order_id)
    return order_lines


def order_get_object(order_id):
    try:
        order = Order.objects.get(pk=order_id)
        return order
    except Order.DoesNotExist:
        return None


def retour_get_list():
    pass


def retour_get_object():
    pass
