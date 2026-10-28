"""RepositorioElementos: guarda las etiquetas, menciones y enlaces de un mensaje.

Realiza la interfaz RegistroDeElementos que define el dominio.
Así cada Etiqueta, Mencion o Enlace sabe "guardarse" llamando a un método de
RegistroDeElementos, sin saber que detrás hay SQLite: el dominio no importa
nada de esta capa, es esta capa la que importa al dominio.

Es la única clase que escribe SQL sobre etiquetas, mensaje_etiqueta, menciones
y enlaces. Todos los valores viajan como parámetros "?".

No abre transacciones: quien lo llama (la operación de publicar, en la capa de
lógica) ya abrió una, y todo lo que se guarda acá entra en ella (rnf 4.4).
"""

from __future__ import annotations

from miblog.acceso_datos.conexion import obtener_conexion
from miblog.logica.dominio.elementos import (
    Enlace,
    Etiqueta,
    Mencion,
    RegistroDeElementos,
)


class RepositorioElementos(RegistroDeElementos):
    def registrar_etiqueta(self, id_mensaje: int, etiqueta: Etiqueta) -> None:
        """Asocia la etiqueta al mensaje; si la etiqueta todavía no existe, la crea.

        Las etiquetas se comparten entre mensajes: "#pizza" es una sola fila en
        la tabla etiquetas, sin importar cuántos mensajes la usen. Por eso se
        intenta insertar y, si ya estaba (nombre UNIQUE), se la reutiliza.
        """
        conexion = obtener_conexion()
        conexion.execute(
            "INSERT OR IGNORE INTO etiquetas (nombre) VALUES (?)",
            (etiqueta.nombre,),
        )
        fila = conexion.execute(
            "SELECT id_etiqueta FROM etiquetas WHERE nombre = ?",
            (etiqueta.nombre,),
        ).fetchone()
        etiqueta.id_etiqueta = fila["id_etiqueta"]
        # OR IGNORE: si el mismo mensaje repite "#pizza #pizza", la asociación ya
        # existe y no se duplica (es la clave primaria de mensaje_etiqueta).
        conexion.execute(
            "INSERT OR IGNORE INTO mensaje_etiqueta (id_mensaje, id_etiqueta) VALUES (?, ?)",
            (id_mensaje, etiqueta.id_etiqueta),
        )

    def registrar_mencion(self, id_mensaje: int, mencion: Mencion) -> bool:
        """Guarda la mención si el usuario mencionado existe y está activo.

        Devuelve True si la guardó y False si la descartó (paso 7 de CU0004:
        mencionar a alguien que no existe no es un error, simplemente no deja
        mención). Se hace con un solo INSERT ... SELECT: el SELECT busca al
        usuario y, si no hay ninguno, no devuelve filas y no se inserta nada.
        La columna nombre_usuario es NOCASE, así que "@Ana" encuentra a "ana".
        """
        cursor = obtener_conexion().execute(
            "INSERT INTO menciones (id_mensaje, id_usuario_mencionado, posicion_en_texto)"
            " SELECT ?, id_usuario, ? FROM usuarios"
            " WHERE nombre_usuario = ? AND activo = 1",
            (id_mensaje, mencion.posicion_en_texto, mencion.nombre_usuario_mencionado),
        )
        return cursor.rowcount == 1

    def registrar_enlace(self, id_mensaje: int, enlace: Enlace) -> None:
        obtener_conexion().execute(
            "INSERT INTO enlaces (id_mensaje, url) VALUES (?, ?)",
            (id_mensaje, enlace.url),
        )

    def eliminar_de_mensaje(self, id_mensaje: int) -> None:
        """Borra las menciones, los enlaces y las asociaciones con etiquetas del mensaje.

        No borra las etiquetas mismas: son compartidas y otros mensajes pueden
        estar usándolas. Lo usa la edición (CU0005) para empezar de
        cero antes de volver a guardar lo que extrajo del texto nuevo.
        """
        conexion = obtener_conexion()
        conexion.execute("DELETE FROM menciones WHERE id_mensaje = ?", (id_mensaje,))
        conexion.execute("DELETE FROM enlaces WHERE id_mensaje = ?", (id_mensaje,))
        conexion.execute("DELETE FROM mensaje_etiqueta WHERE id_mensaje = ?", (id_mensaje,))