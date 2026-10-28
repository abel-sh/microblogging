"""Conexión a SQLite, transacciones y normalización de texto.

Es el único módulo que abre la base. Los repositorios piden la
conexión con obtener_conexion() y ejecutan SQL parametrizado con "?".
"""

from __future__ import annotations

import sqlite3
import unicodedata
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from flask import current_app, g

RUTA_ESQUEMA = Path(__file__).with_name("esquema.sql")


class BaseYaInicializadaError(RuntimeError):
    """La base ya tiene las tablas. esquema.sql no usa IF NOT EXISTS."""


def normalizar(texto: str | None) -> str | None:
    """Minúsculas y sin acentos, para buscar sin que importen.

    "Peña" -> "pena", "JOSÉ" -> "jose". Se registra en SQLite con
    create_function, así que una consulta puede escribir normalizar(columna).
    Recibe None cuando la columna es NULL, y devuelve None.
    """
    if texto is None:
        return None
    descompuesto = unicodedata.normalize("NFD", texto.casefold())
    sin_acentos = "".join(c for c in descompuesto if not unicodedata.combining(c))
    return unicodedata.normalize("NFC", sin_acentos)


def obtener_conexion() -> sqlite3.Connection:
    """Devuelve la conexión de esta petición; la abre la primera vez que se la pide."""
    if "conexion" not in g:
        conexion = sqlite3.connect(
            current_app.config["BASE_DE_DATOS"],
            isolation_level=None,  # nosotros decidimos cuándo hay transacción (BEGIN/COMMIT)
            timeout=5,
        )
        conexion.row_factory = sqlite3.Row
        # SQLite trae las claves foráneas apagadas, y hay que encenderlas en CADA conexión.
        conexion.execute("PRAGMA foreign_keys = ON")
        conexion.create_function("normalizar", 1, normalizar, deterministic=True)
        g.conexion = conexion
    return g.conexion


def cerrar_conexion(error: BaseException | None = None) -> None:
    """Se registra con app.teardown_appcontext: cierra la conexión al terminar la petición."""
    conexion = g.pop("conexion", None)
    if conexion is not None:
        conexion.close()


@contextmanager
def transaccion() -> Iterator[None]:
    """Todo lo que se ejecute adentro se guarda junto o no se guarda.

    BEGIN IMMEDIATE toma el bloqueo de escritura al empezar, no en la primera
    escritura: así "verificar que no existe" y "crear" quedan dentro del mismo
    bloqueo. Si salta cualquier excepción, ROLLBACK y se vuelve a lanzar.
    Solo la capa de lógica abre transacciones, y nunca se anidan.
    """
    conexion = obtener_conexion()
    if conexion.in_transaction:
        raise RuntimeError("transaccion() no se puede anidar.")
    conexion.execute("BEGIN IMMEDIATE")
    try:
        yield
        conexion.execute("COMMIT")
    except BaseException:
        if conexion.in_transaction:
            conexion.execute("ROLLBACK")
        raise


def inicializar_base() -> None:
    """Crea todas las tablas leyendo esquema.sql. Falla si la base ya tiene tablas."""
    conexion = obtener_conexion()
    ya_hay_tablas = conexion.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'usuarios'"
    ).fetchone()
    if ya_hay_tablas:
        raise BaseYaInicializadaError(
            "La base ya está inicializada. Para empezar de cero, borrá el archivo "
            "de la carpeta instance/ y corré el comando de nuevo."
        )
    esquema = RUTA_ESQUEMA.read_text(encoding="utf-8")
    try:
        # Todo el esquema en una transacción: o se crean todas las tablas o ninguna.
        conexion.executescript("BEGIN;\n" + esquema + "\nCOMMIT;")
    except BaseException:
        if conexion.in_transaction:
            conexion.execute("ROLLBACK")
        raise