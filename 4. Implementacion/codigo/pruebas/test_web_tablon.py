"""Pruebas de punta a punta de CU0004 y CU0009, a través de HTTP.

Se usa el cliente de prueba de Flask: hace pedidos reales a la aplicación (con
cookies, redirecciones y plantillas), pero sin abrir un puerto ni un navegador.
Cubre las cuatro capas juntas.
"""

from __future__ import annotations

import os
import re
import unittest
from html import unescape

from werkzeug.security import generate_password_hash

import miblog
from miblog.acceso_datos.conexion import obtener_conexion
from miblog.logica.gestion_mensajes.operaciones_mensaje import OperacionSobreMensaje

from pruebas.ayudas import PruebaConApp, contar, crear_usuario, en, republicar, seguir

LIMITE = OperacionSobreMensaje.LIMITE
CLAVE = "clave1234"


def texto_del_campo(html: str) -> str:
    """Lo que hay escrito en el <textarea> de la página."""
    return unescape(re.search(r"<textarea[^>]*>(.*?)</textarea>", html, re.S).group(1))


class PruebaWebTablon(PruebaConApp):
    def setUp(self):
        super().setUp()
        with self.app.app_context():
            con = obtener_conexion()
            clave_hash = generate_password_hash(CLAVE)
            self.ana = crear_usuario(con, "ana", "Ana Pérez", clave_hash)
            self.beto = crear_usuario(con, "beto", "Beto Pérez", clave_hash)
            seguir(con, self.ana, self.beto)  # ana sigue a beto

    def entrar(self, nombre_usuario):
        """Un cliente con la sesión de `nombre_usuario` ya iniciada."""
        cliente = self.app.test_client()
        respuesta = cliente.post(
            "/sesion/iniciar", data={"nombre_usuario": nombre_usuario, "clave": CLAVE}
        )
        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(respuesta.headers["Location"].endswith("/tablon"))
        return cliente

    def tablon(self, cliente):
        return cliente.get("/tablon").get_data(as_text=True)

    def filas(self, tabla):
        with self.app.app_context():
            return contar(obtener_conexion(), tabla)

    # --- Acceso ---------------------------------------------------------------

    def test_sin_sesion_el_tablon_y_publicar_redirigen_al_inicio(self):
        anonimo = self.app.test_client()
        for respuesta in (anonimo.get("/tablon"), anonimo.post("/mensajes", data={"texto": "hola"})):
            self.assertEqual(respuesta.status_code, 302)
            self.assertEqual(respuesta.headers["Location"], "/")
        self.assertEqual(self.filas("mensajes"), 0)

    # --- CU0009 ---------------------------------------------------------------

    def test_ca_9_1_tablon_vacio_explica_que_hacer(self):
        html = self.tablon(self.entrar("ana"))
        self.assertIn("Tu tablón está vacío", html)
        self.assertIn('href="/usuarios/buscar"', html)

    def test_el_formulario_trae_el_limite_del_servidor_y_no_corta_el_texto(self):
        html = self.tablon(self.entrar("ana"))
        self.assertIn(f'data-limite="{LIMITE}"', html)
        self.assertIn(f">{LIMITE}</span>", html)  # contador inicial
        self.assertIn("contador.js", html)
        self.assertNotIn("maxlength", html)  # si el navegador cortara, no habría ca 4.2

    def test_lo_de_los_seguidos_aparece_y_lo_de_los_demas_no(self):
        ana, beto = self.entrar("ana"), self.entrar("beto")
        ana.post("/mensajes", data={"texto": "mensaje de ana"})
        beto.post("/mensajes", data={"texto": "mensaje de beto"})
        self.assertIn("mensaje de beto", self.tablon(ana))
        self.assertNotIn("mensaje de ana", self.tablon(beto))  # beto no sigue a ana

    def test_una_republicacion_dice_quien_republico_y_ordena_por_su_fecha(self):
        ana, beto = self.entrar("ana"), self.entrar("beto")
        ana.post("/mensajes", data={"texto": "original de ana"})
        beto.post("/mensajes", data={"texto": "mensaje de beto"})
        with self.app.app_context():  # republicar es del bloque 4.5: se carga a mano
            con = obtener_conexion()
            id_original = con.execute("SELECT id_mensaje FROM mensajes WHERE id_autor = ?",
                                      (self.ana,)).fetchone()[0]
            republicar(con, self.beto, id_original, en(60))
        html = self.tablon(ana)
        self.assertIn("Beto Pérez republicó", html)
        self.assertIn("tarjeta--republicacion", html)
        self.assertLess(html.index("Beto Pérez republicó"), html.index("mensaje de beto"))

    # --- CU0004 ---------------------------------------------------------------

    def test_publicar_redirige_y_el_mensaje_aparece_con_autor_y_fecha(self):
        ana = self.entrar("ana")
        respuesta = ana.post("/mensajes", data={"texto": "Hola @beto soy #Nuevo en https://ejemplo.com/x"})
        self.assertEqual(respuesta.status_code, 302)  # Post/Redirect/Get
        self.assertTrue(respuesta.headers["Location"].endswith("/tablon"))

        html = self.tablon(ana)
        self.assertIn("Hola @beto soy #Nuevo en https://ejemplo.com/x", html)
        self.assertIn("Ana Pérez", html)
        self.assertIn("@ana", html)
        self.assertRegex(html, r"\d\d/\d\d/\d{4} \d\d:\d\d")
        self.assertNotIn("Tu tablón está vacío", html)
        self.assertNotIn("(editado)", html)

        with self.app.app_context():
            con = obtener_conexion()
            self.assertEqual([f[0] for f in con.execute("SELECT nombre FROM etiquetas")], ["nuevo"])
            self.assertEqual(contar(con, "menciones"), 1)
            self.assertEqual(contar(con, "enlaces"), 1)

    def test_ca_4_1_mensaje_vacio_avisa_y_no_guarda(self):
        html = self.entrar("ana").post("/mensajes", data={"texto": "   "}).get_data(as_text=True)
        self.assertIn("El mensaje no puede estar vacío.", html)
        self.assertEqual(self.filas("mensajes"), 0)

    def test_ca_4_2_mensaje_excedido_avisa_cuanto_sobra_y_devuelve_el_texto_completo(self):
        largo = "a" * (LIMITE + 7)
        html = self.entrar("ana").post("/mensajes", data={"texto": largo}).get_data(as_text=True)
        self.assertIn("El mensaje se pasa por 7 caracteres.", html)
        self.assertIn(f"El máximo es de {LIMITE} caracteres.", html)
        self.assertEqual(texto_del_campo(html), largo)  # sin recortar
        self.assertIn(">-7</span>", html)  # el contador arranca en negativo
        self.assertEqual(self.filas("mensajes"), 0)

    def test_un_enter_escrito_en_el_navegador_cuenta_como_uno(self):
        texto = "a\r\nb\r\n" + "c" * (LIMITE - 4)
        respuesta = self.entrar("ana").post("/mensajes", data={"texto": texto})
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(self.filas("mensajes"), 1)

    def test_el_html_del_mensaje_se_escapa(self):
        ana = self.entrar("ana")
        ana.post("/mensajes", data={"texto": "<script>alert(1)</script>"})
        html = self.tablon(ana)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)
        self.assertNotIn("<script>alert(1)", html)

    def test_los_saltos_de_linea_llegan_a_la_pagina(self):
        # Que se vean como saltos lo hace el CSS (ver PruebaEstaticos).
        ana = self.entrar("ana")
        ana.post("/mensajes", data={"texto": "primera\r\nsegunda"})
        self.assertIn("primera\nsegunda", self.tablon(ana))

    def test_ca_4_3_el_borrador_sobrevive_a_una_sesion_vencida_y_aparece_una_sola_vez(self):
        cliente = self.app.test_client()
        respuesta = cliente.post("/mensajes", data={"texto": "texto a medio escribir"})
        self.assertEqual(respuesta.headers["Location"], "/")  # la guardia lo manda a iniciar sesión

        cliente.post("/sesion/iniciar", data={"nombre_usuario": "ana", "clave": CLAVE})
        self.assertEqual(texto_del_campo(self.tablon(cliente)), "texto a medio escribir")
        self.assertEqual(texto_del_campo(self.tablon(cliente)), "")  # una sola vez


