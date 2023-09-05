from .services import send_delivery_status_notification


def delivery_loading(delivery):
    delivery.status = "loading"
    delivery.save()
    return delivery


def delivery_ongoing(delivery):
    delivery.status = "ongoing"
    delivery.save()
    send_delivery_status_notification(delivery)
    return delivery


def delivery_unloading(delivery):
    delivery.status = "unloading"
    delivery.save()
    return delivery


def delivery_completed(delivery):
    delivery.status = "completed"
    delivery.save()
    return delivery


def delivery_uncompleted(delivery):
    delivery.status = "uncompleted"
    delivery.save()
    return delivery


def delivery_delayed(delivery):
    delivery.status = "delayed"
    delivery.save()
    return delivery


def delivery_canceled(delivery):
    delivery.status = "canceled"
    delivery.save()
    send_delivery_status_notification(delivery)
    return delivery
