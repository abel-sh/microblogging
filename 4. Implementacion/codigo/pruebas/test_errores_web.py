"""Pruebas del manejo de errores y del registro de eventos (RNF24, RNF16).

Se prueba a través de HTTP, con el cliente de Flask. Para provocar un error
inesperado de verdad se le suma a la aplicación una ruta de prueba que siempre falla;
esa ruta no existe en la aplicación real.
"""

from __future__ import annotations

import logging
import os
import re
import unittest

from flask.logging import default_handler

from miblog import crear_app

from pruebas.ayudas import PruebaConApp

DETALLE_SECRETO = "detalle-interno-que-nadie-debe-ver"


def falla():
    raise ValueError(DETALLE_SECRETO)


class PruebaErroresWeb(PruebaConApp):
    def setUp(self):
        super().setUp()
        # Antes de la primera petición Flask deja sumar rutas.
        self.app.add_url_rule("/falla", "falla", falla, methods=["GET", "POST"])
        self.cliente = self.app.test_client()
        # Flask también escribe los errores en la consola. Acá se provocan a propósito, y
        # se sacan de la consola para que no parezca que la suite falló.
        self.app.logger.removeHandler(default_handler)

    def registro(self) -> str:
        """Lo que hay escrito en el archivo de registro ('' si todavía no existe)."""
        ruta = self.app.config["ARCHIVO_DE_REGISTRO"]
        if not os.path.exists(ruta):
            return ""
        with open(ruta, encoding="utf-8") as archivo:
            return archivo.read()

    # --- Errores que el usuario puede provocar: página propia, sin anotar nada ---

    def test_una_pagina_que_no_existe_da_404_con_la_pagina_de_error(self):
        respuesta = self.cliente.get("/no-existe")
        html = respuesta.get_data(as_text=True)
        self.assertEqual(respuesta.status_code, 404)
        self.assertIn("Esa página no existe", html)
        self.assertIn('href="/">Volver al inicio', html)
        self.assertIn("cuerpo-dialogo", html)  # sin barra: el error puede darse sin sesión
        self.assertEqual(self.registro(), "")  # no es una falla del sistema: no se anota

    def test_un_pedido_con_metodo_equivocado_sigue_siendo_405_y_no_un_500(self):
        # /mensajes solo acepta POST. El manejador general no tiene que tragarse el código.
        respuesta = self.cliente.get("/mensajes")
        self.assertEqual(respuesta.status_code, 405)
        self.assertIn("No se pudo atender el pedido", respuesta.get_data(as_text=True))
        self.assertEqual(self.registro(), "")

    def test_un_pedido_demasiado_grande_da_413_con_la_pagina_de_error(self):
        # MAX_CONTENT_LENGTH es el tamaño de la foto más 1 MB, así que 4 MB lo supera. Es lo
        # que pasa al subir una foto enorme. Se manda como formulario simple y no como
        # archivo porque, con un archivo de ese tamaño, el cliente de pruebas arma un
        # temporal que deja abierto cuando el servidor corta el pedido.
        cuerpo = b"nombre_usuario=" + b"a" * (4 * 1024 * 1024)
        respuesta = self.cliente.post(
            "/registro", data=cuerpo, content_type="application/x-www-form-urlencoded"
        )
        self.assertEqual(respuesta.status_code, 413)
        self.assertIn("Lo que enviaste pesa demasiado", respuesta.get_data(as_text=True))
        self.assertEqual(self.registro(), "")

    def test_un_error_de_negocio_no_pasa_por_la_pagina_de_error(self):
        # Credenciales incorrectas es un curso alternativo (ca 2.1): lo muestra la
        # vista con flash() y no queda nada en el registro.
        respuesta = self.cliente.post(
            "/sesion/iniciar", data={"nombre_usuario": "nadie", "clave": "x"}
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("Usuario o clave incorrectos.", respuesta.get_data(as_text=True))
        self.assertEqual(self.registro(), "")

    # --- Errores inesperados (RNF24) -----------------------------------------------

    def test_un_error_inesperado_muestra_una_pagina_generica_sin_detalles(self):
        respuesta = self.cliente.get("/falla")
        html = respuesta.get_data(as_text=True)
        self.assertEqual(respuesta.status_code, 500)
        self.assertIn("Algo salió mal", html)
        self.assertNotIn(DETALLE_SECRETO, html)
        self.assertNotIn("Traceback", html)

    def test_rnf_24_el_error_inesperado_queda_en_el_registro_con_fecha_y_hora(self):
        self.cliente.get("/falla")
        texto = self.registro()
        self.assertRegex(
            texto,
            r"(?m)^\d\d/\d\d/\d{4} \d\d:\d\d:\d\d ERROR Error inesperado en GET /falla$",
        )
        # El recorrido completo del error, para poder encontrar la causa.
        self.assertIn("Traceback", texto)
        self.assertIn(f"ValueError: {DETALLE_SECRETO}", texto)

    def test_el_registro_no_guarda_lo_que_se_escribio_en_el_formulario(self):
        # rnf 1.2 y rnf 2.2: una clave no se registra en ningún log. Del pedido solo
        # se anotan el método y la ruta.
        self.cliente.post("/falla", data={"clave": "clave-que-no-debe-aparecer"})
        texto = self.registro()
        self.assertIn("Error inesperado en POST /falla", texto)
        self.assertNotIn("clave-que-no-debe-aparecer", texto)

    def test_crear_la_aplicacion_dos_veces_no_repite_las_lineas_del_registro(self):
        # Las pruebas arman muchas aplicaciones en el mismo proceso. Si cada una sumara
        # su propio manejador, un solo error se escribiría varias veces.
        segunda = crear_app()
        segunda.config["TESTING"] = True
        segunda.add_url_rule("/falla", "falla", falla)
        segunda.test_client().get("/falla")
        self.assertEqual(self.registro().count("Error inesperado en GET /falla"), 1)

    def test_el_archivo_de_registro_es_el_que_dice_la_configuracion(self):
        # ARCHIVO_DE_REGISTRO se lee del entorno, igual que BASE_DE_DATOS (RNF28). Sin la
        # variable, el archivo es instance/miblog.log.
        ruta = self.app.config["ARCHIVO_DE_REGISTRO"]
        self.assertTrue(ruta.endswith("prueba.log"))
        manejadores = [m for m in self.app.logger.handlers if isinstance(m, logging.FileHandler)]
        self.assertEqual([m.baseFilename for m in manejadores], [ruta])


if __name__ == "__main__":
    unittest.main()