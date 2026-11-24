
"""
Proyecto: Software FJ
Archivo: excepciones.py
Descripción: Excepciones personalizadas del sistema.
"""


class ErrorSistema(Exception):
    """Excepción general del sistema."""
    pass


class DatosInvalidosError(ErrorSistema):
    """Datos ingresados incorrectamente."""
    pass


class ClienteNoEncontradoError(ErrorSistema):
    """Cliente inexistente."""
    pass


class ServicioNoDisponibleError(ErrorSistema):
    """Servicio no disponible."""
    pass


class ReservaInvalidaError(ErrorSistema):
    """Reserva incorrecta."""
    pass


class OperacionNoPermitidaError(ErrorSistema):
    """Operación no permitida."""
    pass


class ParametroFaltanteError(ErrorSistema):
    """Falta un parámetro obligatorio."""
    pass
