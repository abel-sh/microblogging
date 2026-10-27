"""Pruebas de punta a punta de CU0005, CU0006 y CU0007, a través de HTTP.

Se usa el cliente de prueba de Flask: hace pedidos reales a la aplicación (con
cookies, redirecciones y plantillas), pero sin abrir un puerto ni un navegador.
Cubre las cuatro capas juntas.

Los personajes: ana sigue a beto; carla sigue a ana pero no a beto; dani no sigue a nadie.
"""

from __future__ import annotations

import re
import unittest
from html import unescape

from werkzeug.security import generate_password_hash

from miblog.acceso_datos.conexion import obtener_conexion
from miblog.logica.gestion_mensajes.operaciones_mensaje import OperacionSobreMensaje

from pruebas.ayudas import PruebaConApp, contar, crear_mensaje, crear_usuario, en, republicar, seguir

LIMITE = OperacionSobreMensaje.LIMITE
CLAVE = "clave1234"
RUTAS_NUEVAS = [
    ("post", "/mensajes/1/republicar"),
    ("get", "/mensajes/1/editar"),
    ("post", "/mensajes/1/editar"),
    ("get", "/mensajes/1/borrar"),
    ("post", "/mensajes/1/borrar"),
]


def texto_del_campo(html: str) -> str:
    """Lo que hay escrito en el <textarea> de la página."""
    return unescape(re.search(r"<textarea[^>]*>(.*?)</textarea>", html, re.S).group(1))


