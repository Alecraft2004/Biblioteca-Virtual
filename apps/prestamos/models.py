"""
Modelo de préstamos de libros digitales.
Autor: Alejandro
"""
from django.conf import settings
from django.db import models
from django.utils import timezone


class PrestamoDigital(models.Model):
    """
    Representa la solicitud de préstamo de un libro digital por parte
    de un estudiante o docente, y su ciclo de vida (pendiente -> aprobado/rechazado).
    """

    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        APROBADO = 'APROBADO', 'Aprobado'
        RECHAZADO = 'RECHAZADO', 'Rechazado'
        DEVUELTO = 'DEVUELTO', 'Devuelto'

    libro = models.ForeignKey(
        'catalogo.LibroDigital', on_delete=models.PROTECT, related_name='prestamos'
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prestamos'
    )
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_resolucion = models.DateTimeField(null=True, blank=True)
    aprobado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='prestamos_gestionados'
    )

    class Meta:
        ordering = ['-fecha_solicitud']

    def __str__(self):
        return f"{self.libro.titulo} -> {self.usuario} ({self.estado})"

    def aprobar(self, bibliotecario):
        """Marca el préstamo como aprobado y registra quién lo hizo."""
        self.estado = self.Estado.APROBADO
        self.aprobado_por = bibliotecario
        self.fecha_resolucion = timezone.now()
        self.save()

    def rechazar(self, bibliotecario):
        self.estado = self.Estado.RECHAZADO
        self.aprobado_por = bibliotecario
        self.fecha_resolucion = timezone.now()
        self.save()