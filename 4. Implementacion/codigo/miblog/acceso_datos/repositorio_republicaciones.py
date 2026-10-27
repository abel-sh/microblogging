"""RepositorioRepublicaciones: traduce entre la tabla republicaciones y la entidad Republicacion.

Es la única clase que escribe SQL sobre republicaciones. Todos los valores viajan
como parámetros "?"; nunca se arma una sentencia pegando texto.

Una Republicacion no guarda texto: apunta a un mensaje original. Por eso la
consulta trae, en la misma fila, la republicación, el mensaje al que apunta (con
su texto VIGENTE, o sea el de hoy), el autor de ese mensaje y el usuario que lo
republicó.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime

from miblog.acceso_datos.conexion import obtener_conexion
from miblog.acceso_datos.repositorio_mensajes import (
    construir_mensaje,
    construir_usuario_resumido,
)
from miblog.logica.dominio.republicacion import Republicacion


class RepositorioRepublicaciones:
    # --- Bloque 4.4: visualizar el tablón (CU0009) ---

    def buscar_para_tablon(self, id_usuario: int) -> list[Republicacion]:
        """Las republicaciones hechas por id_usuario o por cualquiera de los que sigue.

        Es la segunda de las dos consultas del tablón. La condición
        es sobre quién REPUBLICÓ, no sobre quién escribió el original: si alguien
        a quien seguís republica un mensaje de un desconocido, aparece en tu
        tablón. Como el texto sale del mensaje original, si
        su autor lo editó acá ya viene el texto nuevo.
        """
        filas = obtener_conexion().execute(
            "SELECT r.id_republicacion, r.fecha_republicacion,"
            " m.id_mensaje, m.texto, m.fecha_publicacion, m.fecha_ultima_edicion,"
            " m.editado, m.origen,"
            " a.id_usuario AS autor_id_usuario, a.nombre_usuario AS autor_nombre_usuario,"
            " a.nombre_completo AS autor_nombre_completo, a.url_foto AS autor_url_foto,"
            " p.id_usuario AS republicador_id_usuario,"
            " p.nombre_usuario AS republicador_nombre_usuario,"
            " p.nombre_completo AS republicador_nombre_completo,"
            " p.url_foto AS republicador_url_foto"
            " FROM republicaciones AS r"
            " JOIN mensajes AS m ON m.id_mensaje = r.id_mensaje"
            " JOIN usuarios AS a ON a.id_usuario = m.id_autor"
            " JOIN usuarios AS p ON p.id_usuario = r.id_usuario"
            " WHERE r.id_usuario = ?"
            " OR r.id_usuario IN (SELECT id_seguido FROM seguimientos WHERE id_seguidor = ?)",
            (id_usuario, id_usuario),
        ).fetchall()
        return [self._construir_republicacion(fila) for fila in filas]

    def _construir_republicacion(self, fila: sqlite3.Row) -> Republicacion:
        return Republicacion(
            id_republicacion=fila["id_republicacion"],
            republicador=construir_usuario_resumido(fila, "republicador_"),
            fecha_republicacion=datetime.fromisoformat(fila["fecha_republicacion"]),
            original=construir_mensaje(fila),
        )