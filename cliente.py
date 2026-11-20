"""
Módulo: cliente.py
Descripción: Define la clase abstracta EntidadGeneral y la clase concreta Cliente,
aplicando abstracción, encapsulamiento y validación estricta de datos mediante
excepciones personalizadas para el sistema de Software FJ.
"""

import re
from abc import ABC, abstractmethod
from excepciones import ClienteInvalidoError


class EntidadGeneral(ABC):
    """Clase abstracta base para todas las entidades del dominio de Software FJ."""

    @abstractmethod
    def obtener_descripcion(self):
        """Retorna una representación textual detallada de la entidad."""
        pass


class Cliente(EntidadGeneral):
    """Representa un cliente registrado en Software FJ con atributos encapsulados."""

    def __init__(self, id_cliente, nombre, email, telefono):
        self.__id_cliente = None
        self.__nombre = None
        self.__email = None
        self.__telefono = None

        self.set_id_cliente(id_cliente)
        self.set_nombre(nombre)
        self.set_email(email)
        self.set_telefono(telefono)

    # ---------- Getters ----------
    def get_id_cliente(self):
        return self.__id_cliente

    def get_nombre(self):
        return self.__nombre

    def get_email(self):
        return self.__email

    def get_telefono(self):
        return self.__telefono

    # ---------- Setters con validación ----------
    def set_id_cliente(self, id_cliente):
        if isinstance(id_cliente, bool) or not isinstance(id_cliente, int) or id_cliente <= 0:
            raise ClienteInvalidoError(
                f"El ID del cliente ('{id_cliente}') debe ser un número entero positivo."
            )
        self.__id_cliente = id_cliente

    def set_nombre(self, nombre):
        if not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise ClienteInvalidoError(
                "El nombre del cliente debe ser un texto de al menos 3 caracteres."
            )
        if any(caracter.isdigit() for caracter in nombre):
            raise ClienteInvalidoError(
                f"El nombre '{nombre.strip()}' no puede contener dígitos numéricos."
            )
        self.__nombre = nombre.strip()

    def set_email(self, email):
        patron_correo = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not isinstance(email, str) or not re.match(patron_correo, email.strip()):
            raise ClienteInvalidoError(
                f"El correo electrónico '{email}' no tiene un formato válido."
            )
        self.__email = email.strip().lower()

    def set_telefono(self, telefono):
        if not isinstance(telefono, str):
            raise ClienteInvalidoError(
                "El teléfono debe ingresarse como cadena de texto numérica."
            )
        limpio = telefono.strip()
        if not limpio.isdigit() or not (7 <= len(limpio) <= 10):
            raise ClienteInvalidoError(
                f"El teléfono '{telefono}' debe contener entre 7 y 10 dígitos."
            )
        self.__telefono = limpio

    # ---------- Implementación de métodos abstractos y mágicos ----------
    def obtener_descripcion(self):
        return (
            f"Cliente #{self.__id_cliente} | Nombre: {self.__nombre} | "
            f"Correo: {self.__email} | Teléfono: {self.__telefono}"
        )

    def __str__(self):
        return self.obtener_descripcion()