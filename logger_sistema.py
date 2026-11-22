"""
Módulo de registro de eventos y errores en archivo de logs (sin base de datos).
"""

from datetime import datetime
import traceback


class LoggerSistema:
    """Gestiona la escritura de eventos y excepciones en un archivo de texto plano."""

    def __init__(self, ruta_archivo: str = "logs_software_fj.log"):
        self.ruta_archivo = ruta_archivo

    def _escribir(self, nivel: str, mensaje: str) -> None:
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{marca_tiempo}] [{nivel}] {mensaje}\n"
        try:
            with open(self.ruta_archivo, "a", encoding="utf-8") as archivo:
                archivo.write(linea)
        except OSError as error_io:
            print(f"[ALERTA LOG] No se pudo escribir en {self.ruta_archivo}: {error_io}")

    def registrar_evento(self, mensaje: str) -> None:
        """Registra una operación o evento informativo del sistema."""
        self._escribir("INFO", mensaje)

    def registrar_advertencia(self, mensaje: str) -> None:
        """Registra una advertencia controlada."""
        self._escribir("WARNING", mensaje)

    def registrar_error(self, error: Exception, contexto: str = "") -> None:
        """Registra una excepción junto con su causa encadenada si existe."""
        detalle_causa = ""
        if error.__cause__ is not None:
            detalle_causa = f" | Causa original: {type(error.__cause__).__name__}: {error.__cause__}"
        prefijo = f"({contexto}) " if contexto else ""
        self._escribir("ERROR", f"{prefijo}{type(error).__name__}: {error}{detalle_causa}")
