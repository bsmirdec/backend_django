from django.db.models import Q

from .models import Delivery, DeliveryLine

from ..managements.selectors import get_worksite_for_employee


def delivery_get_object(delivery_id):
    try:
        delivery = Delivery.objects.get(pk=delivery_id)
        return delivery
    except Delivery.DoesNotExist:
        return None


def deliveries_get_list(employee_id):
    worksites = get_worksite_for_employee(employee_id)
    worksite_ids = [worksite.worksite_id for worksite in worksites]
    deliveries = Delivery.objects.filter(Q(worksite_id__in=worksite_ids))
    return deliveries


def delivery_lines_get_list(delivery_id):
    delivery_lines = DeliveryLine.objects.filter(delivery=delivery_id)
    return delivery_lines
