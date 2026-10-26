"""RepositorioSeguimientos: traduce entre la tabla seguimientos y la entidad Seguimiento.

Es la única clase que escribe SQL sobre seguimientos. Todos los valores viajan
como parámetros "?". La unicidad del par (seguidor, seguido) y la regla de que
nadie se sigue a sí mismo están además en la tabla (PRIMARY KEY y CHECK): son la
segunda barrera, por si el control fallara.
"""

from __future__ import annotations

from miblog.acceso_datos.conexion import obtener_conexion
from miblog.logica.dominio.seguimiento import Seguimiento


class RepositorioSeguimientos:
    def existe(self, id_seguidor: int, id_seguido: int) -> bool:
        """¿Ya hay un seguimiento de id_seguidor hacia id_seguido? (ca 11.3)"""
        fila = obtener_conexion().execute(
            "SELECT 1 FROM seguimientos WHERE id_seguidor = ? AND id_seguido = ?",
            (id_seguidor, id_seguido),
        ).fetchone()
        return fila is not None

    def crear(self, seguimiento: Seguimiento) -> None:
        obtener_conexion().execute(
            "INSERT INTO seguimientos (id_seguidor, id_seguido, fecha_inicio)"
            " VALUES (?, ?, ?)",
            (
                seguimiento.id_seguidor,
                seguimiento.id_seguido,
                seguimiento.fecha_inicio.isoformat(),
            ),
        )

    def buscar_ids_seguidos_de(self, id_usuario: int) -> set[int]:
        """Los ids de todos los usuarios a los que id_usuario sigue.

        Devuelve un set porque la búsqueda solo necesita preguntar "¿este id está
        ahí?" para cada resultado, y en un set esa pregunta es inmediata.
        """
        filas = obtener_conexion().execute(
            "SELECT id_seguido FROM seguimientos WHERE id_seguidor = ?",
            (id_usuario,),
        ).fetchall()
        return {fila["id_seguido"] for fila in filas}