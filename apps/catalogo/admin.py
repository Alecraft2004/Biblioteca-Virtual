# Register your models here.
"""
Autor: Alejandro
"""
from django.contrib import admin
from .models import Categoria, LibroDigital


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(LibroDigital)
class LibroDigitalAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'nivel', 'licencias_totales', 'activo')
    list_filter = ('categoria', 'nivel', 'activo')
    search_fields = ('titulo', 'autor')