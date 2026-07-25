"""
Autor: Steve
"""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .decoradores import rol_requerido
from .forms import UsuarioCreationForm, UsuarioEditForm
from .models import Usuario


@rol_requerido('BIBLIOTECARIO')
def lista_usuarios(request):
    """Muestra todos los usuarios registrados en el sistema."""
    usuarios = Usuario.objects.all().order_by('username')
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})


@rol_requerido('BIBLIOTECARIO')
def crear_usuario(request):
    """Registra un usuario nuevo (estudiante, docente o bibliotecario)."""
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f'Usuario "{usuario.username}" creado correctamente.')
            return redirect('usuarios:lista')
    else:
        form = UsuarioCreationForm()
    return render(request, 'usuarios/formulario.html', {'form': form, 'accion': 'Crear'})


@rol_requerido('BIBLIOTECARIO')
def editar_usuario(request, usuario_id):
    """Modifica datos, rol o estado (activo/suspendido) de un usuario."""
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuario "{usuario.username}" actualizado.')
            return redirect('usuarios:lista')
    else:
        form = UsuarioEditForm(instance=usuario)
    return render(request, 'usuarios/formulario.html', {'form': form, 'accion': 'Editar'})


@rol_requerido('BIBLIOTECARIO')
def eliminar_usuario(request, usuario_id):
    """Elimina un usuario, con confirmación previa en una página aparte."""
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    if request.method == 'POST':
        # Evita que un bibliotecario se elimine a sí mismo por error
        # y se quede sin poder administrar el sistema.
        if usuario == request.user:
            messages.error(request, 'No podés eliminar tu propio usuario.')
            return redirect('usuarios:lista')
        nombre = usuario.username
        usuario.delete()
        messages.warning(request, f'Usuario "{nombre}" eliminado.')
        return redirect('usuarios:lista')
    return render(request, 'usuarios/confirmar_eliminar.html', {'usuario': usuario})