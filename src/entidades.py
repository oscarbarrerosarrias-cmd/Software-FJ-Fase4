
"""
Proyecto: Software FJ
Archivo: entidades.py
Descripción: Clase abstracta Entidad.
"""

from abc import ABC, abstractmethod


class Entidad(ABC):

    def __init__(self, identificador):
        if not isinstance(identificador, str) or not identificador.strip():
            raise ValueError("El identificador es obligatorio.")

        self._identificador = identificador.strip()

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def mostrar_informacion(self):
        """Método obligatorio para las clases derivadas."""
        pass
