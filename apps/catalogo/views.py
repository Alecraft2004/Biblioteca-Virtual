"""
Autor: Alejandro
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.usuarios.decoradores import rol_requerido
from .forms import LibroDigitalForm
from .models import LibroDigital
from django.db.models import ProtectedError


@login_required
def lista_libros(request):
    libros = LibroDigital.objects.filter(activo=True)

    query = request.GET.get('q', '').strip()
    nivel = request.GET.get('nivel', '').strip()

    if query:
        libros = libros.filter(titulo__icontains=query) | libros.filter(autor__icontains=query)
    if nivel:
        libros = libros.filter(nivel=nivel)

    contexto = {
        'libros': libros.distinct(),
        'query': query,
        'nivel': nivel,
        'niveles': LibroDigital.Nivel.choices,
    }
    return render(request, 'catalogo/lista.html', contexto)


@rol_requerido('BIBLIOTECARIO')
def crear_libro(request):
    if request.method == 'POST':
        form = LibroDigitalForm(request.POST, request.FILES)
        if form.is_valid():
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