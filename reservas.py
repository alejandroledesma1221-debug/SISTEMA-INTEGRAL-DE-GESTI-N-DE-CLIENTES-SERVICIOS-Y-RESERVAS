"""
Módulo de gestión de reservas y controlador principal de Software FJ.
Aplica try/except, try/except/else, try/except/finally y encadenamiento de excepciones.
"""

from entidades import EntidadSistema, Cliente
from servicios import Servicio, AlquilerEquipo
from logger_sistema import LoggerSistema
from excepciones import (
    SistemaFJError,
    DatoInvalidoError,
    ParametroFaltanteError,
    OperacionNoPermitidaError,
    ReservaError,
)


class Reserva(EntidadSistema):
    """Integra cliente, servicio, duración y ciclo de vida de una reserva."""

    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA")

    def __init__(
        self,
        id_reserva: str,
        cliente: Cliente,
        servicio: Servicio,
        duracion_horas: int,
        logger: LoggerSistema,
        parametros_extra: dict | None = None,
    ):
        super().__init__(id_reserva)
        self.logger = logger
        self.parametros_extra = parametros_extra or {}

        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("La reserva requiere una instancia válida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("La reserva requiere una instancia válida de Servicio.")
        if not isinstance(duracion_horas, int) or duracion_horas <= 0:
            raise DatoInvalidoError("La duración de la reserva debe ser un número entero positivo de horas.")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion_horas = duracion_horas
        self.estado = "PENDIENTE"
        self.costo_total = 0.0

        # Validar reglas polimórficas del servicio antes de habilitar la reserva
        self.servicio.validar_parametros(self.duracion_horas, **self.parametros_extra)
        self.costo_total = self.servicio.calcular_costo_total(self.duracion_horas)

    def confirmar(self, incluir_iva: bool = True, descuento_porcentaje: float = 0.0) -> None:
        """Confirma la reserva usando try/except/else y encadenamiento de excepciones."""
        try:
            if self.estado != "PENDIENTE":
                raise OperacionNoPermitidaError(
                    f"No se puede confirmar la reserva {self.id_entidad} porque su estado es '{self.estado}'."
                )
            self.servicio.validar_parametros(self.duracion_horas, **self.parametros_extra)
            self.costo_total = self.servicio.calcular_costo_total(
                self.duracion_horas,
                incluir_iva=incluir_iva,
                descuento_porcentaje=descuento_porcentaje,
            )
            if isinstance(self.servicio, AlquilerEquipo):
                cantidad = self.parametros_extra.get("cantidad", 1)
                self.servicio.reservar_unidad(cantidad)
        except SistemaFJError as exc:
            self.logger.registrar_error(exc, contexto=f"Confirmación de reserva {self.id_entidad}")
            raise ReservaError(f"Fallo al confirmar la reserva {self.id_entidad}.") from exc
        else:
            self.estado = "CONFIRMADA"
            self.logger.registrar_evento(
                f"Reserva {self.id_entidad} CONFIRMADA para {self.cliente.nombre} | "
                f"Servicio: {self.servicio.nombre} | Total: ${self.costo_total:,.2f}"
            )

    def cancelar(self, motivo: str = "Solicitud del cliente") -> None:
        """Cancela la reserva y libera recursos si corresponde."""
        try:
            if self.estado in ("CANCELADA", "PROCESADA"):
                raise OperacionNoPermitidaError(
                    f"La reserva {self.id_entidad} no puede cancelarse desde el estado '{self.estado}'."
                )
            estado_anterior = self.estado
            if estado_anterior == "CONFIRMADA" and isinstance(self.servicio, AlquilerEquipo):
                cantidad = self.parametros_extra.get("cantidad", 1)
                self.servicio.liberar_unidad(cantidad)
            self.estado = "CANCELADA"
        except SistemaFJError as exc:
            self.logger.registrar_error(exc, contexto=f"Cancelación de reserva {self.id_entidad}")
            raise ReservaError(f"Error al cancelar la reserva {self.id_entidad}.") from exc
        else:
            self.logger.registrar_evento(
                f"Reserva {self.id_entidad} CANCELADA. Motivo: {motivo}"
            )

    def procesar(self) -> str:
        """Procesa/finaliza la reserva usando try/except/finally para auditoría garantizada."""
        resultado = ""
        try:
            if self.estado != "CONFIRMADA":
                raise OperacionNoPermitidaError(
                    f"Solo se pueden procesar reservas CONFIRMADAS. Estado actual: '{self.estado}'."
                )
            self.estado = "PROCESADA"
            resultado = (
                f"Factura emitida para reserva {self.id_entidad} | Cliente: {self.cliente.nombre} | "
                f"Servicio: {self.servicio.nombre} ({self.duracion_horas}h) | Total pagado: ${self.costo_total:,.2f}"
            )
            self.logger.registrar_evento(f"Reserva {self.id_entidad} PROCESADA exitosamente.")
            return resultado
        except SistemaFJError as exc:
            self.logger.registrar_error(exc, contexto=f"Procesamiento de reserva {self.id_entidad}")
            raise ReservaError(f"No fue posible procesar la reserva {self.id_entidad}.") from exc
        finally:
            self.logger.registrar_evento(
                f"Auditoría de ejecución finalizada para reserva {self.id_entidad} (Estado: {self.estado})."
            )

    def validar(self) -> bool:
        return self.cliente.validar() and self.servicio.validar() and self.duracion_horas > 0

    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self.id_entidad}] Estado: {self.estado} | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | Duración: {self.duracion_horas}h | Total: ${self.costo_total:,.2f}"
        )


