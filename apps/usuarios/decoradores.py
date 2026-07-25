"""
Decorador para restringir vistas según el rol del usuario.
Autor: Steve
"""
from functools import wraps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def rol_requerido(*roles_permitidos):
    """
    Decorador de fábrica (una función que devuelve un decorador):
    se usa como @rol_requerido('BIBLIOTECARIO') sobre una vista.

    Funcionamiento:
    1. Primero exige que el usuario esté logueado (@login_required).
    2. Después chequea que su 'rol' esté dentro de los roles permitidos.
    3. Si no cumple, muestra un mensaje de error y lo redirige a 'inicio'
       en vez de dejarlo entrar a la vista protegida.
    """
    def decorador(vista):
        @wraps(vista)  # conserva el nombre/docstring original de la vista
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.rol not in roles_permitidos:
                messages.error(request, 'No tenés permiso para acceder a esa sección.')
                return redirect('inicio')
            return vista(request, *args, **kwargs)
        return wrapper
    return decorador