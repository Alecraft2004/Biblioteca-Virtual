"""
Motor de reglas lógicas (estilo hechos/condiciones, inspirado en Prolog)
para decidir si un préstamo digital puede aprobarse.
Cada regla es una función pura que recibe 'hechos' (un diccionario con el
estado del sistema) y devuelve (cumple: bool, motivo: str si no cumple).
Autor: Alejandro
"""


def regla_usuario_no_suspendido(hechos):
    if hechos['usuario'].suspendido:
        return False, "El usuario está suspendido."
    return True, None


def regla_licencias_disponibles(hechos):
    if hechos['libro'].licencias_disponibles <= 0:
        return False, "No hay licencias disponibles para este libro."
    return True, None


def regla_nivel_compatible(hechos):
    libro, usuario = hechos['libro'], hechos['usuario']
    if libro.nivel == 'GENERAL':
        return True, None
    if usuario.es_estudiante and libro.nivel != 'GENERAL':
        # Simplificación: se podría cruzar con un campo 'grado' del estudiante.
        return True, None
    return True, None


# Base de reglas: así como en Prolog se declaran cláusulas, acá se declara
# la lista de reglas que se van a evaluar en orden.
REGLAS_APROBACION_PRESTAMO = [
    regla_usuario_no_suspendido,
    regla_licencias_disponibles,
    regla_nivel_compatible,
]


def puede_aprobarse_prestamo(libro, usuario):
    """
    Motor de inferencia simple: evalúa todas las reglas contra los hechos
    (libro, usuario). Si todas se cumplen, el préstamo es válido.
    Devuelve (True, []) o (False, ['motivo1', 'motivo2', ...]).
    """
    hechos = {'libro': libro, 'usuario': usuario}
    motivos_rechazo = []
    for regla in REGLAS_APROBACION_PRESTAMO:
        cumple, motivo = regla(hechos)
        if not cumple:
            motivos_rechazo.append(motivo)
    return (len(motivos_rechazo) == 0, motivos_rechazo)