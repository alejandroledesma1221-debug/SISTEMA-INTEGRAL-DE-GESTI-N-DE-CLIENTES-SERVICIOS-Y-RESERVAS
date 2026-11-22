"""
Módulo de excepciones personalizadas para el Sistema Integral de Gestión
de Clientes, Servicios y Reservas - Software FJ.
"""


class SistemaFJError(Exception):
    """Excepción base para todos los errores controlados del sistema Software FJ."""

    def __init__(self, mensaje: str, codigo_error: str = "ERR_GENERAL"):
        self.mensaje = mensaje
        self.codigo_error = codigo_error
        super().__init__(f"[{codigo_error}] {mensaje}")


class DatoInvalidoError(SistemaFJError):
    """Se lanza cuando un dato ingresado no cumple con el formato o dominio esperado."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR_DATO_INVALIDO")


class ParametroFaltanteError(SistemaFJError):
    """Se lanza cuando falta un parámetro obligatorio en una entidad o servicio."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR_PARAMETRO_FALTANTE")


class OperacionNoPermitidaError(SistemaFJError):
    """Se lanza cuando se intenta ejecutar una acción inválida sobre el estado actual."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR_OPERACION_NO_PERMITIDA")


class ServicioNoDisponibleError(SistemaFJError):
    """Se lanza cuando el servicio solicitado no tiene cupo, stock o disponibilidad."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR_SERVICIO_NO_DISPONIBLE")


class ReservaError(SistemaFJError):
    """Se lanza cuando ocurre un fallo al crear, confirmar, cancelar o calcular una reserva."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR_RESERVA")


class CalculoInconsistenteError(SistemaFJError):
    """Se lanza cuando el resultado de un cálculo financiero o de tarifa es inconsistente."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR_CALCULO_INCONSISTENTE")
