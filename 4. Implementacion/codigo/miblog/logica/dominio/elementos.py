"""Elementos extraídos del texto de un mensaje. 

Factory Method, lado Producto: ElementoExtraido es el producto abstracto y
Etiqueta, Mencion y Enlace son los productos concretos. Los Extractores (que
se escriben en otro bloque) son quienes los crean.

RegistroDeElementos es la interfaz que permite que cada elemento "sepa
guardarse" sin que el dominio dependa de la base de datos (DISEÑO §5.5,
inversión de dependencias). RepositorioElementos la va a realizar.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


class RegistroDeElementos(ABC):
    """Lo que el dominio le pide a quien guarda elementos."""

    @abstractmethod
    def registrar_etiqueta(self, id_mensaje: int, etiqueta: Etiqueta) -> None: ...

    @abstractmethod
    def registrar_mencion(self, id_mensaje: int, mencion: Mencion) -> bool: ...

    @abstractmethod
    def registrar_enlace(self, id_mensaje: int, enlace: Enlace) -> None: ...

    @abstractmethod
    def eliminar_de_mensaje(self, id_mensaje: int) -> None: ...


class ElementoExtraido(ABC):
    """Producto abstracto del Factory Method."""

    @abstractmethod
    def guardar_en(self, registro: RegistroDeElementos, id_mensaje: int) -> None: ...


@dataclass
class Etiqueta(ElementoExtraido):
    nombre: str
    id_etiqueta: int | None = None

    def guardar_en(self, registro: RegistroDeElementos, id_mensaje: int) -> None:
        registro.registrar_etiqueta(id_mensaje, self)


@dataclass
class Mencion(ElementoExtraido):
    nombre_usuario_mencionado: str
    posicion_en_texto: int

    def guardar_en(self, registro: RegistroDeElementos, id_mensaje: int) -> None:
        # registrar_mencion devuelve False si el usuario no existe (paso 7 de CU0004).
        # A quien guarda no le importa: la mención descartada simplemente no se guarda.
        registro.registrar_mencion(id_mensaje, self)


@dataclass
class Enlace(ElementoExtraido):
    url: str

    def guardar_en(self, registro: RegistroDeElementos, id_mensaje: int) -> None:
        registro.registrar_enlace(id_mensaje, self)