class PruebaWebEdicionRepublicacion(PruebaConApp):
    def setUp(self):
        super().setUp()
        with self.app.app_context():
            con = obtener_conexion()
            clave_hash = generate_password_hash(CLAVE)
            self.ana = crear_usuario(con, "ana", "Ana Pérez", clave_hash)
            self.beto = crear_usuario(con, "beto", "Beto Pérez", clave_hash)
            self.carla = crear_usuario(con, "carla", "Carla Gómez", clave_hash)
            self.dani = crear_usuario(con, "dani", "Dani Ruiz", clave_hash)
            seguir(con, self.ana, self.beto)
            seguir(con, self.carla, self.ana)
            self.de_ana = crear_mensaje(con, self.ana, "mensaje de ana #uno", en(-30))
            self.de_beto = crear_mensaje(con, self.beto, "mensaje de beto", en(-20))

    # --- Ayudas ---------------------------------------------------------------

    def entrar(self, nombre_usuario):
        """Un cliente con la sesión de `nombre_usuario` ya iniciada."""
        cliente = self.app.test_client()
        respuesta = cliente.post(
            "/sesion/iniciar", data={"nombre_usuario": nombre_usuario, "clave": CLAVE}
        )
        self.assertEqual(respuesta.status_code, 302)
        return cliente

    def tablon(self, cliente):
        return cliente.get("/tablon").get_data(as_text=True)

    def cuenta(self, tabla):
        with self.app.app_context():
            return contar(obtener_conexion(), tabla)

    def fila_del_mensaje(self, id_mensaje):
        with self.app.app_context():
            fila = obtener_conexion().execute(
                "SELECT texto, editado FROM mensajes WHERE id_mensaje = ?", (id_mensaje,)
            ).fetchone()
            return None if fila is None else (fila["texto"], fila["editado"])

    def republicar_a_mano(self, id_usuario, id_mensaje):
        with self.app.app_context():
            republicar(obtener_conexion(), id_usuario, id_mensaje, en(-10))

    def seguir_a_mano(self, id_seguidor, id_seguido):
        with self.app.app_context():
            seguir(obtener_conexion(), id_seguidor, id_seguido)

    @staticmethod
    def edicion_y_borrado(id_mensaje):
        return (f'href="/mensajes/{id_mensaje}/editar"', f'href="/mensajes/{id_mensaje}/borrar"')

    @staticmethod
    def boton_republicar(id_mensaje):
        return f'action="/mensajes/{id_mensaje}/republicar"'

    # --- Acceso ---------------------------------------------------------------

    def test_sin_sesion_las_cinco_rutas_nuevas_redirigen_al_inicio_sin_hacer_nada(self):
        anonimo = self.app.test_client()
        for metodo, ruta in RUTAS_NUEVAS:
            with self.subTest(ruta=f"{metodo.upper()} {ruta}"):
                respuesta = getattr(anonimo, metodo)(ruta, data={"texto": "intruso"})
                self.assertEqual(respuesta.status_code, 302)
                self.assertEqual(respuesta.headers["Location"], "/")
        self.assertEqual(self.fila_del_mensaje(1), ("mensaje de ana #uno", 0))
        self.assertEqual(self.cuenta("mensajes"), 2)
        self.assertEqual(self.cuenta("republicaciones"), 0)

    def test_el_texto_de_una_edicion_sin_sesion_no_se_guarda_como_borrador_del_tablon(self):
        # Las rutas de edición no usan conservar_borrador (Seguridad):
        # si no, el texto de una edición aparecería en el campo de publicar.
        cliente = self.app.test_client()
        cliente.post(f"/mensajes/{self.de_ana}/editar", data={"texto": "texto editado a medias"})
        cliente.post("/sesion/iniciar", data={"nombre_usuario": "ana", "clave": CLAVE})
        self.assertEqual(texto_del_campo(self.tablon(cliente)), "")

    # --- Los botones del tablón -----------------------------------------------

    def test_en_lo_propio_hay_editar_y_borrar_y_no_republicar(self):
        html = self.tablon(self.entrar("ana"))
        for enlace in self.edicion_y_borrado(self.de_ana):
            self.assertIn(enlace, html)
        self.assertNotIn(self.boton_republicar(self.de_ana), html)

    def test_en_lo_ajeno_hay_republicar_y_no_editar_ni_borrar(self):
        html = self.tablon(self.entrar("ana"))  # ana ve el mensaje de beto
        self.assertIn(self.boton_republicar(self.de_beto), html)
        for enlace in self.edicion_y_borrado(self.de_beto):
            self.assertNotIn(enlace, html)

    def test_h5_el_boton_republicar_aparece_aunque_no_se_siga_al_autor_original(self):
        # carla sigue a ana, ana republica lo de beto: carla lo ve en su tablón, con el
        # botón, aunque no siga a beto. El servidor decide (ca 7.1).
        self.republicar_a_mano(self.ana, self.de_beto)
        html = self.tablon(self.entrar("carla"))
        self.assertIn("Ana Pérez republicó", html)
        self.assertIn(self.boton_republicar(self.de_beto), html)

    def test_en_la_republicacion_ajena_de_un_mensaje_mio_estan_editar_y_borrar(self):
        # El botón se decide por el AUTOR ORIGINAL, no por quién republicó: beto republica
        # lo de ana y ana (que sigue a beto) lo ve en su tablón, con las acciones de su mensaje.
        self.seguir_a_mano(self.beto, self.ana)
        self.republicar_a_mano(self.beto, self.de_ana)
        html = self.tablon(self.entrar("ana"))
        self.assertIn("Beto Pérez republicó", html)
        for enlace in self.edicion_y_borrado(self.de_ana):
            self.assertIn(enlace, html)

    # --- CU0005: Editar ---------------------------------------------------------

    def test_el_dialogo_de_edicion_trae_el_texto_actual_el_limite_y_cancelar(self):
        html = self.entrar("ana").get(f"/mensajes/{self.de_ana}/editar").get_data(as_text=True)
        self.assertEqual(texto_del_campo(html), "mensaje de ana #uno")
        self.assertIn(f'action="/mensajes/{self.de_ana}/editar"', html)
        self.assertIn(f'data-limite="{LIMITE}"', html)
        self.assertIn("contador.js", html)
        self.assertNotIn("maxlength", html)
        self.assertIn('href="/tablon">Cancelar</a>', html)  # ca 5.4: es un enlace
        self.assertIn("cuerpo-dialogo", html)  # página propia con aspecto de diálogo

    def test_editar_guarda_redirige_y_el_tablon_muestra_el_texto_nuevo_con_la_marca(self):
        ana = self.entrar("ana")
        respuesta = ana.post(f"/mensajes/{self.de_ana}/editar", data={"texto": "texto corregido"})
        self.assertEqual(respuesta.status_code, 302)  # Post/Redirect/Get
        self.assertTrue(respuesta.headers["Location"].endswith("/tablon"))

        html = self.tablon(ana)
        self.assertIn("texto corregido", html)
        self.assertNotIn("mensaje de ana #uno", html)
        # rnf 5.2: marca de editado Y fecha de la última modificación.
        self.assertRegex(html, r"\(editado el \d\d/\d\d/\d{4} \d\d:\d\d\)")
        self.assertEqual(self.cuenta("mensajes"), 2)  # no se creó uno nuevo

    def test_un_mensaje_sin_editar_no_lleva_la_marca(self):
        self.assertNotIn("(editado", self.tablon(self.entrar("ana")))

    def test_ca_5_3_texto_vacio_avisa_vuelve_al_dialogo_y_no_toca_el_mensaje(self):
        respuesta = self.entrar("ana").post(f"/mensajes/{self.de_ana}/editar", data={"texto": "   "})
        html = respuesta.get_data(as_text=True)
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("El mensaje no puede estar vacío.", html)  # el diálogo dibuja el aviso
        self.assertIn(f'action="/mensajes/{self.de_ana}/editar"', html)
        self.assertEqual(self.fila_del_mensaje(self.de_ana), ("mensaje de ana #uno", 0))

    def test_ca_5_3_texto_excedido_avisa_cuanto_sobra_y_devuelve_el_texto_completo(self):
        largo = "a" * (LIMITE + 5)
        html = self.entrar("ana").post(
            f"/mensajes/{self.de_ana}/editar", data={"texto": largo}
        ).get_data(as_text=True)
        self.assertIn("El mensaje se pasa por 5 caracteres.", html)
        self.assertIn(f"El máximo es de {LIMITE} caracteres.", html)
        self.assertEqual(texto_del_campo(html), largo)  # sin recortar
        self.assertIn(">-5</span>", html)
        self.assertEqual(self.fila_del_mensaje(self.de_ana), ("mensaje de ana #uno", 0))

    def test_ca_5_2_quien_no_es_el_autor_no_puede_abrir_el_dialogo(self):
        beto = self.entrar("beto")
        respuesta = beto.get(f"/mensajes/{self.de_ana}/editar")
        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(respuesta.headers["Location"].endswith("/tablon"))
        self.assertIn(
            "Solo el autor puede editar o borrar este mensaje.",
            beto.get("/tablon").get_data(as_text=True),
        )

    def test_ca_5_2_el_pedido_directo_de_otro_usuario_se_rechaza_en_el_servidor(self):
        # Sin pasar por el diálogo ni por el botón: la autoría se verifica de nuevo (rnf 5.1).
        beto = self.entrar("beto")
        respuesta = beto.post(
            f"/mensajes/{self.de_ana}/editar", data={"texto": "texto de beto"}, follow_redirects=True
        )
        self.assertIn("Solo el autor puede editar o borrar este mensaje.", respuesta.get_data(as_text=True))
        self.assertEqual(self.fila_del_mensaje(self.de_ana), ("mensaje de ana #uno", 0))

    def test_ca_5_1_si_el_mensaje_ya_no_existe_vuelve_al_tablon_con_un_aviso(self):
        ana = self.entrar("ana")
        for metodo in (ana.get, ana.post):
            with self.subTest(metodo=metodo.__name__):
                respuesta = metodo("/mensajes/9999/editar", follow_redirects=True)
                self.assertIn("El mensaje ya no está disponible.", respuesta.get_data(as_text=True))

    def test_ca_5_4_cancelar_no_cambia_nada(self):
        ana = self.entrar("ana")
        ana.get(f"/mensajes/{self.de_ana}/editar")  # abre el diálogo
        ana.get("/tablon")  # y "Cancelar" es solo volver al tablón
        self.assertEqual(self.fila_del_mensaje(self.de_ana), ("mensaje de ana #uno", 0))

    def test_el_html_del_texto_a_editar_se_escapa(self):
        with self.app.app_context():
            peligroso = crear_mensaje(
                obtener_conexion(), self.ana, "</textarea><script>alert(1)</script>", en(-1)
            )
        html = self.entrar("ana").get(f"/mensajes/{peligroso}/editar").get_data(as_text=True)
        self.assertNotIn("<script>alert(1)", html)
        self.assertIn("&lt;/textarea&gt;&lt;script&gt;", html)

    def test_editar_un_mensaje_republicado_se_ve_en_la_republicacion_sin_tocar_nada_mas(self):
        # El caso del Decorator, de punta a punta: beto republica lo de ana, ana lo edita,
        # y quien ve la republicación (alguien que sigue a beto) ve el texto nuevo.
        self.seguir_a_mano(self.dani, self.beto)
        self.republicar_a_mano(self.beto, self.de_ana)
        dani = self.entrar("dani")
        antes = self.tablon(dani)
        self.assertIn("Beto Pérez republicó", antes)
        self.assertIn("mensaje de ana #uno", antes)

        self.entrar("ana").post(f"/mensajes/{self.de_ana}/editar", data={"texto": "texto nuevo de ana"})

        despues = self.tablon(dani)
        self.assertIn("Beto Pérez republicó", despues)
        self.assertIn("texto nuevo de ana", despues)
        self.assertNotIn("mensaje de ana #uno", despues)
        self.assertRegex(despues, r"\(editado el \d\d/\d\d/\d{4} \d\d:\d\d\)")
        self.assertEqual(self.cuenta("republicaciones"), 1)

    # --- CU0006: Borrar ---------------------------------------------------------

    def test_el_dialogo_de_borrado_muestra_el_mensaje_advierte_y_ofrece_cancelar(self):
        html = self.entrar("ana").get(f"/mensajes/{self.de_ana}/borrar").get_data(as_text=True)
        self.assertIn("¿Borrar este mensaje?", html)
        self.assertIn("mensaje de ana #uno", html)
        self.assertIn("No se puede deshacer", html)  # rnf 6.2
        self.assertIn("republicado", html)
        self.assertIn(f'action="/mensajes/{self.de_ana}/borrar"', html)
        self.assertIn('href="/tablon">Cancelar</a>', html)  # ca 6.3: es un enlace
        self.assertIn("cuerpo-dialogo", html)
        self.assertEqual(self.fila_del_mensaje(self.de_ana), ("mensaje de ana #uno", 0))  # solo mirar no borra

    def test_borrar_elimina_el_mensaje_y_sus_republicaciones_y_redirige(self):
        self.republicar_a_mano(self.beto, self.de_ana)
        ana = self.entrar("ana")
        respuesta = ana.post(f"/mensajes/{self.de_ana}/borrar")
        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(respuesta.headers["Location"].endswith("/tablon"))

        self.assertIsNone(self.fila_del_mensaje(self.de_ana))
        self.assertEqual(self.cuenta("republicaciones"), 0)
        self.assertNotIn("mensaje de ana", self.tablon(ana))

    def test_borrar_deja_el_mensaje_republicado_afuera_del_tablon_de_los_seguidores_del_republicador(self):
        self.seguir_a_mano(self.dani, self.beto)
        self.republicar_a_mano(self.beto, self.de_ana)
        dani = self.entrar("dani")
        self.assertIn("mensaje de ana", self.tablon(dani))

        self.entrar("ana").post(f"/mensajes/{self.de_ana}/borrar")

        self.assertNotIn("mensaje de ana", self.tablon(dani))

    def test_borrar_no_toca_los_otros_mensajes(self):
        self.entrar("ana").post(f"/mensajes/{self.de_ana}/borrar")
        self.assertEqual(self.fila_del_mensaje(self.de_beto), ("mensaje de beto", 0))

    def test_ca_6_1_si_el_mensaje_ya_no_existe_se_actualiza_la_vista_sin_ningun_aviso(self):
        ana = self.entrar("ana")
        for metodo in (ana.get, ana.post):
            with self.subTest(metodo=metodo.__name__):
                respuesta = metodo("/mensajes/9999/borrar")
                self.assertEqual(respuesta.status_code, 302)
                self.assertTrue(respuesta.headers["Location"].endswith("/tablon"))
                html = ana.get("/tablon").get_data(as_text=True)
                self.assertNotIn("ya no está disponible", html)
                self.assertNotIn("aviso--error", html)

    def test_ca_6_1_borrar_dos_veces_la_segunda_no_da_error(self):
        ana = self.entrar("ana")
        ana.post(f"/mensajes/{self.de_ana}/borrar")
        respuesta = ana.post(f"/mensajes/{self.de_ana}/borrar", follow_redirects=True)
        self.assertEqual(respuesta.status_code, 200)
        self.assertNotIn("aviso--error", respuesta.get_data(as_text=True))

    def test_ca_6_2_quien_no_es_el_autor_no_puede_abrir_el_dialogo(self):
        beto = self.entrar("beto")
        respuesta = beto.get(f"/mensajes/{self.de_ana}/borrar", follow_redirects=True)
        self.assertIn("Solo el autor puede editar o borrar este mensaje.", respuesta.get_data(as_text=True))
        self.assertNotIn("¿Borrar este mensaje?", respuesta.get_data(as_text=True))

    def test_ca_6_2_el_pedido_directo_de_otro_usuario_no_borra_nada(self):
        self.republicar_a_mano(self.beto, self.de_ana)
        beto = self.entrar("beto")
        respuesta = beto.post(f"/mensajes/{self.de_ana}/borrar", follow_redirects=True)
        self.assertIn("Solo el autor puede editar o borrar este mensaje.", respuesta.get_data(as_text=True))
        self.assertEqual(self.fila_del_mensaje(self.de_ana), ("mensaje de ana #uno", 0))
        self.assertEqual(self.cuenta("republicaciones"), 1)

    def test_ca_6_3_cancelar_no_borra_nada(self):
        ana = self.entrar("ana")
        ana.get(f"/mensajes/{self.de_ana}/borrar")
        ana.get("/tablon")
        self.assertEqual(self.fila_del_mensaje(self.de_ana), ("mensaje de ana #uno", 0))

    def test_los_get_nunca_cambian_datos(self):
        # Borrar y editar cambian datos solo por POST: un enlace o una precarga no pueden borrar.
        ana = self.entrar("ana")
        ana.get(f"/mensajes/{self.de_ana}/borrar")
        ana.get(f"/mensajes/{self.de_ana}/editar")
        self.assertEqual(self.fila_del_mensaje(self.de_ana), ("mensaje de ana #uno", 0))
        self.assertEqual(ana.get(f"/mensajes/{self.de_ana}/republicar").status_code, 405)

    # --- CU0007: Republicar -----------------------------------------------------

    def test_republicar_redirige_y_la_republicacion_aparece_arriba_de_todo(self):
        ana = self.entrar("ana")
        respuesta = ana.post(f"/mensajes/{self.de_beto}/republicar")
        self.assertEqual(respuesta.status_code, 302)  # Post/Redirect/Get
        self.assertTrue(respuesta.headers["Location"].endswith("/tablon"))

        html = self.tablon(ana)
        self.assertIn("Ana Pérez republicó", html)
        self.assertIn("tarjeta--republicacion", html)
        self.assertLess(html.index("Ana Pérez republicó"), html.index("mensaje de ana #uno"))
        self.assertEqual(self.cuenta("republicaciones"), 1)
        self.assertEqual(self.cuenta("mensajes"), 2)  # no se copió nada

    def test_la_republicacion_llega_a_los_seguidores_del_que_republico(self):
        self.entrar("ana").post(f"/mensajes/{self.de_beto}/republicar")
        html = self.tablon(self.entrar("carla"))  # carla sigue a ana, no a beto
        self.assertIn("Ana Pérez republicó", html)
        self.assertIn("mensaje de beto", html)

    def test_ca_7_3_republicar_dos_veces_solo_informa(self):
        ana = self.entrar("ana")
        ana.post(f"/mensajes/{self.de_beto}/republicar")
        respuesta = ana.post(f"/mensajes/{self.de_beto}/republicar", follow_redirects=True)
        html = respuesta.get_data(as_text=True)
        self.assertIn("Ya republicaste este mensaje.", html)
        self.assertEqual(self.cuenta("republicaciones"), 1)  # no se deshizo nada

    def test_ca_7_2_republicar_un_mensaje_propio_se_rechaza(self):
        respuesta = self.entrar("ana").post(f"/mensajes/{self.de_ana}/republicar", follow_redirects=True)
        self.assertIn("No podés republicar tus propios mensajes.", respuesta.get_data(as_text=True))
        self.assertEqual(self.cuenta("republicaciones"), 0)

    def test_ca_7_1_republicar_lo_de_alguien_a_quien_no_se_sigue_se_rechaza(self):
        self.republicar_a_mano(self.ana, self.de_beto)  # carla lo ve, con botón
        carla = self.entrar("carla")
        self.assertIn(self.boton_republicar(self.de_beto), self.tablon(carla))
        respuesta = carla.post(f"/mensajes/{self.de_beto}/republicar", follow_redirects=True)
        self.assertIn(
            "Solo podés republicar mensajes de usuarios a los que seguís.",
            respuesta.get_data(as_text=True),
        )
        self.assertEqual(self.cuenta("republicaciones"), 1)  # solo la de ana

    def test_ca_7_4_republicar_un_mensaje_que_ya_no_existe_avisa(self):
        respuesta = self.entrar("ana").post("/mensajes/9999/republicar", follow_redirects=True)
        self.assertIn("El mensaje ya no está disponible.", respuesta.get_data(as_text=True))
        self.assertEqual(self.cuenta("republicaciones"), 0)

    def test_ca_7_4_el_autor_borra_justo_antes_de_que_otro_republique(self):
        ana = self.entrar("ana")
        self.assertIn(self.boton_republicar(self.de_beto), self.tablon(ana))  # ana ve el botón
        self.entrar("beto").post(f"/mensajes/{self.de_beto}/borrar")  # beto borra
        respuesta = ana.post(f"/mensajes/{self.de_beto}/republicar", follow_redirects=True)
        self.assertIn("El mensaje ya no está disponible.", respuesta.get_data(as_text=True))
        self.assertEqual(self.cuenta("republicaciones"), 0)

    def test_republicar_un_mensaje_editado_muestra_la_marca_de_editado(self):
        self.entrar("beto").post(f"/mensajes/{self.de_beto}/editar", data={"texto": "beto corregido"})
        ana = self.entrar("ana")
        ana.post(f"/mensajes/{self.de_beto}/republicar")
        html = self.tablon(ana)
        self.assertIn("Ana Pérez republicó", html)
        self.assertIn("beto corregido", html)
        self.assertRegex(html, r"\(editado el \d\d/\d\d/\d{4} \d\d:\d\d\)")


if __name__ == "__main__":
    unittest.main()