from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError

from api.employees.models import Employee


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError("Email obligatoire")
        if not password:
            raise ValueError("Mot de passe obligatoire")

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(_("email address"), unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)

    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, blank=True, null=True)
    is_validated = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"

    def full_clean(self, *args, **kwargs):
        super().full_clean(*args, **kwargs)

        if CustomUser.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            raise ValidationError("Cet e-mail est déjà utilisé par un autre utilisateur.")

        # if len(self.password) < 8:
        #     raise ValidationError("Le mot de passe doit contenir au moins 8 caractères.")

    def __str__(self):
        if self.employee:
            return str(self.employee)
        return self.email
