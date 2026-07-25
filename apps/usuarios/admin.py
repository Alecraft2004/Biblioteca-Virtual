"""
Autor: Steve
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    # Se reutiliza UserAdmin (el admin que Django ya trae armado para
    # usuarios, con sus fieldsets de permisos y contraseña) y solo se
    # le agrega una sección extra para nuestros campos personalizados.
    fieldsets = UserAdmin.fieldsets + (
        ('Rol y estado', {'fields': ('rol', 'suspendido')}),
    )
    # Columnas que se ven en el listado de usuarios del panel /admin.
    list_display = ('username', 'email', 'rol', 'is_active', 'suspendido')