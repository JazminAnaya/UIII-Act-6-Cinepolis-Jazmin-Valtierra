# app_Cinepolis/admin.py
from django.contrib import admin
from .models import Sucursal, Sala, Pelicula, Funcion, Cliente, Transaccion # Importa todos los modelos

# Registra tus modelos aquí
admin.site.register(Sucursal)
admin.site.register(Sala)
admin.site.register(Pelicula)
admin.site.register(Funcion) # ¡Registra Funcion!
admin.site.register(Cliente) # ¡Registra Cliente!
admin.site.register(Transaccion) # ¡Registra Transaccion!