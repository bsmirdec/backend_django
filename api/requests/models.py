from django.db import models
from django.utils import timezone

from ..models import BaseModel
from ..worksites.models import Worksite
from ..products.models import Product


class Request(BaseModel):
    status_options = (("edition", "édition"), ("validation", "en validation"), ("send", "envoyée"), ("confirmed", "confirmé"), ("refused", "refusée"))

    worksite = models.ForeignKey(Worksite, on_delete=models.CASCADE, null=True)
    date_time = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=1))
    threshold = models.IntegerField(default=0)
    validation = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=status_options, default="edition")

    class Meta:
        abstract = True


class Order(Request):
    order_id = models.AutoField(primary_key=True)

    def __str__(self) -> str:
        return f"Commande n°{self.order_id} - chantier {self.worksite}"


class Retour(Request):
    retour_id = models.AutoField(primary_key=True)

    def __str__(self) -> str:
        return f"Retour n°{self.retour_id} - chantier {self.worksite}"


class RequestLine(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        abstract = True


class OrderLine(RequestLine):
    order_line_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["order", "product"]

    def __str__(self):
        return f"Commande n°{self.order} : {self.product} - {self.quantity}"


class RetourLine(RequestLine):
    retour = models.ForeignKey(Retour, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["retour", "product"]
