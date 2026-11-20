"""
Módulo: excepciones.py
Descripción: Define la jerarquía de excepciones personalizadas para el sistema
de gestión de Software FJ, permitiendo capturar errores específicos del dominio
sin detener la ejecución del programa.
"""


class ErrorSoftwareFJ(Exception):
    """Excepción base para todos los errores controlados de Software FJ."""

    def __init__(self, mensaje, codigo_error="ERR-000"):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo_error = codigo_error

    def __str__(self):
        return f"[{self.codigo_error}] {self.mensaje}"


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando los datos de un cliente no cumplen las reglas de validación."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo_error="ERR-CLI")


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando los parámetros de un servicio o tarifa son incorrectos."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo_error="ERR-SRV")


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza al intentar reservar un servicio inactivo o no disponible."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo_error="ERR-DISP")


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se lanza ante conflictos en la creación, procesamiento o cancelación de reservas."""

    def __init__(self, mensaje):
        super().__init__(mensaje, codigo_error="ERR-RES")