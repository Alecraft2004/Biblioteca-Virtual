"""
Modelo de Usuario personalizado con roles para la Biblioteca Virtual.
Autor: Alejandro
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Extiende el usuario base de Django (AbstractUser ya trae username,
    password, email, first_name, last_name) agregando el campo 'rol'
    que define los permisos dentro del sistema.
    """

    class Rol(models.TextChoices):
        ESTUDIANTE = 'ESTUDIANTE', 'Estudiante'
        DOCENTE = 'DOCENTE', 'Docente'
        BIBLIOTECARIO = 'BIBLIOTECARIO', 'Bibliotecario'

    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.ESTUDIANTE)
    suspendido = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_rol_display()})"

    @property
    def es_estudiante(self):
        return self.rol == self.Rol.ESTUDIANTE

    @property
    def es_docente(self):
        return self.rol == self.Rol.DOCENTE

    @property
    def es_bibliotecario(self):
        return self.rol == self.Rol.BIBLIOTECARIO