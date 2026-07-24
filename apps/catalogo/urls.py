"""
Autor: Alejandro
"""
from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.lista_libros, name='lista'),
    path('nuevo/', views.crear_libro, name='crear'),
    path('<int:libro_id>/editar/', views.editar_libro, name='editar'),
    path('<int:libro_id>/eliminar/', views.eliminar_libro, name='eliminar'),
]