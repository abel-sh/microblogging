"""Republicacion: el Decorador del patrón Decorator.

Una republicación NO tiene texto propio (característica C23). Cuando le piden
el texto, el autor, el id o la marca de editado, se lo pide al mensaje
original. Por eso, si el autor edita su mensaje, todas las republicaciones
muestran el texto nuevo sin que nadie las toque.

Solo agrega dos cosas: quién republicó y cuándo.
"""

from __future__ import annotations

from datetime import datetime

from miblog.logica.dominio.mensaje import ElementoDeTablon, MensajePublico
from miblog.logica.dominio.usuario import Usuario


class Republicacion(ElementoDeTablon):
    def __init__(
        self,
        id_republicacion: int,
        republicador: Usuario,
        fecha_republicacion: datetime,
        original: MensajePublico,
    ) -> None:
        self.id_republicacion = id_republicacion
        self.republicador = republicador
        self.fecha_republicacion = fecha_republicacion
        # El tipo es MensajePublico y no ElementoDeTablon a propósito: una
        # republicación no se puede republicar.
        self._original = original

    # --- Cinco métodos que delega en el original ---

    def obtener_texto_vigente(self) -> str:
        return self._original.obtener_texto_vigente()

    def obtener_autor_original(self) -> Usuario:
        return self._original.obtener_autor_original()

    def obtener_id_mensaje(self) -> int:
        return self._original.obtener_id_mensaje()

    def esta_editado(self) -> bool:
        return self._original.esta_editado()

    def obtener_fecha_ultima_edicion(self) -> datetime | None:
        return self._original.obtener_fecha_ultima_edicion()

    # --- Dos métodos que responde con datos propios ---

    def obtener_fecha_de_orden(self) -> datetime:
        return self.fecha_republicacion

    def obtener_republicador(self) -> Usuario:
        return self.republicador