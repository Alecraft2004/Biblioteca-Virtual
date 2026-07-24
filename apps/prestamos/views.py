"""
Autor: Alejandro
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.catalogo.models import LibroDigital
from apps.core.reglas import puede_aprobarse_prestamo
from .models import PrestamoDigital


@login_required
def solicitar_prestamo(request, libro_id):
    libro = get_object_or_404(LibroDigital, pk=libro_id, activo=True)

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
    prestamos = request.user.prestamos.all()
    return render(request, 'prestamos/mis_prestamos.html', {'prestamos': prestamos})


from django.contrib import messages
from apps.usuarios.decoradores import rol_requerido


@rol_requerido('BIBLIOTECARIO')
def gestionar_prestamos(request):
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

from apps.core.funcional import (
    contar_prestamos_por_estado,
    libros_mas_prestados,
    total_licencias,
)
from apps.catalogo.models import LibroDigital


@rol_requerido('BIBLIOTECARIO')
def estadisticas(request):
    libros = list(LibroDigital.objects.filter(activo=True))
    prestamos = list(PrestamoDigital.objects.all())

    contexto = {
        'total_licencias': total_licencias(libros),
        'prestamos_por_estado': contar_prestamos_por_estado(prestamos),
        'top_libros': libros_mas_prestados(libros, top=5),
    }
    return render(request, 'prestamos/estadisticas.html', contexto)