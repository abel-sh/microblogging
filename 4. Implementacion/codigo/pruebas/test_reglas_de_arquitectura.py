"""Las seis comprobaciones mecánicas, como pruebas.

Son los mismos `grep` que se corrían a mano al cerrar cada bloque. Acá buscan lo
mismo en los mismos lugares, así que una sola orden las corre todas y avisa en
cuanto un cambio rompe una regla del diseño.

    python -m unittest pruebas.test_reglas_de_arquitectura -v
"""

from __future__ import annotations

import os
import re
import unittest

from miblog.logica.gestion_mensajes.operaciones_mensaje import OperacionSobreMensaje

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../codigo
EXTENSIONES = (".py", ".html", ".js", ".css", ".sql")


def coincidencias(patron: str, carpeta: str, excluir: str | None = None) -> list[str]:
    """Como `grep -rn patron carpeta`: devuelve "ruta:línea" de cada línea que coincide.

    Recorre todos los archivos de texto de la carpeta. Si se da `excluir`, deja de
    lado las rutas que lo contienen (equivale a `| grep -v excluir`).
    """
    regex = re.compile(patron)
    encontradas = []
    for directorio, subcarpetas, archivos in os.walk(os.path.join(RAIZ, carpeta)):
        subcarpetas[:] = [s for s in subcarpetas if s not in ("__pycache__", "fotos", "fuentes")]
        for nombre in archivos:
            if not nombre.endswith(EXTENSIONES):
                continue
            ruta = os.path.join(directorio, nombre)
            relativa = os.path.relpath(ruta, RAIZ).replace(os.sep, "/")
            if excluir and excluir in relativa:
                continue
            with open(ruta, encoding="utf-8") as archivo:
                for numero, linea in enumerate(archivo, start=1):
                    if regex.search(linea):
                        encontradas.append(f"{relativa}:{numero}")
    return encontradas


class PruebaReglasDeArquitectura(unittest.TestCase):
    def test_1_el_limite_de_caracteres_se_escribe_una_sola_vez(self):
        # rnf 4.2 y ANALISIS §8.8: el único lugar es OperacionSobreMensaje.LIMITE.
        halladas = coincidencias(r"140", "miblog/logica")
        self.assertEqual(len(halladas), 1, halladas)
        self.assertTrue(halladas[0].startswith("miblog/logica/gestion_mensajes/operaciones_mensaje.py"))
        self.assertEqual(OperacionSobreMensaje.LIMITE, 140)  # lo que fija el enunciado

    def test_2_nadie_pregunta_de_que_tipo_es_un_elemento_del_tablon(self):
        # Decorator (ANALISIS §8.5): cero isinstance y cero es_republicacion.
        halladas = coincidencias(r"isinstance|es_republicacion", "miblog/logica")
        halladas += coincidencias(r"isinstance|es_republicacion", "miblog/presentacion")
        self.assertEqual(halladas, [])

    def test_3_el_analizador_no_nombra_ningun_extractor_concreto(self):
        # Strategy (ANALISIS §8.3): solo conoce la interfaz Extractor.
        halladas = coincidencias(r"Extractor[A-Z]", "miblog/logica/gestion_mensajes")
        propias = [h for h in halladas if h.startswith("miblog/logica/gestion_mensajes/analizador.py")]
        self.assertEqual(propias, [])

    def test_4_la_presentacion_no_llega_a_la_base_de_datos(self):
        # RNF25.
        self.assertEqual(coincidencias(r"acceso_datos|sqlite3", "miblog/presentacion"), [])

    def test_5_el_sql_solo_vive_en_acceso_datos(self):
        self.assertEqual(coincidencias(r"execute\(", "miblog", excluir="acceso_datos"), [])

    def test_6_el_dominio_no_depende_del_acceso_a_datos(self):
        # Inversión de dependencias: el dominio define RegistroDeElementos y la capa
        # de datos lo implementa, no al revés.
        self.assertEqual(coincidencias(r"acceso_datos", "miblog/logica/dominio"), [])


if __name__ == "__main__":
    unittest.main()