class PruebaEstaticos(PruebaConApp):
    """Los archivos de presentacion/estaticos/ y su relación con el resto."""

    def leer(self, nombre):
        carpeta = os.path.join(os.path.dirname(miblog.__file__), "presentacion", "estaticos")
        with open(os.path.join(carpeta, nombre), encoding="utf-8") as archivo:
            return archivo.read()

    def test_contador_js_se_sirve_y_no_repite_el_numero_del_limite(self):
        # La URL se toma de la página, porque Flask sirve los estáticos en /estaticos/.
        with self.app.app_context():
            con = obtener_conexion()
            crear_usuario(con, "ana", clave_hash=generate_password_hash(CLAVE))
        cliente = self.app.test_client()
        cliente.post("/sesion/iniciar", data={"nombre_usuario": "ana", "clave": CLAVE})
        pagina = cliente.get("/tablon").get_data(as_text=True)
        url = re.search(r'<script src="([^"]*contador\.js)"', pagina).group(1)

        # El "with" cierra el archivo que Flask abre para servir el estático.
        with self.app.test_client().get(url) as respuesta:
            self.assertEqual(respuesta.status_code, 200)
            contenido = respuesta.data
        self.assertNotIn(str(LIMITE).encode(), contenido)
        # Cuenta caracteres, no unidades UTF-16 (un emoji es 1). Se busca la llamada
        # completa porque "Array.from" también aparece en un comentario del archivo.
        self.assertIn(b"Array.from(campo.value)", contenido)

    def test_la_clase_del_contador_excedido_existe_en_el_css_y_la_usa_el_js(self):
        self.assertRegex(self.leer("estilos.css"), r"\.contador--excedido\s*\{")
        # Se busca el uso real (el nombre también aparece en comentarios).
        self.assertIn('classList.toggle("contador--excedido"', self.leer("contador.js"))

    def test_el_texto_de_las_tarjetas_respeta_los_saltos_de_linea(self):
        regla = re.search(r"\.tarjeta__texto\s*\{([^}]*)\}", self.leer("estilos.css")).group(1)
        self.assertRegex(regla, r"white-space:\s*pre-line")


if __name__ == "__main__":
    unittest.main()