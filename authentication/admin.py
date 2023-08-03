from django.contrib import admin
from authentication.users.models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea
from django.db import models


class UserAdminConfig(UserAdmin):
    model = CustomUser
    search_fields = (
        "user_id",
        "email",
        "employee",
    )
    list_filter = ("email", "employee", "is_active", "is_staff")
    ordering = ("user_id",)
    list_display = ("user_id", "email", "is_active", "is_staff")
    fieldsets = (
        (None, {"fields": ("email",)}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
        ("Informations", {"fields": ("employee", "is_validated")}),
    )
    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 20, "cols": 60})},
    }
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "password1", "password2", "is_active", "is_staff")}),)


admin.site.register(CustomUser, UserAdminConfig)
