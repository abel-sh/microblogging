"""AnalizadorDeTexto: el Contexto del patrón Strategy.

Recibe un texto y devuelve todos los elementos (etiquetas, menciones y enlaces)
que encuentra, pero no sabe cómo se busca ninguno: eso lo saben los extractores.
Los extractores le llegan por el constructor, ya armados. Este archivo no importa
ni nombra ninguno de los tres concretos, solo la interfaz común, Extractor.

Por eso agregar un cuarto tipo de elemento es escribir una clase nueva que
herede de Extractor y sumarla a la lista que arma crear_app(): ni este archivo
ni los controles que lo usan cambian.

Es el "único componente de extracción". Lo comparten la publicación y la edición de 
mensajes, y a futuro la API.
"""

from __future__ import annotations

from miblog.logica.dominio.elementos import ElementoExtraido
from miblog.logica.gestion_mensajes.extractores import Extractor


class AnalizadorDeTexto:
    def __init__(self, extractores: list[Extractor]) -> None:
        self._extractores = extractores

    def analizar(self, texto: str) -> list[ElementoExtraido]:
        """Los elementos que cada extractor encuentra en el texto, uno tras otro."""
        elementos: list[ElementoExtraido] = []
        for extractor in self._extractores:
            elementos.extend(extractor.extraer(texto))
        return elementos