from django.contrib import admin
from .models import Registrado, Silla, Multiplex, Pelicula, Sala, Proyeccion

# Register your models here.
admin.site.register(Multiplex)
admin.site.register(Pelicula)
admin.site.register(Sala)
admin.site.register(Proyeccion)
admin.site.register(Silla)
admin.site.register(Registrado)