"""RepositorioSesiones: la tabla técnica sesiones.

No hay clase de dominio Sesion: esta tabla solo la conoce este repositorio.
Guarda el hash SHA-256 del token, nunca el token (así una copia del archivo de
la base no sirve para armar una cookie). El hash lo calcula ControlAutenticacion;
acá solo llega como texto.
"""

from __future__ import annotations

from datetime import datetime

from miblog.acceso_datos.conexion import obtener_conexion
from miblog.acceso_datos.repositorio_usuarios import construir_usuario
from miblog.logica.dominio.usuario import Usuario


class RepositorioSesiones:
    def crear(self, hash_token: str, id_usuario: int, fecha_expiracion: datetime) -> None:
        obtener_conexion().execute(
            "INSERT INTO sesiones (hash_token, id_usuario, fecha_expiracion)"
            " VALUES (?, ?, ?)",
            (hash_token, id_usuario, fecha_expiracion.isoformat()),
        )

    def buscar_usuario_vigente(self, hash_token: str, ahora: datetime) -> Usuario | None:
        """El dueño de una sesión que existe, no venció y sigue activo; si no, None.

        La comparación con `ahora` está en la consulta: una sesión vencida nunca
        se acepta, aunque su fila todavía no se haya borrado.
        """
        fila = obtener_conexion().execute(
            "SELECT u.* FROM sesiones s"
            " JOIN usuarios u ON u.id_usuario = s.id_usuario"
            " WHERE s.hash_token = ? AND s.fecha_expiracion > ? AND u.activo = 1",
            (hash_token, ahora.isoformat()),
        ).fetchone()
        return construir_usuario(fila) if fila is not None else None

    def eliminar(self, hash_token: str) -> int:
        """Borra la sesión (cerrar sesión). Devuelve cuántas filas borró: 0 o 1."""
        cursor = obtener_conexion().execute(
            "DELETE FROM sesiones WHERE hash_token = ?",
            (hash_token,),
        )
        return cursor.rowcount

    def eliminar_si_vencida(self, hash_token: str, ahora: datetime) -> int:
        """Limpieza al validar: borra esa sesión solo si ya venció."""
        cursor = obtener_conexion().execute(
            "DELETE FROM sesiones WHERE hash_token = ? AND fecha_expiracion <= ?",
            (hash_token, ahora.isoformat()),
        )
        return cursor.rowcount

    def eliminar_vencidas(self, ahora: datetime) -> int:
        """Limpieza al iniciar sesión: borra las vencidas de todos los usuarios."""
        cursor = obtener_conexion().execute(
            "DELETE FROM sesiones WHERE fecha_expiracion <= ?",
            (ahora.isoformat(),),
        )
        return cursor.rowcount