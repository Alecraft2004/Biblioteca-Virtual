"""
Decorador para restringir vistas según el rol del usuario.
Autor: Alejandro
"""
from functools import wraps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def rol_requerido(*roles_permitidos):
    """Decorador de fábrica: solo deja pasar si request.user.rol está en roles_permitidos."""
    def decorador(vista):
        @wraps(vista)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.rol not in roles_permitidos:
                messages.error(request, 'No tenés permiso para acceder a esa sección.')
                return redirect('inicio')
            return vista(request, *args, **kwargs)
        return wrapper
    return decorador