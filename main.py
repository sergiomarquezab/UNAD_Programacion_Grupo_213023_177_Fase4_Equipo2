"""
Módulo: main.py
Descripción: Punto de entrada principal para la simulación de operaciones de
Software FJ. Ejecuta 20 escenarios (válidos e inválidos) que validan la
estabilidad del sistema, el manejo de excepciones y el registro en el archivo .log.
"""

from gestor import GestorSoftwareFJ
from log_manager import obtener_logger

logger = obtener_logger()


def mostrar_encabezado(numero, descripcion):
    """Imprime y registra en el log el inicio de cada escenario de prueba."""
    print(f"\n[Escenario {numero:02d}] {descripcion}")
    logger.info(f"--- Escenario {numero:02d}: {descripcion} ---")


def ejecutar_simulacion():
    """Ejecuta la batería completa de 20 operaciones simuladas en memoria."""
    logger.info("==========================================================")
    logger.info("INICIO DE SIMULACIÓN OPERATIVA - SOFTWARE FJ")
    logger.info("==========================================================")

    print("==========================================================")
    print("   SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ (FASE 4)")
    print("==========================================================")

    gestor = GestorSoftwareFJ()

    # ---------- BLOQUE 1: GESTIÓN DE CLIENTES ----------
    mostrar_encabezado(1, "Registrar cliente válido (Laura Mendoza)")
    gestor.registrar_cliente(101, "Laura Mendoza", "laura.mendoza@correo.com", "3014567890")

    mostrar_encabezado(2, "Registrar cliente válido (Andrés Gómez)")
    gestor.registrar_cliente(102, "Andrés Gómez", "andres.gomez@empresa.co", "3159876543")

    mostrar_encabezado(3, "Registrar cliente válido (Camila Torres)")
    gestor.registrar_cliente(103, "Camila Torres", "camila.t@dominio.org", "6063214567")

    mostrar_encabezado(4, "Registrar cliente con ID duplicado (ERROR esperado)")
    gestor.registrar_cliente(101, "Laura Duplicada", "otra@correo.com", "3001112233")

    mostrar_encabezado(5, "Registrar cliente con correo inválido (ERROR esperado)")
    gestor.registrar_cliente(104, "Mateo Ríos", "mateo_sin_arroba.com", "3205556677")

    mostrar_encabezado(6, "Registrar cliente con nombre numérico (ERROR esperado)")
    gestor.registrar_cliente(105, "Carlos 123", "carlos@correo.com", "3112223344")

    # ---------- BLOQUE 2: CATÁLOGO DE SERVICIOS ----------
    mostrar_encabezado(7, "Crear servicio válido: Sala Ejecutiva (capacidad 12)")
    gestor.crear_servicio("sala", "SAL-01", "Sala Ejecutiva Norte", 60000, 12)

    mostrar_encabezado(8, "Crear servicio válido: Estación MacBook Pro")
    gestor.crear_servicio("equipo", "EQP-01", "MacBook Pro M3", 45000, "Computador Portátil")

    mostrar_encabezado(9, "Crear servicio válido: Consultoría Arquitectura Cloud")
    gestor.crear_servicio("asesoria", "ASE-01", "Consultoría Cloud", 95000, "Infraestructura")

    mostrar_encabezado(10, "Crear servicio y deshabilitar disponibilidad (VideoBeam 4K)")
    videobeam = gestor.crear_servicio("equipo", "EQP-02", "VideoBeam Laser 4K", 25000, "Proyección")
    if videobeam is not None:
        videobeam.cambiar_disponibilidad(False)

    mostrar_encabezado(11, "Crear servicio con precio base negativo (ERROR esperado)")
    gestor.crear_servicio("sala", "SAL-99", "Sala Inválida", -15000, 6)

    # ---------- BLOQUE 3: COTIZACIONES POLIMÓRFICAS ----------
    mostrar_encabezado(12, "Cotizar Sala Ejecutiva por 5 horas (aplica 10% auto + IVA)")
    gestor.cotizar_servicio("SAL-01", 5, aplicar_iva=True, descuento=0.05)

    mostrar_encabezado(13, "Cotizar Asesoría por 6 horas (4 regulares + 2 con recargo 25%)")
    gestor.cotizar_servicio("ASE-01", 6, aplicar_iva=True)

    mostrar_encabezado(14, "Cotizar con descuento fuera de rango 120% (ERROR esperado)")
    gestor.cotizar_servicio("EQP-01", 2, aplicar_iva=False, descuento=1.2)

    # ---------- BLOQUE 4: RESERVAS Y ENCADENAMIENTO DE EXCEPCIONES ----------
    mostrar_encabezado(15, "Crear reserva válida: Sala Ejecutiva por 4 horas (Laura)")
    gestor.crear_reserva(5001, 101, "SAL-01", 4)

    mostrar_encabezado(16, "Crear reserva válida: MacBook Pro por 3 días (Andrés)")
    gestor.crear_reserva(5002, 102, "EQP-01", 3)

    mostrar_encabezado(17, "Crear reserva con cliente inexistente ID 999 (ERROR esperado)")
    gestor.crear_reserva(5003, 999, "SAL-01", 2)

    mostrar_encabezado(18, "Crear reserva de asesoría por 9 horas - excede límite (ERROR esperado)")
    gestor.crear_reserva(5004, 103, "ASE-01", 9)

    mostrar_encabezado(19, "Reservar VideoBeam no disponible (ERROR encadenado esperado)")
    gestor.crear_reserva(5005, 103, "EQP-02", 1)

    # ---------- BLOQUE 5: CANCELACIONES ----------
    mostrar_encabezado(20, "Cancelar reserva #5001 y reintentar cancelación (ERROR esperado)")
    gestor.cancelar_reserva(5001)
    gestor.cancelar_reserva(5001)

    # ---------- RESUMEN DE ESTADO EN MEMORIA ----------
    print("\n==========================================================")
    print("   RESUMEN FINAL DE EJECUCIÓN EN MEMORIA")
    print("==========================================================")
    print(f"  * Clientes activos en memoria : {len(gestor.clientes)}")
    print(f"  * Servicios en catálogo       : {len(gestor.servicios)}")
    print(f"  * Reservas confirmadas/activas: {len(gestor.reservas)}")
    print("  * Estado del sistema          : ESTABLE (0 fallos no controlados)")
    print("==========================================================")

    logger.info(
        f"FIN DE SIMULACIÓN | Clientes={len(gestor.clientes)} | "
        f"Servicios={len(gestor.servicios)} | Reservas={len(gestor.reservas)} | Sistema estable"
    )


if __name__ == "__main__":
    ejecutar_simulacion()