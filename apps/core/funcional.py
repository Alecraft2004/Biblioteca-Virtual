"""
Funciones puras de programación funcional, usadas para generar estadísticas
del catálogo y de préstamos sin tocar la base de datos directamente
(reciben datos, devuelven datos nuevos, no modifican nada).
Autor: Alejandro
"""
from functools import reduce


def libros_por_nivel(libros, nivel):
    """Filtra libros de un nivel educativo específico. Función pura: no muta 'libros'."""
    return list(filter(lambda libro: libro.nivel == nivel, libros))


def titulos(libros):
    """Devuelve solo los títulos, usando map en vez de un for."""
    return list(map(lambda libro: libro.titulo, libros))


def total_licencias(libros):
    """Suma total de licencias usando reduce (programación funcional clásica)."""
    return reduce(lambda acumulado, libro: acumulado + libro.licencias_totales, libros, 0)


def contar_prestamos_por_estado(prestamos):
    """
    Agrupa préstamos por estado sin loops explícitos, combinando
    comprehensions (map/filter implícito) con reduce.
    """
    estados = {p.estado for p in prestamos}
    return {
        estado: len([p for p in prestamos if p.estado == estado])
        for estado in estados
    }


def libros_mas_prestados(libros, top=5):
    """
    Ordena libros por cantidad de préstamos aprobados (de mayor a menor)
    usando 'sorted' con una función clave (estilo funcional), sin mutar la lista original.
    """
    return sorted(
        libros,
        key=lambda libro: libro.prestamos.filter(estado='APROBADO').count(),
        reverse=True,
    )[:top]