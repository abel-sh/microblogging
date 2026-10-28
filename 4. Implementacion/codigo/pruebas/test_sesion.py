"""Pruebas de CU0002 Iniciar Sesión y CU0003 Cerrar Sesión.

Primero el control (ControlAutenticacion con los repositorios de verdad sobre una
base temporal) y después la pantalla, a través de HTTP con el cliente de Flask.
"""

from __future__ import annotations

import hashlib
import unittest
from datetime import datetime, timedelta, timezone

from werkzeug.security import generate_password_hash

from miblog.acceso_datos.conexion import obtener_conexion
from miblog.acceso_datos.repositorio_sesiones import RepositorioSesiones
from miblog.acceso_datos.repositorio_usuarios import RepositorioUsuarios
from miblog.logica.dominio.errores import CredencialesInvalidasError, DatosInvalidosError
from miblog.logica.gestion_usuarios.control_autenticacion import ControlAutenticacion

from pruebas.ayudas import PruebaConApp, PruebaConBase, contar, crear_usuario, en

CLAVE = "clave1234"
# Se calcula una sola vez: cifrar una clave tarda un rato a propósito.
CLAVE_HASH = generate_password_hash(CLAVE)
MENSAJE_GENERICO = "Usuario o clave incorrectos."


class PruebaControlAutenticacion(PruebaConBase):
    def setUp(self):
        super().setUp()
        self.ana = crear_usuario(self.con, "ana", "Ana Pérez", CLAVE_HASH)
        self.control = self.armar_control()

    def armar_control(self, duracion: timedelta = timedelta(minutes=60)) -> ControlAutenticacion:
        return ControlAutenticacion(RepositorioUsuarios(), RepositorioSesiones(), duracion)

    def sesiones(self) -> int:
        return contar(self.con, "sesiones")

    # --- CU0002: curso normal ------------------------------------------------------

    def test_curso_normal_abre_la_sesion_y_el_token_identifica_al_usuario(self):
        token = self.control.autenticar("ana", CLAVE)
        usuario = self.control.obtener_usuario_en_sesion(token)
        self.assertEqual(usuario.id_usuario, self.ana)
        self.assertEqual(self.sesiones(), 1)

    def test_h1_en_la_base_queda_el_hash_del_token_y_no_el_token(self):
        token = self.control.autenticar("ana", CLAVE)
        fila = self.con.execute("SELECT * FROM sesiones").fetchone()
        self.assertEqual(fila["hash_token"], hashlib.sha256(token.encode()).hexdigest())
        self.assertNotIn(token, tuple(fila))
        vence = datetime.fromisoformat(fila["fecha_expiracion"])
        minutos = (vence - datetime.now(timezone.utc)).total_seconds() / 60
        self.assertTrue(59 < minutos <= 60, minutos)  # la sesión dura 60 minutos

    def test_el_nombre_de_usuario_se_recorta_y_no_distingue_mayusculas(self):
        token = self.control.autenticar("  ANA ", CLAVE)
        self.assertEqual(self.control.obtener_usuario_en_sesion(token).id_usuario, self.ana)

    # --- ca 2.1 y ca 2.2 --------------------------------------------------------------

    def test_ca_2_1_usuario_inexistente_clave_incorrecta_y_cuenta_inactiva_dan_el_mismo_error(self):
        crear_usuario(self.con, "inactivo", "Inactivo", CLAVE_HASH, activo=0)
        mensajes = set()
        for nombre, clave in [("nadie", CLAVE), ("ana", "otra-clave"), ("inactivo", CLAVE)]:
            with self.subTest(nombre=nombre):
                with self.assertRaises(CredencialesInvalidasError) as contexto:
                    self.control.autenticar(nombre, clave)
                mensajes.add(contexto.exception.mensaje)
        # rnf 2.3: el mensaje no revela qué falló, así que no se puede descubrir qué usuarios existen.
        self.assertEqual(mensajes, {MENSAJE_GENERICO})
        self.assertEqual(self.sesiones(), 0)

    def test_ca_2_2_los_campos_vacios_se_informan_uno_por_uno(self):
        casos = [
            (("", CLAVE), {"nombre_usuario"}),
            (("ana", ""), {"clave"}),
            (("   ", ""), {"nombre_usuario", "clave"}),
        ]
        for argumentos, esperado in casos:
            with self.subTest(argumentos=argumentos):
                with self.assertRaises(DatosInvalidosError) as contexto:
                    self.control.autenticar(*argumentos)
                self.assertEqual(set(contexto.exception.errores_por_campo), esperado)
        self.assertEqual(self.sesiones(), 0)

    # --- Vigencia de la sesión ----------------------------------------------------------

    def test_una_sesion_vencida_no_vale_y_su_fila_se_borra_al_validarla(self):
        vencida = self.armar_control(timedelta(minutes=-1))
        token = vencida.autenticar("ana", CLAVE)
        self.assertEqual(self.sesiones(), 1)
        self.assertIsNone(self.control.obtener_usuario_en_sesion(token))
        self.assertEqual(self.sesiones(), 0)

    def test_iniciar_sesion_limpia_las_sesiones_vencidas_de_todos_los_usuarios(self):
        beto = crear_usuario(self.con, "beto")
        self.con.execute(
            "INSERT INTO sesiones (hash_token, id_usuario, fecha_expiracion) VALUES (?, ?, ?)",
            ("abandonada", beto, en(-5).isoformat()),
        )
        self.control.autenticar("ana", CLAVE)
        hashes = [f[0] for f in self.con.execute("SELECT hash_token FROM sesiones")]
        self.assertNotIn("abandonada", hashes)
        self.assertEqual(len(hashes), 1)

    def test_una_cuenta_desactivada_despues_de_abrir_la_sesion_deja_de_valer(self):
        token = self.control.autenticar("ana", CLAVE)
        self.con.execute("UPDATE usuarios SET activo = 0 WHERE id_usuario = ?", (self.ana,))
        self.assertIsNone(self.control.obtener_usuario_en_sesion(token))

    def test_sin_token_o_con_un_token_inventado_no_hay_usuario(self):
        for token in (None, "", "token-inventado"):
            with self.subTest(token=token):
                self.assertIsNone(self.control.obtener_usuario_en_sesion(token))

    # --- CU0003 -------------------------------------------------------------------------

    def test_rnf_3_1_cerrar_sesion_invalida_el_token_en_el_servidor_y_solo_ese(self):
        crear_usuario(self.con, "beto", "Beto", CLAVE_HASH)
        token_ana = self.control.autenticar("ana", CLAVE)
        token_beto = self.control.autenticar("beto", CLAVE)
        self.control.cerrar_sesion(token_ana)
        self.assertIsNone(self.control.obtener_usuario_en_sesion(token_ana))
        self.assertIsNotNone(self.control.obtener_usuario_en_sesion(token_beto))
        self.assertEqual(self.sesiones(), 1)

    def test_ca_3_1_cerrar_sin_sesion_o_con_una_ya_cerrada_no_falla(self):
        token = self.control.autenticar("ana", CLAVE)
        for token_a_cerrar in (None, "", "token-inventado", token, token):
            with self.subTest(token=token_a_cerrar):
                self.control.cerrar_sesion(token_a_cerrar)  # no lanza nada
        self.assertEqual(self.sesiones(), 0)


