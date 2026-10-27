"""Pruebas de los extractores y del analizador.

Son las únicas pruebas que no necesitan base de datos: trabajan solo con texto.
"""

from __future__ import annotations

import unittest

from miblog.logica.dominio.elementos import ElementoExtraido, Enlace, Etiqueta, Mencion
from miblog.logica.gestion_mensajes.analizador import AnalizadorDeTexto
from miblog.logica.gestion_mensajes.extractores import (
    Extractor,
    ExtractorEnlaces,
    ExtractorEtiquetas,
    ExtractorMenciones,
)


class PruebaFormaDelPatron(unittest.TestCase):
    """Strategy + Factory Method: que la estructura del diseño exista de verdad."""

    def test_extractor_es_abstracto(self):
        with self.assertRaises(TypeError):
            Extractor()

    def test_las_subclases_solo_definen_patron_y_crear_elemento(self):
        # extraer() es una sola, la de la clase base: ninguna subclase la redefine.
        for clase in (ExtractorEtiquetas, ExtractorMenciones, ExtractorEnlaces):
            with self.subTest(clase=clase.__name__):
                self.assertIs(clase.extraer, Extractor.extraer)

    def test_cada_extractor_fabrica_su_tipo_de_elemento(self):
        casos = [
            (ExtractorEtiquetas(), "#a", Etiqueta),
            (ExtractorMenciones(), "@a", Mencion),
            (ExtractorEnlaces(), "https://a.com", Enlace),
        ]
        for extractor, texto, tipo in casos:
            with self.subTest(tipo=tipo.__name__):
                [elemento] = extractor.extraer(texto)
                self.assertIsInstance(elemento, tipo)
                self.assertIsInstance(elemento, ElementoExtraido)

    def test_sin_nada_que_extraer_devuelve_lista_vacia(self):
        for extractor in (ExtractorEtiquetas(), ExtractorMenciones(), ExtractorEnlaces()):
            with self.subTest(extractor=type(extractor).__name__):
                self.assertEqual(extractor.extraer(""), [])
                self.assertEqual(extractor.extraer("sin nada especial"), [])


class PruebaExtractorEtiquetas(unittest.TestCase):
    def nombres(self, texto):
        return [e.nombre for e in ExtractorEtiquetas().extraer(texto)]

    def test_se_guardan_en_minusculas_y_con_acentos(self):  # D-23
        self.assertEqual(self.nombres("#Pizza #pizza_2 #reunión"), ["pizza", "pizza_2", "reunión"])

    def test_no_se_reconoce_pegada_a_una_letra(self):
        self.assertEqual(self.nombres("C# no"), [])
        self.assertEqual(self.nombres("#a#b"), ["a"])
        self.assertEqual(self.nombres("https://ejemplo.com/a?b=1#c"), [])

    def test_no_se_reconoce_despues_de_una_barra(self):  # D-24
        self.assertEqual(self.nombres("mirá https://x.com/a/#seccion"), [])

    def test_entre_parentesis(self):
        self.assertEqual(self.nombres("(#pizza)"), ["pizza"])


class PruebaExtractorMenciones(unittest.TestCase):
    def nombres(self, texto):
        return [m.nombre_usuario_mencionado for m in ExtractorMenciones().extraer(texto)]

    def test_conserva_el_nombre_tal_como_se_escribio(self):
        self.assertEqual(self.nombres("Hola @Beto y @fantasma!"), ["Beto", "fantasma"])

    def test_la_posicion_apunta_al_arroba(self):
        texto = "Hola @Beto y @fantasma!"
        menciones = ExtractorMenciones().extraer(texto)
        self.assertEqual(
            [m.posicion_en_texto for m in menciones],
            [texto.index("@Beto"), texto.index("@fantasma")],
        )
        for mencion in menciones:
            self.assertEqual(texto[mencion.posicion_en_texto], "@")

    def test_admite_puntos_y_guiones_en_el_medio(self):  # D-24
        self.assertEqual(self.nombres("hola @juan.perez y @ana-lopez!"), ["juan.perez", "ana-lopez"])
        self.assertEqual(self.nombres("@a.b.c"), ["a.b.c"])

    def test_la_puntuacion_del_final_es_de_la_frase(self):
        self.assertEqual(self.nombres("hola @ana."), ["ana"])
        self.assertEqual(self.nombres("hola @ana, chau @beto?"), ["ana", "beto"])
        self.assertEqual(self.nombres("@ana-"), ["ana"])
        self.assertEqual(self.nombres("@ana..x"), ["ana"])

    def test_un_correo_no_es_una_mencion(self):
        self.assertEqual(self.nombres("escribime a ana@empresa.com"), [])

    def test_no_se_reconoce_despues_de_una_barra(self):  # D-24
        self.assertEqual(self.nombres("mirá https://medium.com/@autor/post"), [])

    def test_acentos_y_eñes(self):
        self.assertEqual(self.nombres("@josé y @Ñandú"), ["josé", "Ñandú"])
        self.assertEqual(self.nombres("(@ana)"), ["ana"])


