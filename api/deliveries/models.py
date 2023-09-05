from django.db import models

from ..models import BaseModel
from ..requests.models import Order
from ..products.models import Product
from ..worksites.models import Worksite


class Delivery(BaseModel):
    status_options = (
        ("scheduled", "planifiée"),
        ("delayed", "retard"),
        ("loading", "chargement"),
        ("ongoing", "en routes"),
        ("unloading", "déchargement"),
        ("completed", "terminée"),
        ("uncompleted", "incomplète"),
        ("canceled", "annulée"),
        ("failure", "échec"),
    )

    delivery_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False)
    worksite = models.ForeignKey(Worksite, on_delete=models.CASCADE, null=False)
    expected_date_time = models.DateTimeField(null=False)
    real_date_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=50, choices=status_options, default="scheduled")


class DeliveryLine(models.Model):
    delivery_line_id = models.AutoField(primary_key=True)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
