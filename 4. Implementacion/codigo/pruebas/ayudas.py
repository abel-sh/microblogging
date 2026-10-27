"""Ayudas compartidas por las pruebas de MiBlog.

Las pruebas usan unittest, que viene con Python: no hay que instalar nada. Se
corren desde 4. Implementacion/codigo/, con el entorno virtual activado:

    python -m unittest discover -s pruebas -t . -v

Cada prueba arma su propia aplicación con una base de datos nueva, en una carpeta
temporal que se borra al terminar. Nunca toca instance/miblog.sqlite3 ni usa el
SECRET_KEY de tu .env.

Para dejar la base en el estado que cada prueba necesita se usa SQL directo (las
funciones de abajo). Es a propósito: si sembráramos los datos con los repositorios
que estamos probando, un error en un repositorio rompería también la preparación y
no sabríamos dónde está el problema. La regla "SQL solo en acceso_datos" vale para
el código de la aplicación, no para estas pruebas.
"""

from __future__ import annotations

import os
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from miblog import crear_app
from miblog.acceso_datos.conexion import inicializar_base, obtener_conexion

# Un momento fijo de referencia. Las fechas de las pruebas se expresan en minutos
# antes o después de este momento, así los órdenes son siempre los mismos.
AHORA = datetime.now(timezone.utc)


def en(minutos: int) -> datetime:
    """en(5) es dentro de 5 minutos; en(-20), hace 20 minutos."""
    return AHORA + timedelta(minutes=minutos)


def crear_usuario(
    con,
    nombre_usuario: str,
    nombre_completo: str | None = None,
    clave_hash: str = "no-sirve-para-entrar",
    activo: int = 1,
) -> int:
    """Inserta un usuario y devuelve su id."""
    cursor = con.execute(
        "INSERT INTO usuarios (nombre_usuario, email, clave_hash, nombre_completo, "
        "fecha_alta, activo) VALUES (?, ?, ?, ?, ?, ?)",
        (
            nombre_usuario,
            f"{nombre_usuario}@ejemplo.com",
            clave_hash,
            nombre_completo or nombre_usuario.title(),
            AHORA.isoformat(),
            activo,
        ),
    )
    return cursor.lastrowid


def seguir(con, id_seguidor: int, id_seguido: int) -> None:
    con.execute(
        "INSERT INTO seguimientos (id_seguidor, id_seguido, fecha_inicio) VALUES (?, ?, ?)",
        (id_seguidor, id_seguido, AHORA.isoformat()),
    )


def crear_mensaje(con, id_autor: int, texto: str, fecha: datetime | None = None) -> int:
    """Inserta un mensaje público y devuelve su id."""
    cursor = con.execute(
        "INSERT INTO mensajes (id_autor, texto, fecha_publicacion, editado, origen) "
        "VALUES (?, ?, ?, 0, 'WEB')",
        (id_autor, texto, (fecha or AHORA).isoformat()),
    )
    return cursor.lastrowid


def republicar(con, id_usuario: int, id_mensaje: int, fecha: datetime | None = None) -> None:
    con.execute(
        "INSERT INTO republicaciones (id_usuario, id_mensaje, fecha_republicacion) "
        "VALUES (?, ?, ?)",
        (id_usuario, id_mensaje, (fecha or AHORA).isoformat()),
    )


def contar(con, tabla: str) -> int:
    """Cuántas filas tiene una tabla. `tabla` siempre es un nombre escrito en la prueba."""
    return con.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()[0]


class PruebaConApp(unittest.TestCase):
    """Una aplicación nueva, con su base vacía, para cada prueba.

    Sirve para las pruebas que usan el cliente web (self.app.test_client()). Para
    sembrar o leer datos hay que abrir el contexto de la aplicación:

        with self.app.app_context():
            con = obtener_conexion()
    """

    def setUp(self) -> None:
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)

        # La base y la clave secreta son de la prueba. load_dotenv() no pisa variables
        # que ya existen, así que el .env de verdad no se usa.
        entorno = patch.dict(
            os.environ,
            {
                "SECRET_KEY": "clave-solo-para-pruebas",
                "BASE_DE_DATOS": os.path.join(carpeta.name, "prueba.sqlite3"),
            },
        )
        entorno.start()
        self.addCleanup(entorno.stop)

        self.app = crear_app()
        self.app.config["TESTING"] = True
        with self.app.app_context():
            inicializar_base()


class PruebaConBase(PruebaConApp):
    """Lo mismo, pero con el contexto abierto y la conexión a mano en self.con.

    Sirve para probar repositorios y controles directamente, sin pasar por HTTP.
    No usarla con el cliente web: con un contexto abierto, las peticiones lo
    comparten y se pierde el aislamiento entre una petición y la siguiente.
    """

    def setUp(self) -> None:
        super().setUp()
        contexto = self.app.app_context()
        contexto.push()
        self.addCleanup(contexto.pop)
        self.con = obtener_conexion()