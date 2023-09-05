from django.db import models

from ..employees.models import Employee


class Notification(models.Model):
    notif_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    link = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee} : {self.content}"
