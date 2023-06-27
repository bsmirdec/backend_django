from django.contrib import admin
from .models import Client, Worksite, SiteDirector, SiteSupervisor, SiteForeman, Management, Administrator


class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class SiteSupervisorAdmin(admin.ModelAdmin):
    list_display = ("user_id", "__str__")


class SiteDirectorAdmin(admin.ModelAdmin):
    list_display = ("user_id", "__str__")


class SiteForemanAdmin(admin.ModelAdmin):
    list_display = ("user_id", "__str__")


class ManagementAdmin(admin.ModelAdmin):
    list_display = ("user_id", "__str__")


admin.site.register(Client, ClientAdmin)
admin.site.register(Worksite)
admin.site.register(SiteDirector, SiteDirectorAdmin)
admin.site.register(SiteSupervisor, SiteSupervisorAdmin)
admin.site.register(SiteForeman, SiteForemanAdmin)
admin.site.register(Management, ManagementAdmin)
admin.site.register(Administrator)
