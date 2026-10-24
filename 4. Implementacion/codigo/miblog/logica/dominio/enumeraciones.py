"""Enumeraciones del dominio.

Los valores de texto coinciden con los CHECK de esquema.sql, así un repositorio
puede convertir en las dos direcciones:  RolUsuario(fila["rol"])  y  rol.value
"""

from enum import Enum


class RolUsuario(Enum):
    EMPLEADO = "EMPLEADO"
    ADMINISTRADOR = "ADMINISTRADOR"


class OrigenPublicacion(Enum):
    WEB = "WEB"
    API = "API"