class ErrorSistema(Exception): pass
class ErrorValidacion(ErrorSistema): pass
class ClienteDuplicadoError(ErrorSistema): pass
class ClienteNoEncontradoError(ErrorSistema): pass
class ServicioNoDisponibleError(ErrorSistema): pass
class ReservaInvalidaError(ErrorSistema): pass
class OperacionNoPermitidaError(ErrorSistema): pass
class ErrorCalculoError(ErrorSistema): pass
