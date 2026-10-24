"""Entidad Usuario"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from miblog.logica.dominio.enumeraciones import RolUsuario


def _ahora() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(kw_only=True)
class Usuario:
    """Un empleado registrado.

    email y clave_hash pueden ser None: los objetos que se arman para mostrar
    (por ejemplo, el autor de un mensaje) no necesitan cargarlos.
    """

    id_usuario: int | None = None
    nombre_usuario: str
    email: str | None = None
    clave_hash: str | None = None
    nombre_completo: str
    descripcion: str | None = None
    url_foto: str | None = None
    rol: RolUsuario = RolUsuario.EMPLEADO
    fecha_alta: datetime = field(default_factory=_ahora)
    activo: bool = True