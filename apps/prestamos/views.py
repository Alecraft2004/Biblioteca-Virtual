"""
Autor: Steve
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.catalogo.models import LibroDigital
from apps.core.funcional import (
    contar_prestamos_por_estado,
    libros_mas_prestados,
    total_licencias,
)
from apps.core.reglas import puede_aprobarse_prestamo
from apps.usuarios.decoradores import rol_requerido
from .models import PrestamoDigital


@login_required
def solicitar_prestamo(request, libro_id):
    """
    Cualquier usuario logueado puede solicitar un préstamo. La decisión
    de aprobar automáticamente o dejar pendiente NO se toma acá con
    ifs sueltos: se delega al motor de reglas de core/reglas.py
    (programación lógica), que evalúa hechos (libro, usuario) contra
    una base de reglas y devuelve si corresponde aprobar o no.
    """
    libro = get_object_or_404(LibroDigital, pk=libro_id, activo=True)

    # Bloqueo explícito: un usuario suspendido no puede ni siquiera
    # generar la solicitud, más allá de lo que diga el motor de reglas.
    if request.user.suspendido:
        messages.error(request, 'Tu cuenta está suspendida, no podés solicitar préstamos.')
        return redirect('catalogo:lista')

    if request.method == 'POST':
        aprueba, motivos = puede_aprobarse_prestamo(libro, request.user)

        if aprueba:
            PrestamoDigital.objects.create(
                libro=libro, usuario=request.user, estado=PrestamoDigital.Estado.APROBADO
            )
            messages.success(request, f'Préstamo de "{libro.titulo}" aprobado automáticamente.')
        else:
            PrestamoDigital.objects.create(
                libro=libro, usuario=request.user, estado=PrestamoDigital.Estado.PENDIENTE
            )
            messages.warning(
                request,
                f'Solicitud registrada, pendiente de revisión. Motivos: {"; ".join(motivos)}',
            )
        return redirect('catalogo:lista')

    return render(request, 'prestamos/solicitar.html', {'libro': libro})


@login_required
def mis_prestamos(request):
    """Historial completo de préstamos del usuario logueado (todos los estados)."""
    prestamos = request.user.prestamos.all()
    return render(request, 'prestamos/mis_prestamos.html', {'prestamos': prestamos})


@login_required
def devolver_prestamo(request, prestamo_id):
    """
    Permite al propio usuario devolver un libro que tiene aprobado.
    Se filtra por 'usuario=request.user' para que nadie pueda devolver
    préstamos de otra persona manipulando la URL.
    """
    prestamo = get_object_or_404(PrestamoDigital, pk=prestamo_id, usuario=request.user)
    if request.method == 'POST':
        if prestamo.estado == PrestamoDigital.Estado.APROBADO:
            prestamo.devolver()
            messages.success(
                request, f'Devolviste "{prestamo.libro.titulo}". La licencia quedó disponible de nuevo.'
            )
    return redirect('prestamos:mis_prestamos')


@login_required
def leer_libro(request, prestamo_id):
    """
    Muestra el detalle del libro (portada, sinopsis) y el archivo
    embebido para leerlo. Solo se puede acceder si el préstamo es
    propio y está en estado APROBADO: si lo devolviste o nunca te lo
    aprobaron, no deberías poder seguir leyéndolo.
    """
    prestamo = get_object_or_404(
        PrestamoDigital, pk=prestamo_id, usuario=request.user, estado=PrestamoDigital.Estado.APROBADO
    )
    return render(request, 'prestamos/leer.html', {'prestamo': prestamo})


@rol_requerido('BIBLIOTECARIO')
def gestionar_prestamos(request):
    """Panel del bibliotecario con los préstamos pendientes de revisión."""
    pendientes = PrestamoDigital.objects.filter(estado=PrestamoDigital.Estado.PENDIENTE)
    return render(request, 'prestamos/gestionar.html', {'prestamos': pendientes})


@rol_requerido('BIBLIOTECARIO')
def aprobar_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(PrestamoDigital, pk=prestamo_id)
    prestamo.aprobar(request.user)
    messages.success(request, 'Préstamo aprobado.')
    return redirect('prestamos:gestionar')


@rol_requerido('BIBLIOTECARIO')
def rechazar_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(PrestamoDigital, pk=prestamo_id)
    prestamo.rechazar(request.user)
    messages.warning(request, 'Préstamo rechazado.')
    return redirect('prestamos:gestionar')


@rol_requerido('BIBLIOTECARIO')
def estadisticas(request):
    """
    Dashboard con métricas del sistema. Acá es donde se usan las
    funciones puras de core/funcional.py (programación funcional):
    la vista solo junta los datos y se los pasa a esas funciones,
    que no modifican nada, solo calculan y devuelven resultados nuevos.
    """
    libros = list(LibroDigital.objects.filter(activo=True))
    prestamos = list(PrestamoDigital.objects.all())

    contexto = {
        'total_licencias': total_licencias(libros),
        'prestamos_por_estado': contar_prestamos_por_estado(prestamos),
        'top_libros': libros_mas_prestados(libros, top=5),
    }
    return render(request, 'prestamos/estadisticas.html', contexto)