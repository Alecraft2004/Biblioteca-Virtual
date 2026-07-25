"""
Motor de reglas lógicas (estilo hechos/condiciones, inspirado en Prolog)
para decidir si un préstamo digital puede aprobarse.
Cada regla es una función pura que recibe 'hechos' (un diccionario con el
estado del sistema) y devuelve (cumple: bool, motivo: str si no cumple).
Autor: Alejandro
"""


def regla_usuario_no_suspendido(hechos):
    """Hecho evaluado: el usuario no debe estar suspendido."""
    if hechos['usuario'].suspendido:
        return False, "El usuario está suspendido."
    return True, None


def regla_licencias_disponibles(hechos):
    """Hecho evaluado: debe quedar al menos una licencia libre del libro."""
    if hechos['libro'].licencias_disponibles <= 0:
        return False, "No hay licencias disponibles para este libro."
    return True, None


def regla_nivel_compatible(hechos):
    """
    Hecho evaluado: el nivel del libro debe ser compatible con el usuario.
    Simplificada a propósito: los libros de nivel GENERAL siempre son
    compatibles; para niveles específicos se podría cruzar a futuro con
    un campo 'grado' del estudiante.
    """
    libro, usuario = hechos['libro'], hechos['usuario']
    if libro.nivel == 'GENERAL':
        return True, None
    if usuario.es_estudiante and libro.nivel != 'GENERAL':
        return True, None
    return True, None


# Base de reglas: al estilo de las cláusulas de Prolog, se declara la
# lista de reglas a evaluar. Agregar una regla nueva es sumarla acá,
# sin tocar el motor de inferencia de abajo.
REGLAS_APROBACION_PRESTAMO = [
    regla_usuario_no_suspendido,
    regla_licencias_disponibles,
    regla_nivel_compatible,
]


def puede_aprobarse_prestamo(libro, usuario):
    """
    Motor de inferencia: evalúa todas las reglas contra los hechos
    (libro, usuario) y devuelve (True, []) si todas se cumplen, o
    (False, ['motivo1', 'motivo2', ...]) con los motivos de rechazo.
    """
    hechos = {'libro': libro, 'usuario': usuario}
    motivos_rechazo = []
    for regla in REGLAS_APROBACION_PRESTAMO:
        cumple, motivo = regla(hechos)
        if not cumple:
            motivos_rechazo.append(motivo)
    return (len(motivos_rechazo) == 0, motivos_rechazo)