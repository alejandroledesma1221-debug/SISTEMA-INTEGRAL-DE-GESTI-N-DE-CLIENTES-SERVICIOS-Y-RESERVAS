"""
Módulo de servicios de Software FJ.
Implementa una clase abstracta Servicio y tres servicios especializados:
- ReservaSala
- AlquilerEquipo
- AsesoriaEspecializada
Incluye polimorfismo, sobrescritura de métodos y sobrecarga simulada para cálculo de costos.
"""

from abc import abstractmethod
from entidades import EntidadSistema
from excepciones import (
    DatoInvalidoError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
)


class Servicio(EntidadSistema):
    """Clase abstracta que define el contrato de todos los servicios de Software FJ."""

    IVA_ESTANDAR = 0.19

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, disponible: bool = True):
        super().__init__(id_servicio)
        self.nombre = nombre
        self.tarifa_hora = tarifa_hora
        self.disponible = disponible

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        self._nombre = str(valor).strip()

    @property
    def tarifa_hora(self) -> float:
        return self._tarifa_hora

    @tarifa_hora.setter
    def tarifa_hora(self, valor: float) -> None:
        if valor is None:
            raise ParametroFaltanteError("La tarifa por hora es obligatoria.")
        try:
            tarifa = float(valor)
        except (TypeError, ValueError) as exc:
            raise DatoInvalidoError(f"La tarifa debe ser numérica, se recibió: {valor}") from exc
        if tarifa <= 0:
            raise DatoInvalidoError("La tarifa por hora debe ser mayor que cero.")
        self._tarifa_hora = tarifa

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise DatoInvalidoError("La disponibilidad debe ser booleana.")
        self._disponible = valor

    @abstractmethod
    def validar_parametros(self, duracion_horas: int, **kwargs) -> None:
        """Valida los parámetros específicos requeridos por cada tipo de servicio."""

    @abstractmethod
    def calcular_costo_base(self, duracion_horas: int) -> float:
        """Calcula el subtotal base según las reglas propias del servicio."""

    @abstractmethod
    def describir_servicio(self) -> str:
        """Retorna una descripción técnica y comercial del servicio."""

    def calcular_costo_total(
        self,
        duracion_horas: int,
        incluir_iva: bool = True,
        descuento_porcentaje: float = 0.0,
        recargo_fijo: float = 0.0,
    ) -> float:
        """
        Método sobrecargado mediante parámetros opcionales para calcular costos:
        - Solo duración: aplica IVA estándar sin descuento ni recargo.
        - Con incluir_iva=False: calcula tarifa exenta de impuesto.
        - Con descuento_porcentaje: aplica descuento comercial antes de IVA.
        - Con recargo_fijo: suma cargos adicionales (logística, soporte, etc.).
        """
        if not isinstance(duracion_horas, int) or duracion_horas <= 0:
            raise DatoInvalidoError("La duración en horas debe ser un entero positivo.")
        if not (0 <= descuento_porcentaje < 100):
            raise DatoInvalidoError("El porcentaje de descuento debe estar entre 0 y 99.9.")
        if recargo_fijo < 0:
            raise DatoInvalidoError("El recargo fijo no puede ser negativo.")

        subtotal = self.calcular_costo_base(duracion_horas)
        monto_descuento = subtotal * (descuento_porcentaje / 100.0)
        base_gravable = subtotal - monto_descuento + recargo_fijo
        impuesto = base_gravable * self.IVA_ESTANDAR if incluir_iva else 0.0
        total = round(base_gravable + impuesto, 2)

        if total <= 0:
            raise CalculoInconsistenteError("El cálculo del costo total arrojó un valor menor o igual a cero.")
        return total

    def validar(self) -> bool:
        return bool(self._id_entidad and self._nombre and self._tarifa_hora > 0)

    def obtener_resumen(self) -> str:
        return self.describir_servicio()


