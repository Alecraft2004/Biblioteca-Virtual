"""
Autor: Alejandro
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Rol y estado', {'fields': ('rol', 'suspendido')}),
    )
    list_display = ('username', 'email', 'rol', 'is_active', 'suspendido')