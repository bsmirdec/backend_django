from django.contrib import admin
from . import models


@admin.register(models.Worksite)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("worksite_id", "name", "sector", "client", "city", "adress", "started", "status")


admin.site.register(models.Client)
