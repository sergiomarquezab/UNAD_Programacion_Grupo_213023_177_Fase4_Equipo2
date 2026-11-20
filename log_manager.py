"""
Módulo: log_manager.py
Descripción: Configura y provee el sistema centralizado de auditoría y registro
de eventos (logs) para Software FJ, garantizando trazabilidad completa en archivo
sin interrumpir la ejecución del programa.
"""

import logging
import os


def obtener_logger(nombre_logger="SoftwareFJ", archivo_log="registro_softwarefj.log"):
    """
    Configura y retorna un logger dedicado que escribe eventos e incidencias
    en un archivo .log con marca de tiempo, nivel de severidad y módulo de origen.
    """
    logger = logging.getLogger(nombre_logger)
    logger.setLevel(logging.INFO)

    # Evita duplicar registros si la función se invoca desde múltiples módulos
    if not logger.handlers:
        ruta_completa = os.path.abspath(archivo_log)
        manejador_archivo = logging.FileHandler(
            ruta_completa, mode="a", encoding="utf-8"
        )
        formato = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(module)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        manejador_archivo.setFormatter(formato)
        logger.addHandler(manejador_archivo)
        # Evita que los mensajes suban al logger raíz y se dupliquen
        logger.propagate = False

    return logger