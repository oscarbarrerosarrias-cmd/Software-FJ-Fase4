
"""
Proyecto: Software FJ
Archivo: servicios.py
Descripción: Servicios especializados de la empresa.
"""

from abc import ABC, abstractmethod

from .excepciones import (
    DatosInvalidosError,
    ServicioNoDisponibleError,
    ParametroFaltanteError
)


class Servicio(ABC):

    def __init__(self, codigo, nombre, precio_base):
        if not codigo or not nombre:
            raise ParametroFaltanteError(
                "El código y el nombre son obligatorios."
            )

        if not isinstance(precio_base, (int, float)) or isinstance(precio_base, bool) or precio_base <= 0:
            raise DatosInvalidosError("El precio debe ser mayor que cero.")

        self.codigo = codigo
        self.nombre = nombre
        self.precio_base = float(precio_base)
        self.disponible = True

    @abstractmethod
    def validar_parametros(self, duracion):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    @abstractmethod
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        pass

    def cambiar_disponibilidad(self, estado):
        if not isinstance(estado, bool):
            raise DatosInvalidosError("La disponibilidad debe ser verdadera o falsa.")
        self.disponible = estado


class ReservaSala(Servicio):

    def __init__(self, codigo, nombre, precio_base, capacidad):
        super().__init__(codigo, nombre, precio_base)

        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or capacidad <= 0:
            raise DatosInvalidosError("La capacidad debe ser un entero positivo.")

        self.capacidad = capacidad

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise DatosInvalidosError("La duración de la sala debe ser positiva.")

        if not self.disponible:
            raise ServicioNoDisponibleError("La sala no está disponible.")

        return True

    def describir_servicio(self):
        return (
            f"Reserva de sala: {self.nombre}. "
            f"Capacidad: {self.capacidad} personas."
        )

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)
        validar_condiciones_pago(descuento, impuesto)

        subtotal = self.precio_base * duracion
        return aplicar_condiciones(subtotal, descuento, impuesto)


class AlquilerEquipo(Servicio):

    def __init__(self, codigo, nombre, precio_base, tipo_equipo):
        super().__init__(codigo, nombre, precio_base)

        if not tipo_equipo or not isinstance(tipo_equipo, str):
            raise DatosInvalidosError("Debe indicar el tipo de equipo.")

        self.tipo_equipo = tipo_equipo

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise DatosInvalidosError("Los días de alquiler deben ser positivos.")

        if not self.disponible:
            raise ServicioNoDisponibleError("El equipo no está disponible.")

        return True

    def describir_servicio(self):
        return (
            f"Alquiler de equipo: {self.nombre}. "
            f"Tipo: {self.tipo_equipo}."
        )

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)
        validar_condiciones_pago(descuento, impuesto)

        subtotal = self.precio_base * duracion
        return aplicar_condiciones(subtotal, descuento, impuesto)


class AsesoriaEspecializada(Servicio):

    def __init__(self, codigo, nombre, precio_base, especialidad):
        super().__init__(codigo, nombre, precio_base)

        if not especialidad or not isinstance(especialidad, str):
            raise DatosInvalidosError("Debe indicar la especialidad.")

        self.especialidad = especialidad

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise DatosInvalidosError("Las horas de asesoría deben ser positivas.")

        if not self.disponible:
            raise ServicioNoDisponibleError("La asesoría no está disponible.")

        return True

    def describir_servicio(self):
        return (
            f"Asesoría especializada: {self.nombre}. "
            f"Especialidad: {self.especialidad}."
        )

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)
        validar_condiciones_pago(descuento, impuesto)

        subtotal = self.precio_base * duracion
        return aplicar_condiciones(subtotal, descuento, impuesto)


def validar_condiciones_pago(descuento, impuesto):
    if not isinstance(descuento, (int, float)) or isinstance(descuento, bool) or not 0 <= descuento <= 100:
        raise DatosInvalidosError("El descuento debe estar entre 0 y 100.")

    if not isinstance(impuesto, (int, float)) or isinstance(impuesto, bool) or not 0 <= impuesto <= 100:
        raise DatosInvalidosError("El impuesto debe estar entre 0 y 100.")


def aplicar_condiciones(subtotal, descuento, impuesto):
    total_con_descuento = subtotal * (1 - descuento / 100)
    total = total_con_descuento * (1 + impuesto / 100)
    return round(total, 2)
