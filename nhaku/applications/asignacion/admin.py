from django.contrib import admin
from .models import Car, Asignation, DetailAsignation

# Register your models here.

admin.site.register(Car)
admin.site.register(Asignation)
admin.site.register(DetailAsignation)
