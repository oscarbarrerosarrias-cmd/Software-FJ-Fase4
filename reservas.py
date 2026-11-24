from datetime import datetime
from excepciones import ReservaInvalidaError, OperacionNoPermitidaError

class Reserva:
    def __init__(self, codigo, cliente, servicio, duracion, parametros=None, descuento=0, impuesto=0.19):
        if not codigo or cliente is None or servicio is None:
            raise ReservaInvalidaError("Código, cliente y servicio son obligatorios.")
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ReservaInvalidaError("La duración debe ser positiva.")
        servicio.validar_disponibilidad()
        servicio.validar_parametros(**(parametros or {}))
        self.codigo, self.cliente, self.servicio = str(codigo), cliente, servicio
        self.duracion, self.parametros = duracion, parametros or {}
        self.estado = "Pendiente"
        self.fecha = datetime.now().isoformat(timespec="seconds")
        self.costo = servicio.calcular_costo(duracion, descuento, impuesto)

    def confirmar(self):
        if self.estado != "Pendiente":
            raise OperacionNoPermitidaError("Solo se confirman reservas pendientes.")
        self.estado = "Confirmada"
        return f"Reserva {self.codigo} confirmada."

    def cancelar(self):
        if self.estado in ("Cancelada", "Procesada"):
            raise OperacionNoPermitidaError("No se puede cancelar en el estado actual.")
        self.estado = "Cancelada"
        return f"Reserva {self.codigo} cancelada."

    def procesar(self):
        if self.estado != "Confirmada":
            raise OperacionNoPermitidaError("Primero debe confirmar la reserva.")
        self.estado = "Procesada"
        return f"Reserva {self.codigo} procesada."

    def mostrar_informacion(self):
        return f"{self.codigo} | {self.cliente.nombre} | {self.servicio.nombre} | ${self.costo:,.2f} | {self.estado}"
