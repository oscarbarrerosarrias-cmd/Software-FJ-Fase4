
"""
Proyecto: Software FJ
Archivo: clientes.py
Descripción: Gestión de clientes.
"""

from .entidades import Entidad
from .excepciones import (
    DatosInvalidosError,
    ClienteNoEncontradoError
)


class Cliente(Entidad):

    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)

        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidosError("El nombre no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or "@" not in valor:
            raise DatosInvalidosError("El correo electrónico no es válido.")
        if "." not in valor.split("@")[-1]:
            raise DatosInvalidosError("El dominio del correo no es válido.")
        self.__correo = valor.strip().lower()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        telefono = str(valor).strip()
        if not telefono.isdigit() or len(telefono) < 7:
            raise DatosInvalidosError("El teléfono debe tener al menos 7 dígitos.")
        self.__telefono = telefono

    def mostrar_informacion(self):
        return (
            f"ID: {self.identificador} | "
            f"Nombre: {self.nombre} | "
            f"Correo: {self.correo} | "
            f"Teléfono: {self.telefono}"
        )


class GestorClientes:

    def __init__(self):
        self.clientes = []

    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("El objeto no es un cliente válido.")

        if self.buscar_cliente(cliente.identificador):
            raise DatosInvalidosError("Ya existe un cliente con ese ID.")

        self.clientes.append(cliente)
        return "Cliente registrado correctamente."

    def buscar_cliente(self, identificador):
        for cliente in self.clientes:
            if cliente.identificador == identificador:
                return cliente
        return None

    def obtener_cliente(self, identificador):
        cliente = self.buscar_cliente(identificador)
        if cliente is None:
            raise ClienteNoEncontradoError(
                f"No existe el cliente {identificador}."
            )
        return cliente

    def listar_clientes(self):
        return self.clientes

    def eliminar_cliente(self, identificador):
        cliente = self.obtener_cliente(identificador)
        self.clientes.remove(cliente)
        return "Cliente eliminado correctamente."
