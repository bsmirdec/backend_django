from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth import get_user_model


User = get_user_model()


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

    objects = models.Manager()
    newobjects = NewWorksite()

    class Meta:
        ordering = ["-started"]

    def __str__(self):
        return f"{self.city} - {self.name}"


class WorkingPosition(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, primary_key=True)

    class Meta:
        abstract = True


class Administrator(WorkingPosition):
    def __str__(self):
        return f"Administrateur: {self.user}"


class SiteDirector(WorkingPosition):
    def __str__(self):
        return f"Directeur Travaux: {self.user}"


class SiteSupervisor(WorkingPosition):
    responsable = models.ForeignKey(SiteDirector, verbose_name=("responsable"), on_delete=models.CASCADE)

    def __str__(self):
        return f"Conducteur Travaux: {self.user}"


class SiteForeman(WorkingPosition):
    responsable = models.ForeignKey(SiteDirector, verbose_name=("responsable"), on_delete=models.CASCADE)

    def __str__(self):
        return f"Chef Chantier: {self.user}"


class Management(models.Model):
    worksite = models.ForeignKey(Worksite, on_delete=models.DO_NOTHING)
    staff_type = models.CharField(
        max_length=20,
        choices=(
            ("director", "Director"),
            ("supervisor", "Supervisor"),
            ("foreman", "Foreman"),
        ),
        default="foreman",
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def get_staff(self):
        if self.staff_type == "director":
            return SiteDirector.objects.filter(user=self.user).first()
        elif self.staff_type == "supervisor":
            return SiteSupervisor.objects.filter(user=self.user).first()
        elif self.staff_type == "foreman":
            return SiteForeman.objects.filter(user=self.user).first()

    def set_staff(self, staff):
        if isinstance(staff, SiteDirector):
            self.staff_type = "director"
        elif isinstance(staff, SiteSupervisor):
            self.staff_type = "supervisor"
        elif isinstance(staff, SiteForeman):
            self.staff_type = "foreman"
        else:
            raise ValueError("Invalid staff type")
        self.user = staff.user

    staff = property(get_staff, set_staff)

    def __str__(self):
        return f"{self.staff} est affecté à {self.worksite}"