class PruebaWebSesion(PruebaConApp):
    def setUp(self):
        super().setUp()
        with self.app.app_context():
            self.ana = crear_usuario(obtener_conexion(), "ana", "Ana Pérez", CLAVE_HASH)

    def iniciar(self, cliente, nombre="ana", clave=CLAVE):
        return cliente.post("/sesion/iniciar", data={"nombre_usuario": nombre, "clave": clave})

    def sesiones(self) -> int:
        with self.app.app_context():
            return contar(obtener_conexion(), "sesiones")

    def test_curso_normal_lleva_al_tablon_y_la_cookie_es_httponly_y_samesite_lax(self):
        respuesta = self.iniciar(self.app.test_client())
        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(respuesta.headers["Location"].endswith("/tablon"))
        cookie = " ".join(respuesta.headers.getlist("Set-Cookie"))
        self.assertIn("HttpOnly", cookie)
        self.assertIn("SameSite=Lax", cookie)

    def test_rnf_2_1_la_pantalla_pide_la_clave_enmascarada_y_ofrece_registrarse(self):
        html = self.app.test_client().get("/").get_data(as_text=True)
        self.assertIn('type="password"', html)
        self.assertIn('href="/registro"', html)

    def test_ca_2_1_el_aviso_es_generico_conserva_el_usuario_y_no_la_clave(self):
        respuesta = self.iniciar(self.app.test_client(), nombre="ana", clave="clave-equivocada")
        html = respuesta.get_data(as_text=True)
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(MENSAJE_GENERICO, html)
        self.assertIn('value="ana"', html)
        self.assertNotIn("clave-equivocada", html)
        self.assertEqual(self.sesiones(), 0)

    def test_una_cuenta_inactiva_recibe_el_mismo_aviso_que_una_clave_incorrecta(self):
        with self.app.app_context():
            obtener_conexion().execute("UPDATE usuarios SET activo = 0")
        html = self.iniciar(self.app.test_client()).get_data(as_text=True)
        self.assertIn(MENSAJE_GENERICO, html)

    def test_ca_2_2_los_campos_vacios_dicen_cual_falta(self):
        html = self.iniciar(self.app.test_client(), nombre="", clave="").get_data(as_text=True)
        self.assertIn("Ingresá tu nombre de usuario.", html)
        self.assertIn("Ingresá tu clave.", html)

    def test_cerrar_sesion_pide_confirmacion_y_solo_el_post_la_cierra(self):
        cliente = self.app.test_client()
        self.iniciar(cliente)
        pantalla = cliente.get("/sesion/cerrar")
        self.assertIn("¿Cerrar sesión?", pantalla.get_data(as_text=True))
        self.assertEqual(cliente.get("/tablon").status_code, 200)  # abrir la confirmación no cierra

        respuesta = cliente.post("/sesion/cerrar")
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(respuesta.headers["Location"], "/")
        self.assertEqual(cliente.get("/tablon").headers["Location"], "/")
        self.assertEqual(self.sesiones(), 0)

    def test_rnf_3_1_la_cookie_vieja_no_sirve_despues_de_cerrar_sesion(self):
        cliente = self.app.test_client()
        self.iniciar(cliente)
        cookie_vieja = cliente.get_cookie("session").value
        cliente.post("/sesion/cerrar")

        otro = self.app.test_client()
        otro.set_cookie("session", cookie_vieja)  # alguien que se quedó con la cookie
        respuesta = otro.get("/tablon")
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(respuesta.headers["Location"], "/")

    def test_ca_3_1_cerrar_sin_sesion_vuelve_al_inicio_sin_mostrar_error(self):
        cliente = self.app.test_client()
        respuesta = cliente.post("/sesion/cerrar")
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(respuesta.headers["Location"], "/")
        self.assertNotIn("aviso--error", cliente.get("/").get_data(as_text=True))

    def test_una_sesion_vencida_manda_al_inicio_con_un_aviso(self):
        cliente = self.app.test_client()
        self.iniciar(cliente)
        with self.app.app_context():
            obtener_conexion().execute("UPDATE sesiones SET fecha_expiracion = ?", (en(-1).isoformat(),))
        respuesta = cliente.get("/tablon")
        self.assertEqual(respuesta.headers["Location"], "/")
        self.assertIn("Tu sesión expiró. Volvé a iniciar sesión.", cliente.get("/").get_data(as_text=True))
        self.assertEqual(self.sesiones(), 0)  # y la fila vencida se limpió


if __name__ == "__main__":
    unittest.main()