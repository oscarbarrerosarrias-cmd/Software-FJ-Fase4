from abc import ABC, abstractmethod
import re
from excepciones import ErrorValidacion

class Entidad(ABC):
    def __init__(self, identificador, nombre):
        if not identificador or not str(identificador).strip():
            raise ErrorValidacion("El identificador es obligatorio.")
        if not nombre or not str(nombre).strip():
            raise ErrorValidacion("El nombre es obligatorio.")
        self._identificador = str(identificador).strip()
        self._nombre = str(nombre).strip()

    @property
    def identificador(self): return self._identificador

    @property
    def nombre(self): return self._nombre

    @abstractmethod
    def mostrar_informacion(self): pass


class Cliente(Entidad):
    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(identificacion, nombre)
        self.__correo = None
        self.__telefono = None
        self.correo = correo
        self.telefono = telefono

    @property
    def correo(self): return self.__correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or not re.fullmatch(r"[\w.+-]+@[\w-]+\.[\w.-]+", valor.strip()):
            raise ErrorValidacion("El correo electrónico no es válido.")
        self.__correo = valor.strip()

    @property
    def telefono(self): return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        valor = str(valor).strip()
        if not valor.isdigit() or not 7 <= len(valor) <= 15:
            raise ErrorValidacion("El teléfono debe tener entre 7 y 15 dígitos.")
        self.__telefono = valor

    def mostrar_informacion(self):
        return f"ID: {self.identificador} | {self.nombre} | {self.correo} | {self.telefono}"
