"""OperacionSobreMensaje, Publicacion y Edicion: el patrón Template Method.

Publicar un mensaje y editarlo siguen los mismos pasos en el
mismo orden:

  1. autorizar        (gancho: por defecto no hace nada)
  2. validar el texto (siempre igual)
  3. analizar el texto, o sea extraer etiquetas, menciones y enlaces (siempre igual)
  4. guardar el mensaje   <- esto es lo que cambia: publicar CREA, editar ACTUALIZA
  5. reemplazar los elementos del mensaje (siempre igual)

Ese orden está escrito UNA sola vez, en OperacionSobreMensaje.ejecutar(), y
ninguna subclase lo redefine. Cada subclase completa solo los pasos que le
tocan. Así la regla del límite de caracteres y la llamada al analizador existen
en un único lugar, y la transacción no se le puede olvidar a nadie
porque está en el esqueleto.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import final

from miblog.acceso_datos.conexion import transaccion
from miblog.acceso_datos.repositorio_elementos import RepositorioElementos
from miblog.acceso_datos.repositorio_mensajes import RepositorioMensajes
from miblog.logica.dominio.elementos import ElementoExtraido
from miblog.logica.dominio.errores import (
    MensajeInexistenteError,
    TextoExcedidoError,
    TextoVacioError,
)
from miblog.logica.dominio.mensaje import MensajePublico
from miblog.logica.dominio.usuario import Usuario
from miblog.logica.gestion_mensajes.analizador import AnalizadorDeTexto


class OperacionSobreMensaje(ABC):
    """Clase abstracta del Template Method."""

    # Cuántos caracteres admite un mensaje. Es el único lugar del código donde
    # aparece este número: la vista lo toma de acá para mostrarlo en la pantalla.
    LIMITE = 140

    def __init__(
        self,
        analizador: AnalizadorDeTexto,
        repo_mensajes: RepositorioMensajes,
        repo_elementos: RepositorioElementos,
    ) -> None:
        self._analizador = analizador
        self._repo_mensajes = repo_mensajes
        self._repo_elementos = repo_elementos

    @final
    def ejecutar(self, usuario: Usuario, texto: str, **datos) -> MensajePublico:
        """El método plantilla: fija el orden de los pasos. Ninguna subclase lo redefine.

        Todo ocurre dentro de una transacción: si cualquier paso falla (texto
        inválido, error de la base), no queda nada a medias.
        """
        with transaccion():
            self._autorizar(usuario, **datos)
            texto = self._validar_texto(texto)
            elementos = self._analizador.analizar(texto)
            mensaje = self._persistir_mensaje(texto, usuario, **datos)
            self._reemplazar_elementos(mensaje, elementos)
            return mensaje

    # --- Paso gancho: las subclases pueden redefinirlo, o no ---

    def _autorizar(self, usuario: Usuario, **datos) -> None:
        """Por defecto no controla nada: publicar no necesita permiso especial."""

    # --- Pasos invariantes: iguales para toda operación ---

    def _validar_texto(self, texto: str) -> str:
        """Devuelve el texto listo para guardar, o lanza el error del curso alternativo.

        Se normalizan los saltos de línea: el navegador manda "\\r\\n" (dos
        caracteres) cuando se escribe un Enter, pero el contador de la pantalla
        cuenta uno solo. Sin esto, un mensaje con Enters podría pasar por el
        contador y ser rechazado acá.
        """
        texto = texto.replace("\r\n", "\n").replace("\r", "\n").strip()
        if not texto:
            raise TextoVacioError()
        if len(texto) > self.LIMITE:
            raise TextoExcedidoError(len(texto) - self.LIMITE)
        return texto

    def _reemplazar_elementos(
        self, mensaje: MensajePublico, elementos: list[ElementoExtraido]
    ) -> None:
        """Deja guardados exactamente los elementos del texto actual.

        Primero borra los que el mensaje tuviera (al publicar no hay ninguno; al
        editar sí) y después guarda los nuevos. Cada elemento sabe cómo guardarse.
        """
        self._repo_elementos.eliminar_de_mensaje(mensaje.id_mensaje)
        for elemento in elementos:
            elemento.guardar_en(self._repo_elementos, mensaje.id_mensaje)

    # --- Paso variable: cada subclase lo completa ---

    @abstractmethod
    def _persistir_mensaje(self, texto: str, usuario: Usuario, **datos) -> MensajePublico:
        """Guarda el mensaje y lo devuelve con su id. Publicar lo crea; editar lo actualiza."""


class Publicacion(OperacionSobreMensaje):
    """CU0004: publicar crea un mensaje nuevo. Solo redefine el paso variable."""

    def _persistir_mensaje(self, texto: str, usuario: Usuario, **datos) -> MensajePublico:
        mensaje = MensajePublico.publicar(usuario, texto, datetime.now(timezone.utc))
        mensaje.id_mensaje = self._repo_mensajes.crear(mensaje)
        return mensaje


class Edicion(OperacionSobreMensaje):
    """CU0005: editar actualiza un mensaje que ya existe. Completa dos pasos.

    Se ejecuta como `edicion.ejecutar(usuario, texto, id_mensaje=...)`: el id del
    mensaje viaja en `**datos`, que es el lugar que el esqueleto reserva para lo
    que solo una operación necesita. Validar el texto, analizarlo y reemplazar los
    elementos son los pasos compartidos con Publicacion: acá no se reescriben.
    """

    def _autorizar(self, usuario: Usuario, **datos) -> None:
        """Verifica la autoría DENTRO de la operación que modifica (rnf 5.1).

        Ya se verificó al abrir el diálogo, pero cada petición HTTP es
        independiente: entre abrir y confirmar el mensaje pudo borrarse (ca 5.1)
        o alguien pudo mandar el POST a mano (ca 5.2).
        """
        mensaje = self._buscar_mensaje(datos["id_mensaje"])
        mensaje.verificar_autoria(usuario.id_usuario)

    def _persistir_mensaje(self, texto: str, usuario: Usuario, **datos) -> MensajePublico:
        mensaje = self._buscar_mensaje(datos["id_mensaje"])
        # editar() pone texto, marca de editado y fecha juntos (diagrama de estados 7.1).
        mensaje.editar(texto, datetime.now(timezone.utc))
        self._repo_mensajes.actualizar_texto(mensaje)
        return mensaje

    def _buscar_mensaje(self, id_mensaje: int) -> MensajePublico:
        """El mensaje a editar, o MensajeInexistenteError si ya no existe (ca 5.1)."""
        mensaje = self._repo_mensajes.buscar_por_id(id_mensaje)
        if mensaje is None:
            raise MensajeInexistenteError()
        return mensaje