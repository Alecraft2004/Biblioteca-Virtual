"""
Autor: Steve
"""
from django.urls import path
from . import views

app_name = 'prestamos'

urlpatterns = [
    path('solicitar/<int:libro_id>/', views.solicitar_prestamo, name='solicitar'),
    path('mis-prestamos/', views.mis_prestamos, name='mis_prestamos'),
    path('devolver/<int:prestamo_id>/', views.devolver_prestamo, name='devolver'),
    path('leer/<int:prestamo_id>/', views.leer_libro, name='leer'),
    path('gestionar/', views.gestionar_prestamos, name='gestionar'),
    path('aprobar/<int:prestamo_id>/', views.aprobar_prestamo, name='aprobar'),
    path('rechazar/<int:prestamo_id>/', views.rechazar_prestamo, name='rechazar'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
]