"""ControlTablon: realiza CU0009 Visualizar Tablón.

Arma el tablón de un usuario: sus mensajes, los de la gente que sigue, y las
republicaciones hechas por unos y por otro, todo mezclado y ordenado del más
reciente al más antiguo.

El tablón no es una entidad guardada en ningún lado: es el resultado de este
cálculo, por eso no hay una clase Tablon.

Acá se ve para qué sirve el Decorator. Los mensajes y las republicaciones llegan
en dos listas distintas, pero este control los trata igual: a todos les pide
obtener_fecha_de_orden() y no necesita saber cuál es cuál. Cada uno responde con
la fecha que le corresponde (la de publicación o la de republicación).
"""

from __future__ import annotations

from miblog.acceso_datos.repositorio_mensajes import RepositorioMensajes
from miblog.acceso_datos.repositorio_republicaciones import RepositorioRepublicaciones
from miblog.logica.dominio.mensaje import ElementoDeTablon
from miblog.logica.dominio.usuario import Usuario


class ControlTablon:
    def __init__(
        self,
        repo_mensajes: RepositorioMensajes,
        repo_republicaciones: RepositorioRepublicaciones,
    ) -> None:
        self._repo_mensajes = repo_mensajes
        self._repo_republicaciones = repo_republicaciones

    def obtener_tablon(self, usuario: Usuario) -> list[ElementoDeTablon]:
        """Los elementos del tablón de `usuario`, del más reciente al más antiguo.

        Una lista vacía significa tablón vacío: no es un error, y la
        vista se encarga de mostrar el texto explicativo.
        """
        # Pasos 2 y 3 del curso normal: una consulta por repositorio.
        mensajes = self._repo_mensajes.buscar_publicos_para_tablon(usuario.id_usuario)
        republicaciones = self._repo_republicaciones.buscar_para_tablon(usuario.id_usuario)
        # Paso 4.
        return self._ordenar_por_fecha([*mensajes, *republicaciones])

    def _ordenar_por_fecha(self, elementos: list[ElementoDeTablon]) -> list[ElementoDeTablon]:
        # Sin ningún "if" por tipo (regla RA07): cada elemento dice su propia fecha.
        return sorted(elementos, key=lambda e: e.obtener_fecha_de_orden(), reverse=True)