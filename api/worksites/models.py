from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from ..models import BaseModel

User = get_user_model()


class Worksite(BaseModel):
    status_options = (
        ("etudes", "Etudes"),
        ("gros_oeuvre", "Gros Oeuvre"),
        ("tous_corps_detat", "Tous Corps D'Etat"),
        ("finitions", "Finitions"),
        ("termine", "Terminé"),
    )
    sector_options = (("GO", "Gros Oeuvre"), ("TCE", "Tout Corps D'état"))

    worksite_id = models.AutoField(primary_key=True)
    sector = models.CharField(max_length=20, choices=sector_options, default="GO")
    client = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200, blank=False, null=False)
    postal_code = models.IntegerField(blank=False, null=False)
    city = models.CharField(max_length=50, blank=False, null=False)
    started = models.DateField(null=True, blank=True)
    finished = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=status_options, default="etudes", blank=False, null=False)

    objects = models.Manager()

    class Meta:
        ordering = ["-started"]

    def __str__(self):
        return f"{self.city} - {self.name}"

    def clean(self):
        print("Running custom clean() method...")
        super().clean()
        if self.started and self.finished:
            if self.started > self.finished:
                raise ValidationError("La date de début ne peut pas être postérieure à la date de fin.")
        if self.status == "termine" and not self.finished:
            raise ValidationError("Le statut 'Terminé' nécessite une date de fin spécifiée.")
        if self.postal_code is not None:
            postal_code_str = str(self.postal_code)
            if len(postal_code_str) != 5:
                raise ValidationError("Le code postal doit contenir exactement 5 chiffres.")
            if not postal_code_str.isdigit():
                raise ValidationError("Le code postal doit être composé de chiffres uniquement.")
        print("Custom clean() method completed successfully.")


class WorksiteLimitation(BaseModel):
    pass


class WortksiteStock(models.Model):
    pass
