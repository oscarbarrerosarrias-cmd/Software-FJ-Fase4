
"""
PROYECTO: SOFTWARE FJ
Sistema Integral de Gestión de Clientes, Servicios y Reservas.

Curso: Programación
Código: 213023
Universidad Nacional Abierta y a Distancia - UNAD
"""

import logging
from pathlib import Path

from src.clientes import Cliente, GestorClientes
from src.servicios import (
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada
)
from src.reservas import Reserva, GestorReservas
from src.excepciones import (
    ErrorSistema,
    DatosInvalidosError,
    ServicioNoDisponibleError
)


# =====================================================
# CONFIGURACIÓN DEL SISTEMA DE REGISTRO DE EVENTOS
# =====================================================

CARPETA_LOGS = Path(__file__).resolve().parent / "logs"
CARPETA_LOGS.mkdir(exist_ok=True)

ARCHIVO_LOG = CARPETA_LOGS / "sistema.log"

logging.basicConfig(
    filename=ARCHIVO_LOG,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
    force=True
)

logger = logging.getLogger("SoftwareFJ")


# =====================================================
# INICIALIZACIÓN DE LOS GESTORES
# =====================================================

gestor_clientes = GestorClientes()
gestor_reservas = GestorReservas()

servicios = []


# =====================================================
# FUNCIONES AUXILIARES
# =====================================================

def leer_texto(mensaje):
    valor = input(mensaje).strip()

    if not valor:
        raise DatosInvalidosError("El campo no puede estar vacío.")

    return valor


def leer_numero(mensaje):
    try:
        valor = float(input(mensaje))

        if valor <= 0:
            raise ValueError("El número debe ser positivo.")

        return valor

    except ValueError as error:
        raise DatosInvalidosError(
            "Debe ingresar un número válido y positivo."
        ) from error


def buscar_servicio(codigo):
    for servicio in servicios:
        if servicio.codigo == codigo:
            return servicio

    raise DatosInvalidosError(
        f"No existe el servicio con código {codigo}."
    )


def registrar_servicio_en_lista(servicio):
    if any(s.codigo == servicio.codigo for s in servicios):
        raise DatosInvalidosError(
            "Ya existe un servicio con ese código."
        )

    servicios.append(servicio)
    logger.info("Servicio %s registrado.", servicio.codigo)


def ejecutar_operacion(descripcion, funcion):
    print(f"\n{descripcion}")

    try:
        resultado = funcion()

    except ErrorSistema as error:
        print(f"ERROR CONTROLADO: {error}")
        logger.error("%s: %s", descripcion, error)

    except Exception:
        logger.exception("Error inesperado en: %s", descripcion)
        print("Se presentó un error inesperado. El sistema continúa.")

    else:
        print(f"RESULTADO: {resultado}")
        logger.info("Operación exitosa: %s", descripcion)

    finally:
        print("Operación finalizada.\n")


# =====================================================
# GESTIÓN DE CLIENTES
# =====================================================

def registrar_cliente():
    print("\n--- REGISTRO DE CLIENTE ---")

    identificador = leer_texto("Identificación: ")
    nombre = leer_texto("Nombre completo: ")
    correo = leer_texto("Correo electrónico: ")
    telefono = leer_texto("Teléfono: ")

    cliente = Cliente(
        identificador,
        nombre,
        correo,
        telefono
    )

    mensaje = gestor_clientes.registrar_cliente(cliente)
    return mensaje


def consultar_clientes():
    print("\n--- LISTADO DE CLIENTES ---")

    clientes = gestor_clientes.listar_clientes()

    if not clientes:
        print("No hay clientes registrados.")
        return

    for cliente in clientes:
        print(cliente.mostrar_informacion())


def eliminar_cliente():
    identificador = leer_texto("Identificación del cliente: ")
    return gestor_clientes.eliminar_cliente(identificador)


# =====================================================
# GESTIÓN DE SERVICIOS
# =====================================================

