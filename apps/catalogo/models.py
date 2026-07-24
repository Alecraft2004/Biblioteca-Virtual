# Create your models here.
"""
Modelos del catálogo de libros digitales.
Autor: Alejandro
"""
from django.conf import settings
from django.db import models


class Categoria(models.Model):
    """Categoría temática de un libro (ej: Matemática, Historia, Literatura)."""
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class LibroDigital(models.Model):
    """
    Representa un libro/material digital cargado por un bibliotecario,
    disponible para préstamo según nivel educativo.
    """

    class Nivel(models.TextChoices):
        PRIMARIA = 'PRIMARIA', 'Primaria'
        SECUNDARIA = 'SECUNDARIA', 'Secundaria'
        GENERAL = 'GENERAL', 'General'

    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=150)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='libros')
    nivel = models.CharField(max_length=20, choices=Nivel.choices, default=Nivel.GENERAL)
    sinopsis = models.TextField(blank=True)
    archivo = models.FileField(upload_to='libros/')
    portada = models.ImageField(upload_to='portadas/', blank=True, null=True)
    licencias_totales = models.PositiveIntegerField(default=1)
    activo = models.BooleanField(default=True)
    subido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='libros_subidos'
    )
    fecha_carga = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['titulo']

    def __str__(self):
        return self.titulo

    @property
    def licencias_disponibles(self):
        """
        Licencias libres = totales - préstamos activos.
        Usa el related_name 'prestamos' del modelo PrestamoDigital (lo creamos en el paso 10).
        """
        prestados = self.prestamos.filter(estado='APROBADO').count()
        return max(self.licencias_totales - prestados, 0)