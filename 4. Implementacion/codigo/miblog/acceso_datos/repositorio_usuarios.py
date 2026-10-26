"""RepositorioUsuarios: traduce entre la tabla usuarios y la entidad Usuario.

Es la única clase que escribe SQL sobre usuarios. Todos los valores viajan como
parámetros "?"; nunca se arma una sentencia pegando texto.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime

from miblog.acceso_datos.conexion import obtener_conexion
from miblog.logica.dominio.enumeraciones import RolUsuario
from miblog.logica.dominio.usuario import Usuario


def construir_usuario(fila: sqlite3.Row) -> Usuario:
    """Convierte una fila de la tabla usuarios en un objeto Usuario.

    Es una función del módulo, no un método, porque RepositorioSesiones también
    la necesita (su consulta trae las columnas de usuarios con un JOIN).
    """
    return Usuario(
        id_usuario=fila["id_usuario"],
        nombre_usuario=fila["nombre_usuario"],
        email=fila["email"],
        clave_hash=fila["clave_hash"],
        nombre_completo=fila["nombre_completo"],
        descripcion=fila["descripcion"],
        url_foto=fila["url_foto"],
        rol=RolUsuario(fila["rol"]),
        fecha_alta=datetime.fromisoformat(fila["fecha_alta"]),
        activo=bool(fila["activo"]),
    )


class RepositorioUsuarios:
    def existe_nombre_usuario(self, nombre_usuario: str) -> bool:
        # La columna es COLLATE NOCASE: "Abel" y "abel" cuentan como el mismo nombre.
        fila = obtener_conexion().execute(
            "SELECT 1 FROM usuarios WHERE nombre_usuario = ?",
            (nombre_usuario,),
        ).fetchone()
        return fila is not None

    def existe_email(self, email: str) -> bool:
        fila = obtener_conexion().execute(
            "SELECT 1 FROM usuarios WHERE email = ?",
            (email,),
        ).fetchone()
        return fila is not None

    def crear(self, usuario: Usuario) -> int:
        """Inserta el usuario y devuelve el id que le dio la base."""
        cursor = obtener_conexion().execute(
            "INSERT INTO usuarios (nombre_usuario, email, clave_hash, nombre_completo,"
            " descripcion, url_foto, rol, fecha_alta, activo)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                usuario.nombre_usuario,
                usuario.email,
                usuario.clave_hash,
                usuario.nombre_completo,
                usuario.descripcion,
                usuario.url_foto,
                usuario.rol.value,
                usuario.fecha_alta.isoformat(),
                1 if usuario.activo else 0,
            ),
        )
        return cursor.lastrowid

    def buscar_activo_por_nombre_usuario(self, nombre_usuario: str) -> Usuario | None:
        fila = obtener_conexion().execute(
            "SELECT * FROM usuarios WHERE nombre_usuario = ? AND activo = 1",
            (nombre_usuario,),
        ).fetchone()
        return construir_usuario(fila) if fila is not None else None