def registrar_servicio():
    print("\n--- REGISTRO DE SERVICIOS ---")
    print("1. Reserva de salas")
    print("2. Alquiler de equipos")
    print("3. Asesorías especializadas")

    opcion = input("Seleccione el tipo de servicio: ").strip()

    codigo = leer_texto("Código del servicio: ")
    nombre = leer_texto("Nombre del servicio: ")
    precio = leer_numero("Precio por unidad: ")

    if opcion == "1":
        capacidad = int(leer_numero("Capacidad de la sala: "))

        servicio = ReservaSala(
            codigo,
            nombre,
            precio,
            capacidad
        )

    elif opcion == "2":
        tipo = leer_texto("Tipo de equipo: ")

        servicio = AlquilerEquipo(
            codigo,
            nombre,
            precio,
            tipo
        )

    elif opcion == "3":
        especialidad = leer_texto("Especialidad: ")

        servicio = AsesoriaEspecializada(
            codigo,
            nombre,
            precio,
            especialidad
        )

    else:
        raise DatosInvalidosError("Tipo de servicio incorrecto.")

    registrar_servicio_en_lista(servicio)

    return "Servicio registrado correctamente."


def consultar_servicios():
    print("\n--- SERVICIOS REGISTRADOS ---")

    if not servicios:
        print("No existen servicios registrados.")
        return

    for servicio in servicios:
        print(servicio.describir_servicio())
        print(
            f"Código: {servicio.codigo} | "
            f"Precio: ${servicio.precio_base:,.2f} | "
            f"Disponible: {servicio.disponible}"
        )


# =====================================================
# GESTIÓN DE RESERVAS
# =====================================================

def crear_reserva():
    print("\n--- CREAR RESERVA ---")

    codigo = leer_texto("Código de reserva: ")
    identificacion = leer_texto("Identificación del cliente: ")
    codigo_servicio = leer_texto("Código del servicio: ")
    duracion = leer_numero("Duración: ")

    cliente = gestor_clientes.obtener_cliente(identificacion)
    servicio = buscar_servicio(codigo_servicio)

    reserva = Reserva(
        codigo,
        cliente,
        servicio,
        duracion
    )

    return gestor_reservas.crear_reserva(reserva)


def confirmar_reserva():
    codigo = leer_texto("Código de reserva: ")
    return gestor_reservas.confirmar_reserva(codigo)


def cancelar_reserva():
    codigo = leer_texto("Código de reserva: ")
    return gestor_reservas.cancelar_reserva(codigo)


def procesar_reserva():
    codigo = leer_texto("Código de reserva: ")
    return gestor_reservas.procesar_reserva(codigo)


def consultar_reservas():
    print("\n--- RESERVAS REGISTRADAS ---")

    reservas = gestor_reservas.listar_reservas()

    if not reservas:
        print("No existen reservas registradas.")
        return

    for reserva in reservas:
        print(reserva.mostrar_informacion())


# =====================================================
# DEMOSTRACIÓN DE 12 OPERACIONES
# =====================================================

