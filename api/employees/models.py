import json
from django.db import models

from ..models import BaseModel
from ..permissions.PERMISSIONS_BY_POSITION import PERMISSIONS_BY_POSITION


class Employee(BaseModel):
    positions_options = (
        ("administrator", "Administrateur"),
        ("director", "Directeur"),
        ("studies", "Responsable études"),
        ("site_director", "Directeur de Travaux"),
        ("site_supervisor", "Conducteur de Travaux"),
        ("site_foreman", "Chef de chantier"),
    )

    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=50, choices=positions_options, default="site_foreman")
    is_current = models.BooleanField(default=True)
    manager = models.ForeignKey("self", related_name="staff", on_delete=models.DO_NOTHING, blank=True, null=True)
    permissions = models.JSONField(blank=True, null=True)

    def set_permissions(self, permission_dict):
        if permission_dict:
            self.permissions = json.dumps(permission_dict)
        else:
            self.permissions = json.dumps({})

    def get_permissions(self):
        if self.permissions:
            try:
                return json.loads(self.permissions)
            except json.JSONDecodeError:
                return {}
        else:
            return {}

    def has_permission(self, permission_name):
        permissions = self.get_permissions()
        return permissions.get(permission_name, False)

    def set_default_permissions(self):
        """Permissions par défaut correspondantes au poste associé"""
        position_permissions = PERMISSIONS_BY_POSITION.get(self.position, {})
        self.permissions = json.dumps(position_permissions)

    def set_inactive(self):
        """Rendre l'employé inactif, ainsi que l'user"""
        pass

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.position}"

    def save(self, *args, **kwargs):
        if not self.permissions:
            self.set_default_permissions()

        super().save(*args, **kwargs)
