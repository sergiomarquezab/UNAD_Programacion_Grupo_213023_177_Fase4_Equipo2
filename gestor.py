"""
Módulo: gestor.py
Descripción: Controlador principal en memoria de Software FJ. Administra las
colecciones de clientes, servicios y reservas aplicando estructuras completas
try / except / else / finally y registro de auditoría en archivo .log.
"""

from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva
from excepciones import (
    ErrorSoftwareFJ,
    ClienteInvalidoError,
    ServicioInvalidoError,
    ReservaInvalidaError,
)
from log_manager import obtener_logger

logger = obtener_logger()


class GestorSoftwareFJ:
    """Orquesta todas las operaciones de negocio en memoria para Software FJ."""

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    # ---------- Métodos de búsqueda en memoria ----------
    def buscar_cliente(self, id_cliente):
        for cliente in self.clientes:
            if cliente.get_id_cliente() == id_cliente:
                return cliente
        return None

    def buscar_servicio(self, codigo):
        if not isinstance(codigo, str):
            return None
        codigo_normalizado = codigo.strip().upper()
        for servicio in self.servicios:
            if servicio.codigo == codigo_normalizado:
                return servicio
        return None

    def buscar_reserva(self, id_reserva):
        for reserva in self.reservas:
            if reserva.id_reserva == id_reserva:
                return reserva
        return None

    # ---------- Gestión de Clientes ----------
    def registrar_cliente(self, id_cliente, nombre, email, telefono):
        """Registra un nuevo cliente validando duplicados y formato de datos."""
        try:
            if self.buscar_cliente(id_cliente) is not None:
                raise ClienteInvalidoError(
                    f"Ya existe un cliente registrado con el ID {id_cliente}."
                )
            nuevo_cliente = Cliente(id_cliente, nombre, email, telefono)
        except ErrorSoftwareFJ as error:
            logger.error(f"Error al registrar cliente (ID={id_cliente}): {error}")
            print(f"  [ERROR] {error}")
            return None
        except Exception as error_inesperado:
            logger.exception(f"Error inesperado al registrar cliente: {error_inesperado}")
            print(f"  [ERROR INESPERADO] {error_inesperado}")
            return None
        else:
            self.clientes.append(nuevo_cliente)
            logger.info(f"Cliente registrado exitosamente: {nuevo_cliente.obtener_descripcion()}")
            print(f"  [OK] {nuevo_cliente.obtener_descripcion()}")
            return nuevo_cliente
        finally:
            logger.info(f"Cierre de operación: registrar_cliente (ID={id_cliente})")

    # ---------- Gestión de Servicios ----------
    def crear_servicio(self, tipo, codigo, nombre, precio_base, atributo_extra):
        """Crea y registra un servicio especializado según su tipo ('sala', 'equipo', 'asesoria')."""
        try:
            if self.buscar_servicio(codigo) is not None:
                raise ServicioInvalidoError(
                    f"Ya existe un servicio registrado con el código '{codigo}'."
                )

            tipo_norm = tipo.strip().lower() if isinstance(tipo, str) else ""
            if tipo_norm == "sala":
                nuevo_servicio = ReservaSala(codigo, nombre, precio_base, atributo_extra)
            elif tipo_norm == "equipo":
                nuevo_servicio = AlquilerEquipo(codigo, nombre, precio_base, atributo_extra)
            elif tipo_norm == "asesoria":
                nuevo_servicio = AsesoriaEspecializada(codigo, nombre, precio_base, atributo_extra)
            else:
                raise ServicioInvalidoError(
                    f"Tipo de servicio desconocido: '{tipo}'. Use 'sala', 'equipo' o 'asesoria'."
                )
        except ErrorSoftwareFJ as error:
            logger.error(f"Error al crear servicio ({codigo}): {error}")
            print(f"  [ERROR] {error}")
            return None
        except Exception as error_inesperado:
            logger.exception(f"Error inesperado al crear servicio: {error_inesperado}")
            print(f"  [ERROR INESPERADO] {error_inesperado}")
            return None
        else:
            self.servicios.append(nuevo_servicio)
            logger.info(f"Servicio creado exitosamente: {nuevo_servicio.obtener_descripcion()}")
            print(f"  [OK] {nuevo_servicio.obtener_descripcion()}")
            return nuevo_servicio
        finally:
            logger.info(f"Cierre de operación: crear_servicio (Código={codigo})")

    # ---------- Cotización polimórfica ----------
    def cotizar_servicio(self, codigo_servicio, duracion, aplicar_iva=False, descuento=0.0):
        """Calcula el costo de un servicio sin generar reserva."""
        try:
            servicio = self.buscar_servicio(codigo_servicio)
            if servicio is None:
                raise ServicioInvalidoError(
                    f"No se encontró ningún servicio con el código '{codigo_servicio}'."
                )
            total = servicio.calcular_costo(duracion, aplicar_iva=aplicar_iva, descuento=descuento)
        except ErrorSoftwareFJ as error:
            logger.error(f"Error al cotizar servicio '{codigo_servicio}': {error}")
            print(f"  [ERROR] {error}")
            return None
        except Exception as error_inesperado:
            logger.exception(f"Error inesperado al cotizar: {error_inesperado}")
            print(f"  [ERROR INESPERADO] {error_inesperado}")
            return None
        else:
            detalle = (
                f"Cotización {servicio.nombre} ({duracion} u. | IVA={aplicar_iva} | "
                f"Desc={descuento*100:.0f}%): ${total:,.2f}"
            )
            logger.info(detalle)
            print(f"  [OK] {detalle}")
            return total
        finally:
            logger.info(f"Cierre de operación: cotizar_servicio (Código={codigo_servicio})")

    # ---------- Gestión de Reservas ----------
    def crear_reserva(self, id_reserva, id_cliente, codigo_servicio, duracion):
        """Crea y procesa una reserva asociando cliente y servicio existentes."""
        try:
            if self.buscar_reserva(id_reserva) is not None:
                raise ReservaInvalidaError(
                    f"Ya existe una reserva registrada con el ID {id_reserva}."
                )

            cliente = self.buscar_cliente(id_cliente)
            if cliente is None:
                raise ClienteInvalidoError(
                    f"No existe un cliente registrado con el ID {id_cliente}."
                )

            servicio = self.buscar_servicio(codigo_servicio)
            if servicio is None:
                raise ServicioInvalidoError(
                    f"No existe un servicio registrado con el código '{codigo_servicio}'."
                )

            servicio.validar_parametros(duracion)
            nueva_reserva = Reserva(id_reserva, cliente, servicio, duracion)
            nueva_reserva.procesar()
        except ErrorSoftwareFJ as error:
            logger.error(f"Error al crear reserva #{id_reserva}: {error}")
            print(f"  [ERROR] {error}")
            return None
        except Exception as error_inesperado:
            logger.exception(f"Error inesperado al crear reserva: {error_inesperado}")
            print(f"  [ERROR INESPERADO] {error_inesperado}")
            return None
        else:
            self.reservas.append(nueva_reserva)
            print(f"  [OK] {nueva_reserva.obtener_descripcion()}")
            return nueva_reserva
        finally:
            logger.info(f"Cierre de operación: crear_reserva (ID={id_reserva})")

    def cancelar_reserva(self, id_reserva):
        """Cancela una reserva existente en memoria."""
        try:
            reserva = self.buscar_reserva(id_reserva)
            if reserva is None:
                raise ReservaInvalidaError(
                    f"No se encontró ninguna reserva con el ID {id_reserva}."
                )
            reserva.cancelar()
        except ErrorSoftwareFJ as error:
            logger.error(f"Error al cancelar reserva #{id_reserva}: {error}")
            print(f"  [ERROR] {error}")
            return False
        except Exception as error_inesperado:
            logger.exception(f"Error inesperado al cancelar reserva: {error_inesperado}")
            print(f"  [ERROR INESPERADO] {error_inesperado}")
            return False
        else:
            print(f"  [OK] Reserva #{id_reserva} cancelada correctamente.")
            return True
        finally:
            logger.info(f"Cierre de operación: cancelar_reserva (ID={id_reserva})")