def ejecutar_demostracion():

    print("\n" + "=" * 60)
    print("DEMOSTRACIÓN DE OPERACIONES - SOFTWARE FJ")
    print("=" * 60)

    def operacion_1():
        cliente = Cliente(
            "1001",
            "Carlos Pérez",
            "carlos@gmail.com",
            "3001234567"
        )
        return gestor_clientes.registrar_cliente(cliente)

    def operacion_2():
        cliente = Cliente(
            "1002",
            "María Rodríguez",
            "maria@gmail.com",
            "3101234567"
        )
        return gestor_clientes.registrar_cliente(cliente)

    def operacion_3():
        return gestor_clientes.obtener_cliente("1001").mostrar_informacion()

    def operacion_4():
        return gestor_clientes.registrar_cliente(
            Cliente(
                "1003",
                "",
                "incorrecto",
                "123"
            )
        )

    def operacion_5():
        servicio = ReservaSala(
            "S001",
            "Sala de reuniones",
            50000,
            15
        )
        registrar_servicio_en_lista(servicio)
        return servicio.describir_servicio()

    def operacion_6():
        servicio = AlquilerEquipo(
            "E001",
            "Computador portátil",
            30000,
            "Portátil"
        )
        registrar_servicio_en_lista(servicio)
        return servicio.describir_servicio()

    def operacion_7():
        servicio = AsesoriaEspecializada(
            "A001",
            "Asesoría tecnológica",
            80000,
            "Tecnología"
        )
        registrar_servicio_en_lista(servicio)
        return servicio.describir_servicio()

    def operacion_8():
        return ReservaSala(
            "S002",
            "Sala incorrecta",
            -5000,
            10
        )

    def operacion_9():
        reserva = Reserva(
            "R001",
            gestor_clientes.obtener_cliente("1001"),
            buscar_servicio("S001"),
            2
        )
        return gestor_reservas.crear_reserva(reserva)

    def operacion_10():
        return gestor_reservas.confirmar_reserva("R001")

    def operacion_11():
        reserva = Reserva(
            "R002",
            gestor_clientes.obtener_cliente("1002"),
            buscar_servicio("E001"),
            3
        )
        gestor_reservas.crear_reserva(reserva)
        return gestor_reservas.confirmar_reserva("R002")

    def operacion_12():
        servicio = buscar_servicio("A001")
        servicio.cambiar_disponibilidad(False)

        try:
            servicio.calcular_costo(2)
        except ServicioNoDisponibleError as error:
            raise DatosInvalidosError(
                "No fue posible calcular el costo porque el servicio no está disponible."
            ) from error

    operaciones = [
        ("1. Registrar cliente válido", operacion_1),
        ("2. Registrar segundo cliente", operacion_2),
        ("3. Consultar cliente", operacion_3),
        ("4. Registrar cliente inválido", operacion_4),
        ("5. Crear servicio de sala", operacion_5),
        ("6. Crear servicio de equipo", operacion_6),
        ("7. Crear servicio de asesoría", operacion_7),
        ("8. Crear servicio con precio incorrecto", operacion_8),
        ("9. Crear reserva", operacion_9),
        ("10. Confirmar reserva", operacion_10),
        ("11. Crear y confirmar otra reserva", operacion_11),
        ("12. Intentar utilizar servicio no disponible", operacion_12)
    ]

    for descripcion, funcion in operaciones:
        ejecutar_operacion(descripcion, funcion)

    print("=" * 60)
    print("DEMOSTRACIÓN FINALIZADA")
    print("El sistema continúa funcionando después de los errores.")
    print("=" * 60)


# =====================================================
# MENÚ PRINCIPAL
# =====================================================

def mostrar_menu():

    print("\n")
    print("=" * 55)
    print("       SISTEMA INTEGRAL SOFTWARE FJ")
    print("=" * 55)
    print("1. Registrar cliente")
    print("2. Consultar clientes")
    print("3. Eliminar cliente")
    print("4. Registrar servicio")
    print("5. Consultar servicios")
    print("6. Crear reserva")
    print("7. Confirmar reserva")
    print("8. Cancelar reserva")
    print("9. Procesar reserva")
    print("10. Consultar reservas")
    print("11. Ejecutar demostración de 12 operaciones")
    print("12. Salir")
    print("=" * 55)


def main():

    logger.info("Sistema Software FJ iniciado.")

    print("\nBienvenido al Sistema Integral Software FJ")

    try:
        while True:

            mostrar_menu()

            opcion = input("Seleccione una opción: ").strip()

            opciones = {
                "1": registrar_cliente,
                "2": consultar_clientes,
                "3": eliminar_cliente,
                "4": registrar_servicio,
                "5": consultar_servicios,
                "6": crear_reserva,
                "7": confirmar_reserva,
                "8": cancelar_reserva,
                "9": procesar_reserva,
                "10": consultar_reservas,
                "11": ejecutar_demostracion
            }

            if opcion == "12":
                print("Gracias por utilizar Software FJ.")
                break

            funcion = opciones.get(opcion)

            if funcion is None:
                print("Opción incorrecta. Intente nuevamente.")
                logger.warning("Opción de menú inválida: %s", opcion)
                continue

            ejecutar_operacion(
                "Ejecución de opción " + opcion,
                funcion
            )

    except (KeyboardInterrupt, EOFError):
        print("\nEl programa fue interrumpido por el usuario.")

    finally:
        logger.info("Sistema Software FJ finalizado.")
        print("Registro de eventos actualizado.")


if __name__ == "__main__":
    main()
