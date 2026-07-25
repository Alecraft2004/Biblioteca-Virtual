"""
Autor: Steve
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Usuario


class UsuarioCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'rol']


class UsuarioEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'rol', 'suspendido', 'is_active']


class LoginSuspendidoForm(AuthenticationForm):
    """
    Formulario de login personalizado. Django's AuthenticationForm ya
    trae el método 'confirm_login_allowed' pensado justo para este caso:
    se ejecuta después de validar usuario/contraseña, y si lanza un
    ValidationError, el login se rechaza mostrando ese mensaje.
    """
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if user.suspendido:
            raise forms.ValidationError(
                "Tu cuenta está suspendida. Contactá al bibliotecario para reactivarla.",
                code='suspendido',
            )