"""
Módulo: reserva.py
Descripción: Define la clase Reserva, encargada de gestionar el ciclo de vida
de una reserva (Pendiente, Confirmada, Fallida, Cancelada), el cálculo de su
costo total y el encadenamiento de excepciones ante servicios no disponibles.
"""

from cliente import EntidadGeneral
from excepciones import ServicioNoDisponibleError, ReservaInvalidaError
from log_manager import obtener_logger

logger = obtener_logger()


class Reserva(EntidadGeneral):
    """Representa una reserva asociada a un cliente y a un servicio de Software FJ."""

    ESTADOS_VALIDOS = ("Pendiente", "Confirmada", "Fallida", "Cancelada")

    def __init__(self, id_reserva, cliente, servicio, duracion):
        if isinstance(id_reserva, bool) or not isinstance(id_reserva, int) or id_reserva <= 0:
            raise ReservaInvalidaError(
                f"El ID de la reserva ('{id_reserva}') debe ser un número entero positivo."
            )

        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"
        self.costo_total = 0.0

    def confirmar(self):
        """
        Valida la disponibilidad del servicio, calcula el costo con IVA (19 %)
        y cambia el estado de la reserva a 'Confirmada'.
        """
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.servicio.nombre}' ({self.servicio.codigo}) "
                f"no se encuentra disponible actualmente."
            )

        self.costo_total = self.servicio.calcular_costo(self.duracion, aplicar_iva=True)
        self.estado = "Confirmada"
        logger.info(
            f"Reserva #{self.id_reserva} confirmada | Cliente: {self.cliente.get_nombre()} | "
            f"Servicio: {self.servicio.nombre} | Total: ${self.costo_total:,.2f}"
        )
        return True

    def procesar(self):
        """
        Ejecuta la confirmación de la reserva aplicando encadenamiento de excepciones
        si el servicio subyacente no está disponible.
        """
        try:
            return self.confirmar()
        except ServicioNoDisponibleError as error_origen:
            self.estado = "Fallida"
            logger.error(
                f"Fallo al procesar Reserva #{self.id_reserva}: {error_origen}"
            )
            raise ReservaInvalidaError(
                f"No fue posible procesar la reserva #{self.id_reserva} por indisponibilidad del servicio."
            ) from error_origen

    def cancelar(self):
        """Cancela una reserva activa; impide cancelar una reserva ya cancelada o fallida."""
        if self.estado == "Cancelada":
            raise ReservaInvalidaError(
                f"La reserva #{self.id_reserva} ya se encuentra cancelada."
            )
        if self.estado == "Fallida":
            raise ReservaInvalidaError(
                f"La reserva #{self.id_reserva} está en estado Fallida y no puede cancelarse."
            )

        self.estado = "Cancelada"
        logger.info(f"Reserva #{self.id_reserva} cancelada correctamente.")
        return True

    def obtener_descripcion(self):
        return (
            f"Reserva #{self.id_reserva} | Cliente: {self.cliente.get_nombre()} | "
            f"Servicio: {self.servicio.nombre} ({self.duracion} u.) | "
            f"Estado: {self.estado} | Total: ${self.costo_total:,.2f}"
        )

    def __str__(self):
        return self.obtener_descripcion()