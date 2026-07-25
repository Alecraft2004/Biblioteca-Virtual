"""
Autor: Alejandro
"""
from django import forms
from .models import LibroDigital


class LibroDigitalForm(forms.ModelForm):
    """Formulario de carga/edición de libros, usado por el bibliotecario."""

    class Meta:
        model = LibroDigital
        fields = [
            'titulo', 'autor', 'categoria', 'nivel', 'sinopsis',
            'archivo', 'portada', 'licencias_totales', 'activo',
        ]
        widgets = {
            # Reemplaza el checkbox por defecto por un toggle visual (CSS).
            'activo': forms.CheckboxInput(attrs={'class': 'toggle-switch'}),
            # Sinopsis con más espacio vertical que un input de una línea.
            'sinopsis': forms.Textarea(attrs={'rows': 4}),
        }