from django.contrib import admin

from .models import Client, Driver, Employee

# Register your models here.

admin.site.register(Client)
admin.site.register(Driver)
admin.site.register(Employee)
