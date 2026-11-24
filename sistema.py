import logging
from pathlib import Path
from excepciones import ClienteDuplicadoError, ClienteNoEncontradoError, ErrorValidacion, ServicioNoDisponibleError
from reservas import Reserva

class SistemaSoftwareFJ:
    def __init__(self):
        self.clientes, self.servicios, self.reservas = [], [], []
        carpeta = Path(__file__).parent / "logs"
        carpeta.mkdir(exist_ok=True)
        logging.basicConfig(filename=carpeta / "software_fj.log", level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s", encoding="utf-8", force=True)
        self.logger = logging.getLogger("SoftwareFJ")
        self.logger.info("Sistema iniciado.")

    def registrar_cliente(self, cliente):
        if any(c.identificador == cliente.identificador for c in self.clientes):
            raise ClienteDuplicadoError("El cliente ya está registrado.")
        self.clientes.append(cliente)
        self.logger.info("Cliente registrado: %s", cliente.identificador)
        return cliente

    def buscar_cliente(self, identificacion):
        for c in self.clientes:
            if c.identificador == str(identificacion): return c
        raise ClienteNoEncontradoError(f"Cliente {identificacion} no encontrado.")

    def agregar_servicio(self, servicio):
        if any(s.codigo == servicio.codigo for s in self.servicios):
            raise ErrorValidacion("Código de servicio duplicado.")
        self.servicios.append(servicio)
        self.logger.info("Servicio agregado: %s", servicio.codigo)
        return servicio

    def buscar_servicio(self, codigo):
        for s in self.servicios:
            if s.codigo == str(codigo): return s
        raise ServicioNoDisponibleError(f"Servicio {codigo} no encontrado.")

    def crear_reserva(self, codigo, id_cliente, cod_servicio, duracion, parametros=None, descuento=0, impuesto=0.19):
        try:
            cliente = self.buscar_cliente(id_cliente)
            servicio = self.buscar_servicio(cod_servicio)
            reserva = Reserva(codigo, cliente, servicio, duracion, parametros, descuento, impuesto)
        except (ClienteNoEncontradoError, ServicioNoDisponibleError) as error:
            self.logger.exception("Error en validación de reserva.")
            raise ErrorValidacion("No fue posible validar la reserva.") from error
        else:
            self.reservas.append(reserva)
            self.logger.info("Reserva creada: %s", codigo)
            return reserva
        finally:
            self.logger.info("Terminó el intento de crear reserva: %s", codigo)

    def listar_clientes(self): return [c.mostrar_informacion() for c in self.clientes]
    def listar_servicios(self): return [s.describir() for s in self.servicios]
    def listar_reservas(self): return [r.mostrar_informacion() for r in self.reservas]
