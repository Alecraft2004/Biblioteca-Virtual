"""
Autor: Alejandro
"""
from django import forms
from .models import LibroDigital


class LibroDigitalForm(forms.ModelForm):
    class Meta:
        model = LibroDigital
        fields = [
            'titulo', 'autor', 'categoria', 'nivel', 'sinopsis',
            'archivo', 'portada', 'licencias_totales', 'activo',
        ]