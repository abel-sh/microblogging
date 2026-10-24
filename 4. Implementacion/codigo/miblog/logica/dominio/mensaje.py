"""ElementoDeTablon, Mensaje y MensajePublico   .

Decorator, lado Componente y ComponenteConcreto:
  - ElementoDeTablon     = Componente (la interfaz que usa el tablón).
  - MensajePublico       = ComponenteConcreto.
  - Republicacion        = Decorador (está en republicacion.py).

ElementoDeTablon vive acá, junto a MensajePublico, para que republicacion.py
pueda importar los dos sin que haya un ciclo de importaciones.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from miblog.logica.dominio.enumeraciones import OrigenPublicacion
from miblog.logica.dominio.errores import NoEsAutorError
from miblog.logica.dominio.usuario import Usuario


class ElementoDeTablon(ABC):
    """Lo único que el tablón sabe pedirle a lo que muestra."""

    @abstractmethod
    def obtener_fecha_de_orden(self) -> datetime: ...

    @abstractmethod
    def obtener_texto_vigente(self) -> str: ...

    @abstractmethod
    def obtener_autor_original(self) -> Usuario: ...

    @abstractmethod
    def obtener_id_mensaje(self) -> int: ...

    @abstractmethod
    def esta_editado(self) -> bool: ...

    @abstractmethod
    def obtener_fecha_ultima_edicion(self) -> datetime | None: ...

    @abstractmethod
    def obtener_republicador(self) -> Usuario | None: ...


@dataclass(kw_only=True)
class Mensaje(ABC):
    """Datos y reglas comunes a todo mensaje. Es abstracta: no se instancia sola."""

    id_mensaje: int | None = None
    autor: Usuario
    texto: str
    fecha_publicacion: datetime
    fecha_ultima_edicion: datetime | None = None
    editado: bool = False
    origen: OrigenPublicacion = OrigenPublicacion.WEB

    def __post_init__(self) -> None:
        # Mensaje no tiene métodos abstractos, así que ABC solo no alcanza para
        # impedir Mensaje(...). Este control hace que "abstracta" sea verdad.
        if type(self) is Mensaje:
            raise TypeError("Mensaje es abstracta: usá MensajePublico.")

    def es_autor(self, id_usuario: int) -> bool:
        return self.autor.id_usuario == id_usuario

    def verificar_autoria(self, id_usuario: int) -> None:
        """Lanza NoEsAutorError si id_usuario no es el autor (rnf 5.1, rnf 6.1)."""
        if not self.es_autor(id_usuario):
            raise NoEsAutorError()


class MensajePublico(Mensaje, ElementoDeTablon):
    """El único tipo de mensaje de esta versión (el privado es CU0008, fuera de alcance)."""

    @staticmethod
    def publicar(autor: Usuario, texto: str, fecha: datetime) -> MensajePublico:
        """Crea un mensaje en estado Publicado (diagrama de estados 7.1)."""
        return MensajePublico(
            autor=autor,
            texto=texto,
            fecha_publicacion=fecha,
            fecha_ultima_edicion=None,
            editado=False,
            origen=OrigenPublicacion.WEB,
        )

    def editar(self, texto: str, fecha: datetime) -> None:
        """Pasa a Editado. Pone los dos atributos juntos, como exige el CHECK de la tabla."""
        self.texto = texto
        self.editado = True
        self.fecha_ultima_edicion = fecha

    # --- Interfaz ElementoDeTablon: responde con sus propios datos ---

    def obtener_fecha_de_orden(self) -> datetime:
        return self.fecha_publicacion

    def obtener_texto_vigente(self) -> str:
        return self.texto

    def obtener_autor_original(self) -> Usuario:
        return self.autor

    def obtener_id_mensaje(self) -> int:
        return self.id_mensaje

    def esta_editado(self) -> bool:
        return self.editado

    def obtener_fecha_ultima_edicion(self) -> datetime | None:
        return self.fecha_ultima_edicion

    def obtener_republicador(self) -> None:
        # Un mensaje común no fue republicado por nadie. Devolver None es lo que
        # evita que la plantilla pregunte "¿qué tipo de elemento sos?".
        return None