# app_Cinepolis/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_cinepolis, name='inicio_cinepolis'),

    # Rutas para Sucursales
    path('sucursales/agregar/', views.agregar_sucursal, name='agregar_sucursal'),
    path('sucursales/', views.ver_sucursales, name='ver_sucursales'),
    path('sucursales/actualizar/<int:pk>/', views.actualizar_sucursal, name='actualizar_sucursal'),
    path('sucursales/realizar_actualizacion/<int:pk>/', views.realizar_actualizacion_sucursal, name='realizar_actualizacion_sucursal'),
    path('sucursales/borrar/<int:pk>/', views.borrar_sucursal, name='borrar_sucursal'),

    # Rutas para Salas
    path('salas/agregar/', views.agregar_sala, name='agregar_sala'),
    path('salas/', views.ver_salas, name='ver_salas'),
    path('salas/actualizar/<int:pk>/', views.actualizar_sala, name='actualizar_sala'),
    path('salas/realizar_actualizacion/<int:pk>/', views.realizar_actualizacion_sala, name='realizar_actualizacion_sala'),
    path('salas/borrar/<int:pk>/', views.borrar_sala, name='borrar_sala'),

    # Rutas para Películas
    path('peliculas/agregar/', views.agregar_pelicula, name='agregar_pelicula'),
    path('peliculas/', views.ver_peliculas, name='ver_peliculas'),
    path('peliculas/actualizar/<int:pk>/', views.actualizar_pelicula, name='actualizar_pelicula'),
    path('peliculas/realizar_actualizacion/<int:pk>/', views.realizar_actualizacion_pelicula, name='realizar_actualizacion_pelicula'),
    path('peliculas/borrar/<int:pk>/', views.borrar_pelicula, name='borrar_pelicula'),

    # Rutas para Funciones (¡Nuevas!)
    path('funciones/agregar/', views.agregar_funcion, name='agregar_funcion'),
    path('funciones/', views.ver_funciones, name='ver_funciones'),
    path('funciones/actualizar/<int:pk>/', views.actualizar_funcion, name='actualizar_funcion'),
    path('funciones/realizar_actualizacion/<int:pk>/', views.actualizar_funcion, name='realizar_actualizacion_funcion'), # Redirige a actualizar_funcion
    path('funciones/borrar/<int:pk>/', views.borrar_funcion, name='borrar_funcion'),

    # Rutas para Clientes (¡Nuevas!)
    path('clientes/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('clientes/', views.ver_clientes, name='ver_clientes'),
    path('clientes/actualizar/<int:pk>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('clientes/realizar_actualizacion/<int:pk>/', views.actualizar_cliente, name='realizar_actualizacion_cliente'), # Redirige a actualizar_cliente
    path('clientes/borrar/<int:pk>/', views.borrar_cliente, name='borrar_cliente'),

    # Rutas para Transacciones (¡Nuevas!)
    path('transacciones/agregar/', views.agregar_transaccion, name='agregar_transaccion'),
    path('transacciones/', views.ver_transacciones, name='ver_transacciones'),
    path('transacciones/actualizar/<int:pk>/', views.actualizar_transaccion, name='actualizar_transaccion'),
    path('transacciones/realizar_actualizacion/<int:pk>/', views.actualizar_transaccion, name='realizar_actualizacion_transaccion'), # Redirige a actualizar_transaccion
    path('transacciones/borrar/<int:pk>/', views.borrar_transaccion, name='borrar_transaccion'),
]