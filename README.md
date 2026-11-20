# Sistema Integral de Gestión – Software FJ

Proyecto correspondiente al **Componente Práctico – Prácticas Simuladas (Fase 4)** del curso **Programación (213023)** de la Universidad Nacional Abierta y a Distancia (UNAD) – Grupo `213023_177`.

## Autores
* **Sergio** – Arquitectura, Excepciones Personalizadas, Logging y Modelo de Clientes
* **Yeison** – Catálogo de Servicios, Gestión de Reservas y Simulaciones *(Por confirmar módulo)*

## Descripción del Proyecto
Aplicación modular desarrollada en **Python 3** bajo el paradigma de **Programación Orientada a Objetos (POO)** para administrar los clientes, el portafolio de servicios (reserva de salas, alquiler de equipos y asesorías especializadas) y las reservas de la empresa **Software FJ**. El sistema opera en memoria mediante estructuras de datos y garantiza la continuidad operativa mediante manejo robusto de excepciones y registro de auditoría en archivo `.log`.

## Estructura del Repositorio
```text
├── cliente.py               # Clase abstracta base y entidad Cliente con encapsulamiento y validaciones
├── servicios.py             # Clase abstracta Servicio y clases derivadas (polimorfismo en tarifas)
├── reserva.py               # Gestión del ciclo de vida de reservas y encadenamiento de excepciones
├── excepciones.py           # Jerarquía de excepciones personalizadas del dominio
├── log_manager.py           # Configuración centralizada del sistema de logs
├── gestor.py                # Controlador principal en memoria con bloques try/except/else/finally
├── main.py                  # Script de simulación con casos válidos e inválidos
└── registro_softwarefj.log  # Evidencia generada de eventos e incidencias del sistema
