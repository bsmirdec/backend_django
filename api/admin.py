from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .worksites.models import Worksite
from .employees.models import Employee


admin.site.register(Worksite)
admin.site.register(Employee)
