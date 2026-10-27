"""RepositorioMensajes: traduce entre la tabla mensajes y la entidad MensajePublico.

Es la única clase que escribe SQL sobre mensajes. Todos los valores viajan como
parámetros "?"; nunca se arma una sentencia pegando texto.

Cuando una consulta trae mensajes, trae también a su autor (con un JOIN): así
cada MensajePublico llega completo, sin ir a buscar al autor mensaje por mensaje.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime

from miblog.acceso_datos.conexion import obtener_conexion
from miblog.logica.dominio.enumeraciones import OrigenPublicacion
from miblog.logica.dominio.mensaje import MensajePublico
from miblog.logica.dominio.usuario import Usuario


def construir_usuario_resumido(fila: sqlite3.Row, prefijo: str) -> Usuario:
    """Arma un Usuario "para mostrar" a partir de columnas que empiezan con `prefijo`.

    Las consultas con JOIN traen el autor (y, en las republicaciones, también al
    republicador) con nombres como "autor_nombre_usuario", porque dos usuarios en
    la misma fila no pueden llamar igual a sus columnas. El prefijo dice de cuál
    de los dos se trata.

    Solo se cargan los datos que el tablón muestra: no viajan el correo ni el hash
    de la clave de gente que no es el usuario de la sesión. Los demás campos
    quedan con los valores por defecto de Usuario y no hay que consultarlos.
    """
    return Usuario(
        id_usuario=fila[prefijo + "id_usuario"],
        nombre_usuario=fila[prefijo + "nombre_usuario"],
        nombre_completo=fila[prefijo + "nombre_completo"],
        url_foto=fila[prefijo + "url_foto"],
    )


def construir_mensaje(fila: sqlite3.Row) -> MensajePublico:
    """Convierte una fila de mensajes JOIN usuarios en un MensajePublico.

    La fila tiene que traer las columnas de mensajes sin prefijo (id_mensaje,
    texto, fecha_publicacion, fecha_ultima_edicion, editado, origen) y las del
    autor con el prefijo "autor_". Es una función del módulo porque
    RepositorioRepublicaciones también la necesita.
    """
    return MensajePublico(
        id_mensaje=fila["id_mensaje"],
        autor=construir_usuario_resumido(fila, "autor_"),
        texto=fila["texto"],
        fecha_publicacion=datetime.fromisoformat(fila["fecha_publicacion"]),
        fecha_ultima_edicion=_fecha_desde_texto(fila["fecha_ultima_edicion"]),
        editado=bool(fila["editado"]),
        origen=OrigenPublicacion(fila["origen"]),
    )


class RepositorioMensajes:
    # --- Bloque 4.4: publicar (CU0004) y visualizar el tablón (CU0009) ---

    def crear(self, mensaje: MensajePublico) -> int:
        """Inserta el mensaje y devuelve el id que le dio la base."""
        cursor = obtener_conexion().execute(
            "INSERT INTO mensajes (id_autor, texto, fecha_publicacion,"
            " fecha_ultima_edicion, editado, origen)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (
                mensaje.autor.id_usuario,
                mensaje.texto,
                mensaje.fecha_publicacion.isoformat(),
                _fecha_a_texto(mensaje.fecha_ultima_edicion),
                1 if mensaje.editado else 0,
                mensaje.origen.value,
            ),
        )
        return cursor.lastrowid

    def buscar_publicos_para_tablon(self, id_usuario: int) -> list[MensajePublico]:
        """Los mensajes de id_usuario y de todos los que sigue, con su autor.

        Los pasos 2 y 3 de CU0009 ("a quién sigue" y "reunir sus mensajes") van
        en una sola consulta: la subconsulta de seguimientos reemplaza al viaje
        extra a la base (DISEÑO §6.8). El orden no se decide acá sino en
        ControlTablon, que tiene que mezclar estos mensajes con las
        republicaciones (rnf 9.2, RA07).
        """
        filas = obtener_conexion().execute(
            "SELECT m.id_mensaje, m.texto, m.fecha_publicacion, m.fecha_ultima_edicion,"
            " m.editado, m.origen,"
            " a.id_usuario AS autor_id_usuario, a.nombre_usuario AS autor_nombre_usuario,"
            " a.nombre_completo AS autor_nombre_completo, a.url_foto AS autor_url_foto"
            " FROM mensajes AS m"
            " JOIN usuarios AS a ON a.id_usuario = m.id_autor"
            " WHERE m.id_autor = ?"
            " OR m.id_autor IN (SELECT id_seguido FROM seguimientos WHERE id_seguidor = ?)",
            (id_usuario, id_usuario),
        ).fetchall()
        return [construir_mensaje(fila) for fila in filas]

    # --- Bloque 4.5: editar (CU0005), borrar (CU0006) y republicar (CU0007) ---

    def buscar_por_id(self, id_mensaje: int) -> MensajePublico | None:
        """El mensaje con ese id, con su autor, o None si no existe (o ya lo borraron).

        Lo usan los tres casos de uso del bloque: editar y borrar para verificar la
        autoría (rnf 5.1, rnf 6.1) y republicar para saber de quién es el original.
        No filtra por usuario: quién puede hacer qué con el mensaje lo decide la
        lógica, no esta consulta.
        """
        fila = obtener_conexion().execute(
            "SELECT m.id_mensaje, m.texto, m.fecha_publicacion, m.fecha_ultima_edicion,"
            " m.editado, m.origen,"
            " a.id_usuario AS autor_id_usuario, a.nombre_usuario AS autor_nombre_usuario,"
            " a.nombre_completo AS autor_nombre_completo, a.url_foto AS autor_url_foto"
            " FROM mensajes AS m"
            " JOIN usuarios AS a ON a.id_usuario = m.id_autor"
            " WHERE m.id_mensaje = ?",
            (id_mensaje,),
        ).fetchone()
        return construir_mensaje(fila) if fila is not None else None

    def actualizar_texto(self, mensaje: MensajePublico) -> int:
        """Guarda el texto nuevo, la marca de editado y la fecha de la última edición.

        Escribe las tres columnas juntas, como exige el CHECK de la tabla (diagrama
        de estados 7.1): un mensaje editado siempre tiene fecha de edición.
        Devuelve cuántas filas cambió (1 si el mensaje existe, 0 si no).
        """
        cursor = obtener_conexion().execute(
            "UPDATE mensajes SET texto = ?, editado = ?, fecha_ultima_edicion = ?"
            " WHERE id_mensaje = ?",
            (
                mensaje.texto,
                1 if mensaje.editado else 0,
                _fecha_a_texto(mensaje.fecha_ultima_edicion),
                mensaje.id_mensaje,
            ),
        )
        return cursor.rowcount

    def eliminar(self, id_mensaje: int) -> int:
        """Borra la fila del mensaje. Devuelve cuántas filas borró.

        Es el ÚLTIMO paso del borrado: antes, ControlPublicacion borró
        las republicaciones y los elementos. Si no lo hubiera hecho, las claves
        foráneas harían fallar este DELETE y la transacción volvería atrás.
        """
        cursor = obtener_conexion().execute(
            "DELETE FROM mensajes WHERE id_mensaje = ?",
            (id_mensaje,),
        )
        return cursor.rowcount


def _fecha_a_texto(fecha: datetime | None) -> str | None:
    """datetime -> texto ISO 8601, que es como se guardan las fechas. None sigue siendo None."""
    return fecha.isoformat() if fecha is not None else None


def _fecha_desde_texto(texto: str | None) -> datetime | None:
    """Texto ISO 8601 -> datetime. None sigue siendo None."""
    return datetime.fromisoformat(texto) if texto is not None else None