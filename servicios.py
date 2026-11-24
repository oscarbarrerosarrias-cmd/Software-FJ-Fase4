from abc import ABC, abstractmethod
from excepciones import ErrorValidacion, ServicioNoDisponibleError, ErrorCalculoError

class Servicio(ABC):
    def __init__(self, codigo, nombre, tarifa, disponible=True):
        if not codigo or not nombre or not isinstance(tarifa, (int, float)) or tarifa <= 0:
            raise ErrorValidacion("Código, nombre y tarifa positiva son obligatorios.")
        self._codigo, self._nombre, self._tarifa = str(codigo), str(nombre), float(tarifa)
        self.disponible = bool(disponible)

    @property
    def codigo(self): return self._codigo
    @property
    def nombre(self): return self._nombre

    def validar_disponibilidad(self):
        if not self.disponible:
            raise ServicioNoDisponibleError(f"Servicio no disponible: {self.nombre}")

    @abstractmethod
    def validar_parametros(self, **kwargs): pass
    @abstractmethod
    def describir(self): pass
    @abstractmethod
    def calcular_costo(self, duracion, descuento=0, impuesto=0.19): pass

    def calcular_costo_simple(self, duracion):
        return self.calcular_costo(duracion)
    def calcular_costo_personalizado(self, duracion, descuento=0, impuesto=0.19):
        return self.calcular_costo(duracion, descuento, impuesto)

    def _validar_calculo(self, duracion, descuento, impuesto):
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ErrorCalculoError("La duración debe ser positiva.")
        if not 0 <= descuento <= 1 or not 0 <= impuesto <= 1:
            raise ErrorCalculoError("Descuento e impuesto deben estar entre 0 y 1.")


class ReservaSala(Servicio):
    def __init__(self, codigo, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(codigo, nombre, tarifa_hora, disponible)
        self.capacidad = capacidad
    def validar_parametros(self, **kwargs):
        personas = kwargs.get("personas")
        if not isinstance(personas, int) or personas < 1 or personas > self.capacidad:
            raise ErrorValidacion("Cantidad de personas inválida para la capacidad de la sala.")
    def describir(self): return f"Sala {self.nombre}, capacidad {self.capacidad}"
    def calcular_costo(self, duracion, descuento=0, impuesto=0.19):
        self._validar_calculo(duracion, descuento, impuesto)
        return round(self._tarifa * duracion * (1-descuento) * (1+impuesto), 2)


class AlquilerEquipo(Servicio):
    def __init__(self, codigo, nombre, tarifa_dia, cantidad_disponible, disponible=True):
        super().__init__(codigo, nombre, tarifa_dia, disponible)
        self.cantidad_disponible = cantidad_disponible
    def validar_parametros(self, **kwargs):
        cantidad = kwargs.get("cantidad")
        if not isinstance(cantidad, int) or cantidad < 1 or cantidad > self.cantidad_disponible:
            raise ServicioNoDisponibleError("Cantidad de equipos no disponible.")
    def describir(self): return f"Equipo {self.nombre}, unidades {self.cantidad_disponible}"
    def calcular_costo(self, duracion, descuento=0, impuesto=0.19):
        self._validar_calculo(duracion, descuento, impuesto)
        return round(self._tarifa * duracion * (1-descuento) * (1+impuesto), 2)


class AsesoriaEspecializada(Servicio):
    def __init__(self, codigo, nombre, tarifa_hora, especialidad, disponible=True):
        super().__init__(codigo, nombre, tarifa_hora, disponible)
        if not especialidad: raise ErrorValidacion("La especialidad es obligatoria.")
        self.especialidad = especialidad
    def validar_parametros(self, **kwargs):
        if not kwargs.get("tema"): raise ErrorValidacion("Debe indicar el tema de la asesoría.")
    def describir(self): return f"Asesoría {self.nombre}, especialidad {self.especialidad}"
    def calcular_costo(self, duracion, descuento=0, impuesto=0.19):
        self._validar_calculo(duracion, descuento, impuesto)
        return round(self._tarifa * duracion * (1-descuento) * (1+impuesto), 2)
