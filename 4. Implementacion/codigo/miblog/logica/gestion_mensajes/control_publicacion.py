"""ControlPublicacion: realiza CU0004 Publicar Mensaje.

No sabe de HTTP ni de SQL, y tampoco repite los pasos de publicar: recibe armada
la operación Publicacion (Template Method) y le pide que se ejecute. Por eso
publicar() queda en una línea.

Este control suma editar() y borrar() (CU0005, CU0006) y la
verificación de autoría, y recibe además la operación Edicion.
"""

from __future__ import annotations

from miblog.logica.dominio.mensaje import MensajePublico
from miblog.logica.dominio.usuario import Usuario
from miblog.logica.gestion_mensajes.operaciones_mensaje import Publicacion


class ControlPublicacion:
    def __init__(self, publicacion: Publicacion) -> None:
        self._publicacion = publicacion

    def publicar(self, autor: Usuario, texto: str) -> MensajePublico:
        """Publica el texto como mensaje de `autor`, o lanza el error del curso alternativo.

        Los errores posibles son TextoVacioError (ca 4.1) y TextoExcedidoError
        (ca 4.2). La sesión expirada (ca 4.3) no llega hasta acá: la atiende
        GuardiaSesion antes de que se ejecute la vista.
        """
        return self._publicacion.ejecutar(autor, texto)