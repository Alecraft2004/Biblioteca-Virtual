"""
Autor: Alejandro
"""
from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.lista_libros, name='lista'),
    path('nuevo/', views.crear_libro, name='crear'),
    path('inactivos/', views.libros_inactivos, name='inactivos'),
    path('<int:libro_id>/activar/', views.activar_libro, name='activar'),
    path('<int:libro_id>/editar/', views.editar_libro, name='editar'),
    path('<int:libro_id>/eliminar/', views.eliminar_libro, name='eliminar'),
]