import json
from django.db import models

from ..models import BaseModel


class Category(BaseModel):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    types = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    def set_types(self, types_list):
        self.permissions = json.dumps(types_list)

    def get_types(self):
        if self.types:
            return json.loads(self.types)
        else:
            return []


class Product(BaseModel):
    product_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=50, choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_type_choices()

    def _set_type_choices(self):
        if self.category:
            category_types = self.category.types.split(",")
            self._meta.get_field("type").choices = [(t, t) for t in category_types]
