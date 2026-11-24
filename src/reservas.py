
"""
Proyecto: Software FJ
Archivo: reservas.py
Descripción: Gestión de reservas.
"""

import logging

from .clientes import Cliente
from .servicios import Servicio
from .excepciones import (
    DatosInvalidosError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ServicioNoDisponibleError
)

logger = logging.getLogger(__name__)


class Reserva:

    def __init__(self, codigo, cliente, servicio, duracion):
        if not codigo:
            raise DatosInvalidosError("El código de reserva es obligatorio.")

        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("El cliente no es válido.")

        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("El servicio no es válido.")

        servicio.validar_parametros(duracion)

        self.codigo = codigo
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"
        self.costo_total = 0.0

    def confirmar(self):
        if self.estado != "Pendiente":
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes."
            )

        self.servicio.validar_parametros(self.duracion)
        self.costo_total = self.servicio.calcular_costo(self.duracion)
        self.estado = "Confirmada"

        logger.info("Reserva %s confirmada.", self.codigo)

        return "Reserva confirmada correctamente."

    def cancelar(self):
        if self.estado == "Cancelada":
            raise OperacionNoPermitidaError(
                "La reserva ya se encuentra cancelada."
            )

        if self.estado == "Procesada":
            raise OperacionNoPermitidaError(
                "No se puede cancelar una reserva procesada."
            )

        self.estado = "Cancelada"
        logger.info("Reserva %s cancelada.", self.codigo)

        return "Reserva cancelada correctamente."

    def procesar(self):
        if self.estado != "Confirmada":
            raise ReservaInvalidaError(
                "La reserva debe estar confirmada antes de procesarse."
            )

        self.estado = "Procesada"
        logger.info("Reserva %s procesada.", self.codigo)

        return "Reserva procesada correctamente."

    def mostrar_informacion(self):
        return (
            f"Reserva: {self.codigo} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Duración: {self.duracion} | "
            f"Estado: {self.estado} | "
            f"Costo: ${self.costo_total:,.2f}"
        )


class GestorReservas:

    def __init__(self):
        self.reservas = []

    def crear_reserva(self, reserva):
        if not isinstance(reserva, Reserva):
            raise ReservaInvalidaError("El objeto de reserva no es válido.")

        for existente in self.reservas:
            if existente.codigo == reserva.codigo:
                raise ReservaInvalidaError(
                    "Ya existe una reserva con ese código."
                )

        self.reservas.append(reserva)
        logger.info("Reserva %s creada.", reserva.codigo)

        return "Reserva creada correctamente."

    def buscar_reserva(self, codigo):
        for reserva in self.reservas:
            if reserva.codigo == codigo:
                return reserva

        raise ReservaInvalidaError(
            f"No existe la reserva {codigo}."
        )

    def listar_reservas(self):
        return self.reservas

    def confirmar_reserva(self, codigo):
        reserva = self.buscar_reserva(codigo)
        return reserva.confirmar()

    def cancelar_reserva(self, codigo):
        reserva = self.buscar_reserva(codigo)
        return reserva.cancelar()

    def procesar_reserva(self, codigo):
        reserva = self.buscar_reserva(codigo)
        return reserva.procesar()
