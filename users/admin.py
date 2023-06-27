from django.contrib import admin
from users.models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea
from django.db import models


class UserAdminConfig(UserAdmin):
    model = CustomUser
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("email", "first_name", "last_name", "is_active", "is_staff")
    ordering = ("last_name",)
    list_display = ("id", "email", "first_name", "last_name", "is_active", "is_staff")
    fieldsets = (
        (None, {"fields": ("email", "first_name", "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 20, "cols": 60})},
    }
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "first_name", "last_name", "password1", "password2", "is_active", "is_staff")}),
    )


admin.site.register(CustomUser, UserAdminConfig)
