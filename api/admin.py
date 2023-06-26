from django.contrib import admin
from .models import Client, Worksite, SiteDirector, SiteSupervisor, SiteForeman, Management

admin.site.register(Client)
admin.site.register(Worksite)
admin.site.register(SiteDirector)
admin.site.register(SiteSupervisor)
admin.site.register(SiteForeman)
admin.site.register(Management)
