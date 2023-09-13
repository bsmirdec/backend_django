from django.db import models

from ..models import BaseModel
from ..products.models import Product
from ..worksites.models import Worksite


class WarehouseStock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.product}: {self.quantity}"

    def get_total_quantity(self):
        return self.quantity * self.product.packaging


class BaseStock(BaseModel):
    worksite = models.ForeignKey(Worksite, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        abstract = True

    def get_total_quantity(self):
        return self.quantity * self.product.packaging


class Stock(BaseStock):
    stock_id = models.AutoField(primary_key=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["worksite", "product"], name="unique_stock")]

    def __str__(self) -> str:
        return f"Chantier: {self.worksite} - {self.product} : {self.quantity}"


class WorksiteMaxStock(BaseStock):
    max_stock_id = models.AutoField(primary_key=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["worksite", "product"], name="unique_max_stock")]

    def __str__(self) -> str:
        return f"Chantier: {self.worksite} - Produit: {self.product} - Quantité Max: {self.quantity}"
