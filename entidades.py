"""
Módulo base con la clase abstracta general del sistema y la clase Cliente.
Implementa abstracción, herencia y encapsulación con validaciones estrictas.
"""

from abc import ABC, abstractmethod
from datetime import datetime
import re
from excepciones import DatoInvalidoError, ParametroFaltanteError


class EntidadSistema(ABC):
    """Clase abstracta base para todas las entidades gestionadas por Software FJ."""

    def __init__(self, id_entidad: str):
        self.id_entidad = id_entidad
        self._fecha_creacion = datetime.now()
        self._activo = True

    @property
    def id_entidad(self) -> str:
        return self._id_entidad

    @id_entidad.setter
    def id_entidad(self, valor: str) -> None:
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El identificador de la entidad es obligatorio.")
        self._id_entidad = str(valor).strip()

    @property
    def fecha_creacion(self) -> datetime:
        return self._fecha_creacion

    @property
    def activo(self) -> bool:
        return self._activo

    @activo.setter
    def activo(self, estado: bool) -> None:
        if not isinstance(estado, bool):
            raise DatoInvalidoError("El estado activo debe ser un valor booleano.")
        self._activo = estado

    @abstractmethod
    def validar(self) -> bool:
        """Valida la integridad interna de la entidad."""

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Retorna una descripción legible de la entidad."""


class Cliente(EntidadSistema):
    """Representa un cliente de Software FJ con encapsulación y validaciones."""

    def __init__(self, id_cliente: str, nombre: str, documento: str, correo: str, telefono: str):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El nombre del cliente no puede estar vacío.")
        nombre_limpio = str(valor).strip()
        if len(nombre_limpio) < 3 or any(char.isdigit() for char in nombre_limpio):
            raise DatoInvalidoError(f"Nombre de cliente inválido: '{valor}'.")
        self._nombre = nombre_limpio

    @property
    def documento(self) -> str:
        return self._documento

    @documento.setter
    def documento(self, valor: str) -> None:
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El documento de identidad es obligatorio.")
        doc_limpio = str(valor).strip()
        if not doc_limpio.isdigit() or not (6 <= len(doc_limpio) <= 12):
            raise DatoInvalidoError(f"Documento inválido '{valor}'. Debe tener entre 6 y 12 dígitos.")
        self._documento = doc_limpio

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El correo electrónico es obligatorio.")
        correo_limpio = str(valor).strip()
        patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.match(patron, correo_limpio):
            raise DatoInvalidoError(f"Formato de correo electrónico inválido: '{valor}'.")
        self._correo = correo_limpio

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El teléfono de contacto es obligatorio.")
        tel_limpio = str(valor).strip()
        if not tel_limpio.isdigit() or not (7 <= len(tel_limpio) <= 10):
            raise DatoInvalidoError(f"Teléfono inválido '{valor}'. Debe contener entre 7 y 10 dígitos.")
        self._telefono = tel_limpio

    def validar(self) -> bool:
        return bool(self._id_entidad and self._nombre and self._documento and self._correo and self._telefono)

    def obtener_resumen(self) -> str:
        return f"Cliente [{self.id_entidad}] {self.nombre} | Doc: {self.documento} | Email: {self.correo}"
