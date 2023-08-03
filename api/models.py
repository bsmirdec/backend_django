from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Client(BaseModel):
    name = models.CharField(unique=True, max_length=50)

    def __str__(self) -> str:
        return self.name
