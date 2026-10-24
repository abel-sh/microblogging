"""Entidad Seguimiento (DISEÑO §3.2 y §3.3)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Seguimiento:
    """id_seguidor sigue a id_seguido desde fecha_inicio."""

    id_seguidor: int
    id_seguido: int
    fecha_inicio: datetime