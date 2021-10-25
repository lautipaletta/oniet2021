from django.contrib import admin
from .models import Provincia, Localidad, Barrio

# Register your models here.

admin.site.register(Provincia)
admin.site.register(Localidad)
admin.site.register(Barrio)