class GestorSoftwareFJ:
    """Controlador central en memoria (listas) que coordina clientes, servicios y reservas."""

    def __init__(self, archivo_log: str = "logs_software_fj.log"):
        self.clientes: list[Cliente] = []
        self.servicios: list[Servicio] = []
        self.reservas: list[Reserva] = []
        self.logger = LoggerSistema(archivo_log)
        self.logger.registrar_evento("Sistema Software FJ inicializado correctamente.")

    def registrar_cliente(self, cliente: Cliente) -> bool:
        try:
            if any(c.id_entidad == cliente.id_entidad or c.documento == cliente.documento for c in self.clientes):
                raise DatoInvalidoError(
                    f"Ya existe un cliente registrado con ID '{cliente.id_entidad}' o documento '{cliente.documento}'."
                )
            cliente.validar()
            self.clientes.append(cliente)
            self.logger.registrar_evento(f"Cliente registrado: {cliente.obtener_resumen()}")
            return True
        except SistemaFJError as exc:
            self.logger.registrar_error(exc, contexto="Registro de cliente")
            print(f"  [ERROR CONTROLADO] {exc}")
            return False

    def registrar_servicio(self, servicio: Servicio) -> bool:
        try:
            if any(s.id_entidad == servicio.id_entidad for s in self.servicios):
                raise DatoInvalidoError(f"Ya existe un servicio con ID '{servicio.id_entidad}'.")
            servicio.validar()
            self.servicios.append(servicio)
            self.logger.registrar_evento(f"Servicio registrado: {servicio.describir_servicio()}")
            return True
        except SistemaFJError as exc:
            self.logger.registrar_error(exc, contexto="Registro de servicio")
            print(f"  [ERROR CONTROLADO] {exc}")
            return False

    def crear_reserva(
        self,
        id_reserva: str,
        id_cliente: str,
        id_servicio: str,
        duracion_horas: int,
        parametros_extra: dict | None = None,
    ) -> Reserva | None:
        try:
            if any(r.id_entidad == id_reserva for r in self.reservas):
                raise DatoInvalidoError(f"Ya existe una reserva con ID '{id_reserva}'.")

            cliente = next((c for c in self.clientes if c.id_entidad == id_cliente), None)
            if cliente is None:
                raise ParametroFaltanteError(f"No se encontró el cliente con ID '{id_cliente}'.")

            servicio = next((s for s in self.servicios if s.id_entidad == id_servicio), None)
            if servicio is None:
                raise ParametroFaltanteError(f"No se encontró el servicio con ID '{id_servicio}'.")

            nueva_reserva = Reserva(
                id_reserva=id_reserva,
                cliente=cliente,
                servicio=servicio,
                duracion_horas=duracion_horas,
                logger=self.logger,
                parametros_extra=parametros_extra,
            )
            self.reservas.append(nueva_reserva)
            self.logger.registrar_evento(f"Reserva creada en estado PENDIENTE: {nueva_reserva.obtener_resumen()}")
            return nueva_reserva
        except SistemaFJError as exc:
            self.logger.registrar_error(exc, contexto=f"Creación de reserva {id_reserva}")
            print(f"  [ERROR CONTROLADO] {exc}")
            return None
