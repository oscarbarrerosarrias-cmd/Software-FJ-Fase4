from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from sistema import SistemaSoftwareFJ
from excepciones import ErrorSistema

def ejecutar_pruebas():
    sistema = SistemaSoftwareFJ()
    print("\n===== SISTEMA SOFTWARE FJ =====")
    operaciones = 0

    def intento(numero, descripcion, accion):
        nonlocal operaciones
        operaciones += 1
        try:
            resultado = accion()
            print(f"{numero}. {descripcion}: {resultado if resultado is not None else 'Correcto'}")
        except ErrorSistema as error:
            sistema.logger.exception("Operación %s fallida: %s", numero, descripcion)
            print(f"{numero}. {descripcion}: ERROR CONTROLADO -> {error}")

    intento(1, "Registrar cliente válido", lambda: sistema.registrar_cliente(
        Cliente("1001", "Laura Gómez", "laura@gmail.com", "3101234567")).nombre)
    intento(2, "Correo inválido", lambda: Cliente("1002", "Carlos", "correo-mal", "3111234567"))
    intento(3, "Teléfono inválido", lambda: Cliente("1003", "Ana", "ana@gmail.com", "12"))
    intento(4, "Cliente duplicado", lambda: sistema.registrar_cliente(
        Cliente("1001", "Laura", "laura@gmail.com", "3101234567")).nombre)

    sala = ReservaSala("S01", "Sala de reuniones", 50000, 12)
    equipo = AlquilerEquipo("E01", "Video beam", 80000, 4)
    asesoria = AsesoriaEspecializada("A01", "Asesoría tecnológica", 100000, "Desarrollo")
    intento(5, "Crear servicio de sala", lambda: sistema.agregar_servicio(sala).describir())
    intento(6, "Crear servicio de equipo", lambda: sistema.agregar_servicio(equipo).describir())
    intento(7, "Crear servicio de asesoría", lambda: sistema.agregar_servicio(asesoria).describir())
    intento(8, "Validar capacidad incorrecta", lambda: sala.validar_parametros(personas=20))

    r1 = sistema.crear_reserva("R001", "1001", "S01", 2, {"personas": 8}, descuento=0.10)
    intento(9, "Crear reserva de sala", lambda: r1.mostrar_informacion())
    intento(10, "Confirmar reserva", lambda: r1.confirmar())
    intento(11, "Procesar reserva", lambda: r1.procesar())
    intento(12, "Cancelar reserva procesada", lambda: r1.cancelar())

    intento(13, "Cliente inexistente (encadenamiento)", lambda: sistema.crear_reserva(
        "R002", "9999", "A01", 1, {"tema": "Seguridad"}))
    equipo.disponible = False
    intento(14, "Servicio no disponible", lambda: sistema.crear_reserva(
        "R003", "1001", "E01", 1, {"cantidad": 1}))
    intento(15, "Cálculo con tarifa simple", lambda: f"${sala.calcular_costo_simple(1):,.2f}")

    r4 = sistema.crear_reserva("R004", "1001", "A01", 1.5, {"tema": "Ciberseguridad"}, descuento=0.05)
    intento(16, "Cancelar reserva pendiente", lambda: r4.cancelar())

    try:
        print("\nPrueba try/except/else/finally:")
        valor = sala.calcular_costo_personalizado(2, descuento=0.15, impuesto=0.19)
    except ErrorSistema as error:
        print("Error de cálculo:", error)
    else:
        print(f"Resultado del cálculo: ${valor:,.2f}")
    finally:
        print("Bloque finally ejecutado; consulte logs/software_fj.log.")

    print("\n--- RESUMEN ---")
    print("Clientes:", len(sistema.clientes), "| Servicios:", len(sistema.servicios), "| Reservas:", len(sistema.reservas))
    for item in sistema.listar_reservas(): print(item)
    print(f"\nSe ejecutaron {operaciones} operaciones controladas. El programa continúa activo.")

if __name__ == "__main__":
    ejecutar_pruebas()
