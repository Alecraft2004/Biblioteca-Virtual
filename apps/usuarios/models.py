"""
Modelo de Usuario personalizado con roles para la Biblioteca Virtual.
Autor: Steve
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Extiende el usuario base de Django (AbstractUser ya trae username,
    password, email, first_name, last_name, y todo el sistema de
    autenticación y permisos resuelto) agregando el campo 'rol', que
    es lo que determina qué puede hacer cada persona dentro del sistema.
    """

    class Rol(models.TextChoices):
        # TextChoices es la forma declarativa de Django para definir un
        # enum: cada opción tiene un valor interno (lo que se guarda en
        # la base de datos) y una etiqueta legible (lo que se muestra).
        ESTUDIANTE = 'ESTUDIANTE', 'Estudiante'
        DOCENTE = 'DOCENTE', 'Docente'
        BIBLIOTECARIO = 'BIBLIOTECARIO', 'Bibliotecario'

    # Rol asignado al usuario; por defecto todo usuario nuevo entra como
    # Estudiante, y el bibliotecario es quien puede cambiarlo después.
    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.ESTUDIANTE)

    # Permite al bibliotecario bloquear el acceso de un usuario sin
    # necesidad de borrarlo (conserva su historial de préstamos).
    suspendido = models.BooleanField(default=False)

    def __str__(self):
        # Se usa en el panel de admin y en cualquier lugar donde Django
        # necesite mostrar el objeto como texto.
        return f"{self.get_full_name() or self.username} ({self.get_rol_display()})"

    # --- Propiedades de conveniencia ---
    # En vez de escribir 'usuario.rol == "ESTUDIANTE"' en cada vista o
    # template, se usa 'usuario.es_estudiante'. Más legible y evita
    # errores de tipeo con los strings de los roles.
    @property
    def es_estudiante(self):
        return self.rol == self.Rol.ESTUDIANTE

    @property
    def es_docente(self):
        return self.rol == self.Rol.DOCENTE

    @property
    def es_bibliotecario(self):
        return self.rol == self.Rol.BIBLIOTECARIO