"""
Modelo de préstamos de libros digitales.
Autor: Steve
"""
from django.conf import settings
from django.db import models
from django.utils import timezone


class PrestamoDigital(models.Model):
    """
    Representa la solicitud de préstamo de un libro digital por parte
    de un estudiante o docente, y su ciclo de vida:
    PENDIENTE -> APROBADO/RECHAZADO -> (si se aprobó) DEVUELTO.
    Cada solicitud es un registro histórico, no se sobrescribe.
    """

    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        APROBADO = 'APROBADO', 'Aprobado'
        RECHAZADO = 'RECHAZADO', 'Rechazado'
        DEVUELTO = 'DEVUELTO', 'Devuelto'

    # PROTECT: no se puede borrar un libro si tiene préstamos en la
    # tabla (así se conserva el historial). Se usa el string
    # 'catalogo.LibroDigital' en vez de importar la clase directamente
    # para evitar un import circular entre las apps catalogo y prestamos.
    libro = models.ForeignKey(
        'catalogo.LibroDigital', on_delete=models.PROTECT, related_name='prestamos'
    )
    # CASCADE: si se borra el usuario, tiene sentido que se borren
    # también sus solicitudes de préstamo asociadas.
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prestamos'
    )
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_resolucion = models.DateTimeField(null=True, blank=True)

    # Registra qué bibliotecario aprobó/rechazó, para trazabilidad.
    aprobado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='prestamos_gestionados'
    )

    class Meta:
        ordering = ['-fecha_solicitud']  # los más recientes primero

    def __str__(self):
        return f"{self.libro.titulo} -> {self.usuario} ({self.estado})"

    def aprobar(self, bibliotecario):
        """Marca el préstamo como aprobado y registra quién y cuándo."""
        self.estado = self.Estado.APROBADO
        self.aprobado_por = bibliotecario
        self.fecha_resolucion = timezone.now()
        self.save()

    def rechazar(self, bibliotecario):
        """Marca el préstamo como rechazado y registra quién y cuándo."""
        self.estado = self.Estado.RECHAZADO
        self.aprobado_por = bibliotecario
        self.fecha_resolucion = timezone.now()
        self.save()

    def devolver(self):
        """
        Marca el préstamo como devuelto. Como 'licencias_disponibles'
        en LibroDigital solo cuenta préstamos en estado APROBADO, este
        cambio libera automáticamente una licencia del libro.
        """
        self.estado = self.Estado.DEVUELTO
        self.save()