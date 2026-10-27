"""ControlRepublicacion: realiza CU0007 Republicar Mensaje.

No sabe de HTTP. Recibe quién republica (el Usuario de la sesión) y qué mensaje
(un id, porque viene en la URL), y o registra la republicación o lanza el error de
negocio del curso alternativo que corresponda.

Una republicación no copia el texto: guarda solo quién, cuándo y a qué mensaje
apunta. Por eso este control nunca lee ni escribe texto de mensajes.

Abre una transacción para que "verificar que no la hizo ya" y "crear" queden bajo
el mismo bloqueo: dos clics casi simultáneos no pueden pasar los dos la verificación.
"""

from __future__ import annotations

from datetime import datetime, timezone

from miblog.acceso_datos.conexion import transaccion
from miblog.acceso_datos.repositorio_mensajes import RepositorioMensajes
from miblog.acceso_datos.repositorio_republicaciones import RepositorioRepublicaciones
from miblog.acceso_datos.repositorio_seguimientos import RepositorioSeguimientos
from miblog.logica.dominio.errores import (
    AutorNoSeguidoError,
    MensajeInexistenteError,
    MensajePropioError,
    RepublicacionExistenteError,
)
from miblog.logica.dominio.mensaje import MensajePublico
from miblog.logica.dominio.usuario import Usuario


class ControlRepublicacion:
    def __init__(
        self,
        repo_mensajes: RepositorioMensajes,
        repo_seguimientos: RepositorioSeguimientos,
        repo_republicaciones: RepositorioRepublicaciones,
    ) -> None:
        self._repo_mensajes = repo_mensajes
        self._repo_seguimientos = repo_seguimientos
        self._repo_republicaciones = repo_republicaciones

    def republicar(self, usuario: Usuario, id_mensaje: int) -> int:
        """Registra que `usuario` republica el mensaje y devuelve el id de la republicación.

        Las verificaciones van en el orden de DISEÑO §6.7, y el orden importa:
        primero que el mensaje exista (ca 7.4: sin mensaje no hay nada para
        verificar), después que no sea propio (ca 7.2), después que se siga a su
        autor (ca 7.1) y por último que no esté ya republicado (ca 7.3).
        """
        with transaccion():
            mensaje = self._repo_mensajes.buscar_por_id(id_mensaje)
            if mensaje is None:
                raise MensajeInexistenteError()
            self._verificar_no_es_propio(usuario, mensaje)
            self._verificar_sigue_al_autor(usuario, mensaje)
            self._verificar_no_duplicada(usuario, id_mensaje)
            # Paso 4: solo quién, cuándo y la referencia. No se copia el texto.
            return self._repo_republicaciones.crear(
                usuario.id_usuario, id_mensaje, datetime.now(timezone.utc)
            )

    def _verificar_no_es_propio(self, usuario: Usuario, mensaje: MensajePublico) -> None:
        # Va antes que "sigue al autor": uno no puede seguirse a sí mismo (ca 11.2),
        # y un mensaje propio caería en ca 7.1 con un aviso que no corresponde.
        if mensaje.es_autor(usuario.id_usuario):
            raise MensajePropioError()

    def _verificar_sigue_al_autor(self, usuario: Usuario, mensaje: MensajePublico) -> None:
        if not self._repo_seguimientos.existe(usuario.id_usuario, mensaje.autor.id_usuario):
            raise AutorNoSeguidoError()

    def _verificar_no_duplicada(self, usuario: Usuario, id_mensaje: int) -> None:
        if self._repo_republicaciones.existe(usuario.id_usuario, id_mensaje):
            raise RepublicacionExistenteError()