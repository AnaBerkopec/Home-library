from django.contrib import admin

from .models import Lokacija, Knjiga, Izposojeno

admin.site.register(Lokacija)
admin.site.register(Knjiga)
admin.site.register(Izposojeno)