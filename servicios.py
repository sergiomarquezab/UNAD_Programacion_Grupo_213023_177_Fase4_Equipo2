"""
Módulo: servicios.py
Descripción: Define la clase abstracta Servicio y las clases derivadas
ReservaSala, AlquilerEquipo y AsesoriaEspecializada para Software FJ,
aplicando herencia, polimorfismo y validación de reglas de negocio.
"""

from abc import ABC, abstractmethod
from cliente import EntidadGeneral
from excepciones import ServicioInvalidoError


class Servicio(EntidadGeneral, ABC):
    """Clase abstracta que representa un servicio ofertado por Software FJ."""

    TASA_IVA = 0.19

    def __init__(self, codigo, nombre, precio_base):
        if not isinstance(codigo, str) or not codigo.strip():
            raise ServicioInvalidoError("El código del servicio no puede estar vacío.")
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El nombre del servicio no puede estar vacío.")
        if isinstance(precio_base, bool) or not isinstance(precio_base, (int, float)) or precio_base <= 0:
            raise ServicioInvalidoError(
                f"El precio base ('{precio_base}') debe ser un valor numérico mayor a cero."
            )

        self.codigo = codigo.strip().upper()
        self.nombre = nombre.strip()
        self.precio_base = float(precio_base)
        self.disponible = True

    @abstractmethod
    def validar_parametros(self, duracion):
        """Valida que la duración cumpla con las reglas específicas del servicio."""
        pass

    @abstractmethod
    def calcular_costo(self, duracion, aplicar_iva=False, descuento=0.0):
        """Calcula el valor total del servicio aplicando sus reglas particulares."""
        pass

    def _procesar_descuento_e_impuesto(self, subtotal, aplicar_iva, descuento):
        """Aplica descuento promocional (0.0 a 1.0) e IVA (19 %) sobre el subtotal."""
        if isinstance(descuento, bool) or not isinstance(descuento, (int, float)) or not (0.0 <= descuento <= 1.0):
            raise ServicioInvalidoError(
                f"El porcentaje de descuento ({descuento}) debe estar entre 0.0 y 1.0."
            )

        total = subtotal * (1.0 - descuento)
        if aplicar_iva:
            total *= (1.0 + self.TASA_IVA)
        return round(total, 2)

    def cambiar_disponibilidad(self, estado):
        """Habilita o deshabilita la disponibilidad del servicio."""
        if not isinstance(estado, bool):
            raise ServicioInvalidoError("El estado de disponibilidad debe ser booleano (True/False).")
        self.disponible = estado

    def obtener_descripcion(self):
        estado_txt = "Disponible" if self.disponible else "No disponible"
        return (
            f"[{self.codigo}] {self.nombre} | Tarifa base: ${self.precio_base:,.2f} | "
            f"Estado: {estado_txt}"
        )

    def __str__(self):
        return self.obtener_descripcion()


class ReservaSala(Servicio):
    """Servicio de alquiler de salas de reuniones/capacitación por horas."""

    def __init__(self, codigo, nombre, precio_base, capacidad):
        super().__init__(codigo, nombre, precio_base)
        if isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError("La capacidad de la sala debe ser un entero positivo.")
        self.capacidad = capacidad

    def validar_parametros(self, duracion):
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion < 1:
            raise ServicioInvalidoError("La reserva de sala requiere una duración mínima de 1 hora.")

    def calcular_costo(self, duracion, aplicar_iva=False, descuento=0.0):
        self.validar_parametros(duracion)
        subtotal = self.precio_base * duracion
        # Descuento automático del 10 % por bloque de 4 o más horas
        if duracion >= 4:
            subtotal *= 0.90
        return self._procesar_descuento_e_impuesto(subtotal, aplicar_iva, descuento)

    def obtener_descripcion(self):
        return f"{super().obtener_descripcion()} | Capacidad: {self.capacidad} personas"


class AlquilerEquipo(Servicio):
    """Servicio de préstamo/alquiler de equipos tecnológicos por días."""

    RECARGO_SEGURO = 0.10

    def __init__(self, codigo, nombre, precio_base, tipo_equipo):
        super().__init__(codigo, nombre, precio_base)
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ServicioInvalidoError("El tipo de equipo no puede estar vacío.")
        self.tipo_equipo = tipo_equipo.strip()

    def validar_parametros(self, duracion):
        if isinstance(duracion, bool) or not isinstance(duracion, int) or duracion < 1:
            raise ServicioInvalidoError(
                "El alquiler de equipos se gestiona por días enteros completos (mínimo 1 día)."
            )

    def calcular_costo(self, duracion, aplicar_iva=False, descuento=0.0):
        self.validar_parametros(duracion)
        subtotal = (self.precio_base * duracion) * (1.0 + self.RECARGO_SEGURO)
        return self._procesar_descuento_e_impuesto(subtotal, aplicar_iva, descuento)

    def obtener_descripcion(self):
        return f"{super().obtener_descripcion()} | Equipo: {self.tipo_equipo}"


class AsesoriaEspecializada(Servicio):
    """Servicio de consultoría técnica por horas (máximo 8 horas por día)."""

    RECARGO_HORA_EXTRA = 0.25

    def __init__(self, codigo, nombre, precio_base, area):
        super().__init__(codigo, nombre, precio_base)
        if not isinstance(area, str) or not area.strip():
            raise ServicioInvalidoError("El área de especialización no puede estar vacía.")
        self.area = area.strip()

    def validar_parametros(self, duracion):
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or not (1 <= duracion <= 8):
            raise ServicioInvalidoError(
                "La asesoría especializada debe programarse entre 1 y 8 horas por jornada."
            )

    def calcular_costo(self, duracion, aplicar_iva=False, descuento=0.0):
        self.validar_parametros(duracion)
        horas_regulares = min(duracion, 4)
        horas_adicionales = max(duracion - 4, 0)
        subtotal = (self.precio_base * horas_regulares) + (
            self.precio_base * (1.0 + self.RECARGO_HORA_EXTRA) * horas_adicionales
        )
        return self._procesar_descuento_e_impuesto(subtotal, aplicar_iva, descuento)

    def obtener_descripcion(self):
        return f"{super().obtener_descripcion()} | Área: {self.area}"