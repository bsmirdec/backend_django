from django.db import models

from ..models import BaseModel
from ..employees.models import Employee
from ..worksites.models import Worksite


class Management(BaseModel):
    worksite = models.ForeignKey(Worksite, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["worksite", "employee"], name="unique_management")]

    def __str__(self):
        return f"Employé : {self.employee}, Chantier : {self.worksite}"
