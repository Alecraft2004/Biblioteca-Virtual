"""
Autor: Alejandro
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from apps.usuarios.decoradores import rol_requerido
from .forms import LibroDigitalForm
from .models import LibroDigital


@login_required
def lista_libros(request):
    """
    Catálogo visible para cualquier usuario logueado. Soporta búsqueda
    por título/autor y filtro por nivel educativo vía parámetros GET
    (query string), por eso no hace falta un formulario POST acá.
    """
    libros = LibroDigital.objects.filter(activo=True)

    query = request.GET.get('q', '').strip()
    nivel = request.GET.get('nivel', '').strip()

    if query:
        # OR entre título y autor: alcanza con que coincida uno de los dos.
        libros = libros.filter(titulo__icontains=query) | libros.filter(autor__icontains=query)
    if nivel:
        libros = libros.filter(nivel=nivel)

    contexto = {
        # distinct() evita duplicados cuando un libro matchea por título Y autor.
        'libros': libros.distinct(),
        'query': query,
        'nivel': nivel,
        'niveles': LibroDigital.Nivel.choices,
    }
    return render(request, 'catalogo/lista.html', contexto)


@rol_requerido('BIBLIOTECARIO')
def crear_libro(request):
    """Alta de un nuevo libro digital. Solo accesible por el bibliotecario."""
    if request.method == 'POST':
        form = LibroDigitalForm(request.POST, request.FILES)
        if form.is_valid():
            # commit=False: guarda el objeto en memoria sin tocar la BD
            # todavía, para poder completar 'subido_por' antes de guardar.
            libro = form.save(commit=False)
            libro.subido_por = request.user
            libro.save()
            messages.success(request, f'Libro "{libro.titulo}" cargado correctamente.')
            return redirect('catalogo:lista')
    else:
        form = LibroDigitalForm()
    return render(request, 'catalogo/formulario.html', {'form': form, 'accion': 'Cargar'})


@rol_requerido('BIBLIOTECARIO')
def editar_libro(request, libro_id):
    """Modifica los datos de un libro ya cargado."""
    libro = get_object_or_404(LibroDigital, pk=libro_id)
    if request.method == 'POST':
        form = LibroDigitalForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            form.save()
            messages.success(request, f'Libro "{libro.titulo}" actualizado.')
            return redirect('catalogo:lista')
    else:
        form = LibroDigitalForm(instance=libro)
    return render(request, 'catalogo/formulario.html', {'form': form, 'accion': 'Editar'})


@rol_requerido('BIBLIOTECARIO')
def eliminar_libro(request, libro_id):
    """
    Elimina un libro, con pantalla de confirmación previa (GET) y borrado
    real recién en el POST. Si el libro tiene préstamos asociados, la
    relación PROTECT en PrestamoDigital.libro lanza ProtectedError en vez
    de dejar borrar y romper el historial de préstamos.
    """
    libro = get_object_or_404(LibroDigital, pk=libro_id)
    if request.method == 'POST':
        titulo = libro.titulo
        try:
            libro.delete()
            messages.warning(request, f'Libro "{titulo}" eliminado.')
        except ProtectedError:
            messages.error(
                request,
                f'No se puede eliminar "{titulo}" porque tiene préstamos asociados. '
                'Gestioná esos préstamos primero.'
            )
        return redirect('catalogo:lista')
    return render(request, 'catalogo/confirmar_eliminar.html', {'libro': libro})