class PruebaExtractorEnlaces(unittest.TestCase):
    def urls(self, texto):
        return [e.url for e in ExtractorEnlaces().extraer(texto)]

    def test_conserva_la_direccion_tal_como_se_escribio(self):
        self.assertEqual(
            self.urls("mirá https://ejemplo.com/a?b=1#c y HTTP://X.COM/Y"),
            ["https://ejemplo.com/a?b=1#c", "HTTP://X.COM/Y"],
        )

    def test_no_incluye_la_puntuacion_del_final(self):  # D-24
        self.assertEqual(self.urls("mirá https://a.com/x."), ["https://a.com/x"])
        self.assertEqual(self.urls("¿viste https://a.com/x? sí, https://b.com/y!"),
                         ["https://a.com/x", "https://b.com/y"])
        self.assertEqual(self.urls("(ver https://a.com/x) fin"), ["https://a.com/x"])

    def test_solo_http_y_https(self):  # D-24
        self.assertEqual(self.urls("ftp://x.com y www.x.com"), [])

    def test_una_direccion_vacia_no_es_un_enlace(self):
        self.assertEqual(self.urls("https://"), [])
        self.assertEqual(self.urls("http://."), [])


class PruebaAnalizadorDeTexto(unittest.TestCase):
    TEXTO = "Hola @beto, mirá #miblog en https://ejemplo.com/x y #Pizza"

    def setUp(self):
        self.analizador = AnalizadorDeTexto(
            [ExtractorEtiquetas(), ExtractorMenciones(), ExtractorEnlaces()]
        )

    def test_junta_lo_de_todos_los_extractores_en_el_orden_de_la_lista(self):
        tipos = [type(e).__name__ for e in self.analizador.analizar(self.TEXTO)]
        self.assertEqual(tipos, ["Etiqueta", "Etiqueta", "Mencion", "Enlace"])

    def test_texto_vacio(self):
        self.assertEqual(self.analizador.analizar(""), [])

    def test_sin_extractores_no_extrae_nada(self):
        self.assertEqual(AnalizadorDeTexto([]).analizar(self.TEXTO), [])

    def test_acepta_un_cuarto_extractor_sin_cambiar_el_analizador(self):
        # La condición 3 de ANALISIS §8.3: sumar un tipo de elemento no obliga a tocar
        # AnalizadorDeTexto. Acá el "cuarto tipo" se inventa dentro de la prueba.
        class Palabra(ElementoExtraido):
            def __init__(self, texto):
                self.texto = texto

            def guardar_en(self, registro, id_mensaje):
                pass

        class ExtractorDePalabraMiblog(Extractor):
            def patron(self):
                return r"\bmiblog\b"

            def crear_elemento(self, coincidencia):
                return Palabra(coincidencia.group(0))

        analizador = AnalizadorDeTexto([ExtractorEtiquetas(), ExtractorDePalabraMiblog()])
        tipos = [type(e).__name__ for e in analizador.analizar(self.TEXTO)]
        self.assertEqual(tipos, ["Etiqueta", "Etiqueta", "Palabra"])


if __name__ == "__main__":
    unittest.main()