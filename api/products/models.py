from django.db import models

from ..models import BaseModel
from ..THRESHOLD_OPTIONS import THRESHOLD_OPTIONS


class Category(BaseModel):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Type(BaseModel):
    type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    threshold = models.IntegerField(choices=THRESHOLD_OPTIONS, default=0)

    def __str__(self):
        return f"{self.name}"


class Product(BaseModel):
    product_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    packaging = models.IntegerField()
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    length = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="api/products/images/")

    def __str__(self):
        return f"{self.name}"

    def package_weight(self):
        return self.packaging * self.weight
