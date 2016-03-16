from django.contrib import admin

from .models import Guide, Zone, Manifest, Observations

# Register your models here.

admin.site.register(Zone)
admin.site.register(Guide)
admin.site.register(Manifest)
admin.site.register(Observations)
