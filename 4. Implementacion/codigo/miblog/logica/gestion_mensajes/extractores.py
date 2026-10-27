"""Extractor y sus tres variantes: la familia de Strategy y Factory Method.

Un Extractor sabe encontrar UNA clase de elemento dentro de un texto: las
etiquetas (#), las menciones (@) o los enlaces (http). Todos funcionan igual,
y esa forma común está escrita una sola vez, en Extractor.extraer():

  1. pedir el patrón (cada subclase dice cuál es el suyo);
  2. buscar todas las coincidencias en el texto;
  3. por cada una, pedirle a la subclase que fabrique el objeto.

Strategy: cada subclase es una estrategia intercambiable. AnalizadorDeTexto las
recibe por constructor y no sabe cuáles son.
Factory Method: crear_elemento() es el método de fábrica. Cada subclase decide
qué clase instancia (Etiqueta, Mencion o Enlace); la clase base no tiene ningún
"if" por tipo.

Los extractores solo leen texto y crean objetos en memoria. No tocan la base de
datos: guardar es cosa de cada elemento (ElementoExtraido.guardar_en).
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod

from miblog.logica.dominio.elementos import ElementoExtraido, Enlace, Etiqueta, Mencion


class Extractor(ABC):
    """Interfaz común de la familia (Strategy) y creador abstracto (Factory Method)."""

    def extraer(self, texto: str) -> list[ElementoExtraido]:
        """Todos los elementos de este tipo que aparecen en el texto, en orden."""
        return [
            self.crear_elemento(coincidencia)
            for coincidencia in re.finditer(self.patron(), texto)
        ]

    @abstractmethod
    def patron(self) -> str:
        """Expresión regular que encuentra este tipo de elemento."""

    @abstractmethod
    def crear_elemento(self, coincidencia: re.Match) -> ElementoExtraido:
        """Método de fábrica: arma el objeto a partir de una coincidencia del patrón."""


class ExtractorEtiquetas(Extractor):
    """Encuentra #etiquetas."""

    def patron(self) -> str:
        # "#" seguido de letras, números o guion bajo. El (?<![\w/]) pide que antes
        # del "#" no haya una letra ni una barra: así "C#" o el "#seccion" de una URL
        # ("https://sitio.com/a/#seccion") no cuentan como etiqueta.
        return r"(?<![\w/])#(\w+)"

    def crear_elemento(self, coincidencia: re.Match) -> Etiqueta:
        # Se guarda en minúsculas para que #Pizza y #pizza sean la misma etiqueta
        # (la columna etiquetas.nombre distingue mayúsculas de minúsculas).
        return Etiqueta(nombre=coincidencia.group(1).lower())


class ExtractorMenciones(Extractor):
    """Encuentra @menciones."""

    def patron(self) -> str:
        # "@" seguido de un nombre. Igual que en las etiquetas, el (?<![\w/]) evita
        # que "ana@empresa.com" cuente como una mención a "empresa" y que
        # "https://medium.com/@autor" cuente como una mención a "autor".
        # El nombre admite "." y "-" pero solo EN EL MEDIO ("juan.perez", "ana-lopez"):
        # así, en "hola @ana." el punto final es de la frase y no del nombre.
        return r"(?<![\w/])@(\w+(?:[.\-]\w+)*)"

    def crear_elemento(self, coincidencia: re.Match) -> Mencion:
        # Siempre crea la mención; si el usuario no existe, se descarta recién al
        # guardar (RepositorioElementos.registrar_mencion devuelve False).
        # La posición es la del "@" dentro del texto.
        return Mencion(
            nombre_usuario_mencionado=coincidencia.group(1),
            posicion_en_texto=coincidencia.start(),
        )


class ExtractorEnlaces(Extractor):
    """Encuentra enlaces que empiezan con http:// o https://."""

    def patron(self) -> str:
        # Todo lo que no sea un espacio, pero sin contar como parte del enlace la
        # puntuación del final: en "mirá https://sitio.com." el punto es de la frase.
        return r"(?i)https?://\S*[^\s.,;:!?)\]}>\"']"

    def crear_elemento(self, coincidencia: re.Match) -> Enlace:
        return Enlace(url=coincidencia.group(0))