class ReservaSala(Servicio):
    """Servicio especializado para reserva de salas de reuniones, capacitación o coworking."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, capacidad_maxima: int, tiene_videoconferencia: bool = True, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        if not isinstance(capacidad_maxima, int) or capacidad_maxima <= 0:
            raise DatoInvalidoError("La capacidad máxima de la sala debe ser un entero positivo.")
        self.capacidad_maxima = capacidad_maxima
        self.tiene_videoconferencia = bool(tiene_videoconferencia)

    def validar_parametros(self, duracion_horas: int, **kwargs) -> None:
        if not self.disponible:
            raise ServicioNoDisponibleError(f"La sala '{self.nombre}' no se encuentra disponible.")
        if duracion_horas < 1 or duracion_horas > 12:
            raise DatoInvalidoError("La reserva de sala debe durar entre 1 y 12 horas.")
        asistentes = kwargs.get("asistentes", 1)
        if not isinstance(asistentes, int) or asistentes <= 0:
            raise DatoInvalidoError("El número de asistentes debe ser un entero positivo.")
        if asistentes > self.capacidad_maxima:
            raise DatoInvalidoError(
                f"Los asistentes ({asistentes}) superan la capacidad máxima de la sala ({self.capacidad_maxima})."
            )

    def calcular_costo_base(self, duracion_horas: int) -> float:
        costo = self.tarifa_hora * duracion_horas
        # Cargo adicional del 10% si la sala cuenta con sistema avanzado de videoconferencia
        if self.tiene_videoconferencia:
            costo *= 1.10
        return round(costo, 2)

    def describir_servicio(self) -> str:
        extra = "con videoconferencia" if self.tiene_videoconferencia else "estándar"
        estado = "Disponible" if self.disponible else "Ocupada"
        return (
            f"[Sala] {self.nombre} (ID: {self.id_entidad}) | Capacidad: {self.capacidad_maxima} pers. | "
            f"Modalidad: {extra} | Tarifa/h: ${self.tarifa_hora:,.2f} | Estado: {estado}"
        )


class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de hardware y equipos tecnológicos."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, categoria_equipo: str, stock_disponible: int, deposito_seguridad: float = 50000.0):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible=(stock_disponible > 0))
        if not categoria_equipo or not str(categoria_equipo).strip():
            raise ParametroFaltanteError("La categoría del equipo es obligatoria.")
        if not isinstance(stock_disponible, int) or stock_disponible < 0:
            raise DatoInvalidoError("El stock disponible no puede ser negativo.")
        if deposito_seguridad < 0:
            raise DatoInvalidoError("El depósito de seguridad no puede ser negativo.")
        self.categoria_equipo = categoria_equipo.strip()
        self.stock_disponible = stock_disponible
        self.deposito_seguridad = float(deposito_seguridad)

    def validar_parametros(self, duracion_horas: int, **kwargs) -> None:
        cantidad = kwargs.get("cantidad", 1)
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise DatoInvalidoError("La cantidad de equipos a alquilar debe ser al menos 1.")
        if not self.disponible or self.stock_disponible < cantidad:
            raise ServicioNoDisponibleError(
                f"Stock insuficiente para '{self.nombre}'. Disponible: {self.stock_disponible}, solicitado: {cantidad}."
            )
        if duracion_horas < 2:
            raise DatoInvalidoError("El alquiler de equipos requiere una duración mínima de 2 horas.")

    def calcular_costo_base(self, duracion_horas: int) -> float:
        return round((self.tarifa_hora * duracion_horas) + self.deposito_seguridad, 2)

    def reservar_unidad(self, cantidad: int = 1) -> None:
        if cantidad > self.stock_disponible:
            raise ServicioNoDisponibleError(f"No hay suficiente stock para descontar {cantidad} unidad(es).")
        self.stock_disponible -= cantidad
        self.disponible = self.stock_disponible > 0

    def liberar_unidad(self, cantidad: int = 1) -> None:
        self.stock_disponible += cantidad
        self.disponible = self.stock_disponible > 0

    def describir_servicio(self) -> str:
        return (
            f"[Equipo] {self.nombre} ({self.categoria_equipo}) | Stock: {self.stock_disponible} | "
            f"Tarifa/h: ${self.tarifa_hora:,.2f} | Depósito: ${self.deposito_seguridad:,.2f}"
        )


class AsesoriaEspecializada(Servicio):
    """Servicio especializado de consultoría técnica en ingeniería y desarrollo de software."""

    NIVELES_VALIDOS = {"Junior": 1.0, "Senior": 1.35, "Arquitecto": 1.75}

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, especialidad: str, nivel_consultor: str = "Senior", disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        if not especialidad or not str(especialidad).strip():
            raise ParametroFaltanteError("La especialidad de la asesoría es obligatoria.")
        if nivel_consultor not in self.NIVELES_VALIDOS:
            raise DatoInvalidoError(
                f"Nivel de consultor '{nivel_consultor}' inválido. Opciones: {list(self.NIVELES_VALIDOS.keys())}."
            )
        self.especialidad = especialidad.strip()
        self.nivel_consultor = nivel_consultor

    def validar_parametros(self, duracion_horas: int, **kwargs) -> None:
        if not self.disponible:
            raise ServicioNoDisponibleError(f"El consultor de '{self.nombre}' no tiene agenda disponible.")
        if duracion_horas < 1 or duracion_horas > 8:
            raise DatoInvalidoError("Las sesiones de asesoría deben durar entre 1 y 8 horas por jornada.")
        modalidad = kwargs.get("modalidad", "Remota")
        if modalidad not in ("Remota", "Presencial"):
            raise DatoInvalidoError("La modalidad de asesoría debe ser 'Remota' o 'Presencial'.")

    def calcular_costo_base(self, duracion_horas: int) -> float:
        factor_nivel = self.NIVELES_VALIDOS[self.nivel_consultor]
        return round(self.tarifa_hora * duracion_horas * factor_nivel, 2)

    def describir_servicio(self) -> str:
        return (
            f"[Asesoría] {self.nombre} | Área: {self.especialidad} | Consultor: {self.nivel_consultor} | "
            f"Tarifa base/h: ${self.tarifa_hora:,.2f}"
        )
