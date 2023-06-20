from django.db import models
from django.db.models.query import QuerySet


class Client(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Worksite(models.Model):
    class NewWorksite(models.Manager):
        def get_queryset(self) -> QuerySet:
            return super().get_queryset().filter(status=("etudes"))

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
    name = models.CharField(max_length=50)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    city = models.CharField(max_length=50)
    adress = models.CharField(max_length=200)
    started = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=status_options, default="etudes")
    # members = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Management")

    objects = models.Manager()
    newobjects = NewWorksite()

    class Meta:
        ordering = ["-started"]

    def __str__(self):
        return f"{self.city} - {self.name}"


# class Management(models.Model):
#     site_director = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
#     site_supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
#     site_foreman = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
#     worksite = models.ForeignKey(Worksite, on_delete=models.DO_NOTHING)
