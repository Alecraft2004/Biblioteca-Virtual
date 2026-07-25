"""
Autor: Steve
"""
from django.contrib import admin
from .models import PrestamoDigital


@admin.register(PrestamoDigital)
class PrestamoDigitalAdmin(admin.ModelAdmin):
    list_display = ('libro', 'usuario', 'estado', 'fecha_solicitud', 'aprobado_por')
    list_filter = ('estado',)
    search_fields = ('libro__titulo', 'usuario__username')