"""Pruebas de CU0014 Buscar Usuarios y CU0011 Seguir Usuario.

Tres grupos: el control de búsqueda, el control de seguimiento (los dos con los
repositorios de verdad sobre una base temporal) y la pantalla, a través de HTTP.
"""

from __future__ import annotations

import sqlite3
import unittest
from dataclasses import fields
from datetime import datetime, timezone

from werkzeug.security import generate_password_hash

from miblog.acceso_datos.conexion import obtener_conexion
from miblog.acceso_datos.repositorio_seguimientos import RepositorioSeguimientos
from miblog.acceso_datos.repositorio_usuarios import RepositorioUsuarios
from miblog.logica.dominio.errores import (
    AutoSeguimientoError,
    CriterioVacioError,
    SeguimientoExistenteError,
    UsuarioInexistenteError,
)
from miblog.logica.gestion_relaciones.control_busqueda_usuarios import (
    ControlBusquedaUsuarios,
    ResultadoBusqueda,
)
from miblog.logica.gestion_relaciones.control_seguimiento import ControlSeguimiento

from pruebas.ayudas import PruebaConApp, PruebaConBase, contar, crear_usuario, seguir

CLAVE = "clave1234"
CLAVE_HASH = generate_password_hash(CLAVE)  # una sola vez: cifrar tarda a propósito


def nombres(resultados: list[ResultadoBusqueda]) -> list[str]:
    return [r.nombre_usuario for r in resultados]


class PruebaControlBusqueda(PruebaConBase):
    def setUp(self):
        super().setUp()
        self.control = ControlBusquedaUsuarios(RepositorioUsuarios(), RepositorioSeguimientos())
        self.repo_usuarios = RepositorioUsuarios()
        self.ana = self.repo_usuarios.buscar_activo_por_id(crear_usuario(self.con, "ana", "Ana Pérez"))

    def buscar(self, criterio: str) -> list[ResultadoBusqueda]:
        return self.control.buscar(criterio, self.ana)

    def test_curso_normal_busca_por_nombre_de_usuario_y_por_nombre_completo(self):
        crear_usuario(self.con, "beto", "Roberto Díaz")
        crear_usuario(self.con, "caro", "Carolina Beto")
        # "beto" está en el nombre de usuario de uno y en el nombre completo de otro.
        self.assertEqual(sorted(nombres(self.buscar("beto"))), ["beto", "caro"])
        # y vale con un pedazo del medio, no solo con el principio
        self.assertEqual(nombres(self.buscar("bert")), ["beto"])

    def test_rnf_14_1_no_importan_las_mayusculas_ni_los_acentos(self):
        crear_usuario(self.con, "maria", "María Gómez")
        crear_usuario(self.con, "jose", "JOSÉ PEÑA")
        for criterio in ("maria", "MARÍA", "gomez", "GÓMEZ"):
            with self.subTest(criterio=criterio):
                self.assertEqual(nombres(self.buscar(criterio)), ["maria"])
        for criterio in ("pena", "peña", "José"):
            with self.subTest(criterio=criterio):
                self.assertEqual(nombres(self.buscar(criterio)), ["jose"])

    def test_ca_14_1_un_criterio_vacio_o_de_solo_espacios_se_rechaza(self):
        for criterio in ("", "   ", "\t \n"):
            with self.subTest(criterio=repr(criterio)):
                with self.assertRaises(CriterioVacioError):
                    self.buscar(criterio)

    def test_el_criterio_se_recorta_antes_de_buscar(self):
        self.assertEqual(nombres(self.buscar("  ana  ")), ["ana"])

    def test_ca_14_2_sin_coincidencias_es_una_lista_vacia_y_no_un_error(self):
        self.assertEqual(self.buscar("nadie-se-llama-asi"), [])

    def test_los_comodines_de_like_se_buscan_como_texto_comun(self):
        crear_usuario(self.con, "ana_1", "Ana Uno")
        crear_usuario(self.con, "anaX1", "Ana Equis")
        crear_usuario(self.con, "tasa100", "Tasa Cien")
        # "_" no es "cualquier carácter": "a_1" solo está en ana_1.
        self.assertEqual(nombres(self.buscar("a_1")), ["ana_1"])
        # "%" no es "todo": ningún nombre lo contiene.
        self.assertEqual(self.buscar("%"), [])
        self.assertEqual(self.buscar("100%"), [])
        self.assertEqual(self.buscar("\\"), [])

    def test_solo_aparecen_cuentas_activas(self):
        crear_usuario(self.con, "luis_activo", "Luis Activo")
        crear_usuario(self.con, "luis_baja", "Luis Baja", activo=0)
        self.assertEqual(nombres(self.buscar("luis")), ["luis_activo"])

    def test_rnf_14_2_el_resultado_no_lleva_correo_ni_descripcion(self):
        # La pantalla no puede mostrar lo que nunca le llega.
        self.assertEqual(
            [f.name for f in fields(ResultadoBusqueda)],
            ["id_usuario", "nombre_usuario", "nombre_completo", "url_foto", "lo_sigue"],
        )
        resultado = self.buscar("ana")[0]
        self.assertFalse(hasattr(resultado, "email"))
        self.assertFalse(hasattr(resultado, "descripcion"))

    def test_lo_sigue_marca_solo_a_los_que_sigue_quien_busca(self):
        beto = crear_usuario(self.con, "beto_x", "Beto X")
        caro = crear_usuario(self.con, "caro_x", "Caro X")
        crear_usuario(self.con, "dani_x", "Dani X")
        seguir(self.con, self.ana.id_usuario, beto)
        seguir(self.con, caro, self.ana.id_usuario)  # caro sigue a ana, no al revés
        marcas = {r.nombre_usuario: r.lo_sigue for r in self.buscar("_x")}
        self.assertEqual(marcas, {"beto_x": True, "caro_x": False, "dani_x": False})

    def test_la_propia_cuenta_aparece_en_los_resultados_sin_marcarse_como_seguida(self):
        # Es la pantalla la que no le ofrece el botón (ver la prueba web de más abajo).
        resultados = self.buscar("ana")
        self.assertEqual(nombres(resultados), ["ana"])
        self.assertFalse(resultados[0].lo_sigue)

    def test_d_19_el_orden_es_por_nombre_completo_sin_acentos_y_despues_por_id(self):
        zoe = crear_usuario(self.con, "emp_zoe", "Zoe Sosa")
        alvaro = crear_usuario(self.con, "emp_alvaro", "Álvaro Paz")
        beto = crear_usuario(self.con, "emp_beto", "beto Ruiz")  # minúscula a propósito
        gomez_1 = crear_usuario(self.con, "emp_gomez_1", "Ana Gómez")
        gomez_2 = crear_usuario(self.con, "emp_gomez_2", "Ana Gómez")
        ids = [r.id_usuario for r in self.buscar("emp_")]
        # Álvaro antes que Ana (a-l < a-n) aunque la Á suelta se ordene mal; las dos Ana
        # Gómez, iguales, por orden de alta; y beto (minúscula) antes que Zoe.
        self.assertEqual(ids, [alvaro, gomez_1, gomez_2, beto, zoe])


class PruebaControlSeguimiento(PruebaConBase):
    def setUp(self):
        super().setUp()
        self.repo_usuarios = RepositorioUsuarios()
        self.repo_seguimientos = RepositorioSeguimientos()
        self.control = ControlSeguimiento(self.repo_usuarios, self.repo_seguimientos)
        self.ana = self.usuario(crear_usuario(self.con, "ana", "Ana Pérez"))
        self.beto = crear_usuario(self.con, "beto", "Beto Díaz")

    def usuario(self, id_usuario: int):
        return self.repo_usuarios.buscar_activo_por_id(id_usuario)

    def seguimientos(self) -> int:
        return contar(self.con, "seguimientos")

    def test_curso_normal_registra_el_seguimiento_con_su_fecha_de_inicio(self):
        antes = datetime.now(timezone.utc)
        self.control.seguir(self.ana, self.beto)
        fila = self.con.execute("SELECT * FROM seguimientos").fetchone()
        self.assertEqual((fila["id_seguidor"], fila["id_seguido"]), (self.ana.id_usuario, self.beto))
        # rnf 11.2: la fecha queda guardada, con zona horaria, y es de ahora
        inicio = datetime.fromisoformat(fila["fecha_inicio"])
        self.assertIsNotNone(inicio.tzinfo)
        self.assertGreaterEqual(inicio, antes)
        self.assertLessEqual(inicio, datetime.now(timezone.utc))

    def test_ca_11_1_una_cuenta_inexistente_o_inactiva_no_se_puede_seguir(self):
        inactivo = crear_usuario(self.con, "inactivo", "Inactivo", activo=0)
        for id_seguido in (inactivo, 99999):
            with self.subTest(id_seguido=id_seguido):
                with self.assertRaises(UsuarioInexistenteError):
                    self.control.seguir(self.ana, id_seguido)
        self.assertEqual(self.seguimientos(), 0)

    def test_ca_11_2_nadie_se_sigue_a_si_mismo(self):
        with self.assertRaises(AutoSeguimientoError):
            self.control.seguir(self.ana, self.ana.id_usuario)
        self.assertEqual(self.seguimientos(), 0)

    def test_ca_11_3_seguir_dos_veces_al_mismo_usuario_se_rechaza_y_queda_uno_solo(self):
        self.control.seguir(self.ana, self.beto)
        with self.assertRaises(SeguimientoExistenteError):
            self.control.seguir(self.ana, self.beto)
        self.assertEqual(self.seguimientos(), 1)

    def test_el_seguimiento_es_unilateral(self):
        self.control.seguir(self.ana, self.beto)
        self.assertTrue(self.repo_seguimientos.existe(self.ana.id_usuario, self.beto))
        self.assertFalse(self.repo_seguimientos.existe(self.beto, self.ana.id_usuario))
        # y Beto puede seguir a Ana después: no es "ya existe" porque el par es otro
        self.control.seguir(self.usuario(self.beto), self.ana.id_usuario)
        self.assertEqual(self.seguimientos(), 2)

    def test_la_tabla_es_la_segunda_barrera_contra_el_duplicado_y_el_auto_seguimiento(self):
        # Si el control fallara, la base se niega igual: PRIMARY KEY del par y CHECK.
        seguir(self.con, self.ana.id_usuario, self.beto)
        with self.assertRaises(sqlite3.IntegrityError):
            seguir(self.con, self.ana.id_usuario, self.beto)
        with self.assertRaises(sqlite3.IntegrityError):
            seguir(self.con, self.ana.id_usuario, self.ana.id_usuario)
        self.assertEqual(self.seguimientos(), 1)


class PruebaWebRelaciones(PruebaConApp):
    def setUp(self):
        super().setUp()
        with self.app.app_context():
            con = obtener_conexion()
            self.ana = crear_usuario(con, "ana", "Ana Pérez", CLAVE_HASH)
            self.beto = crear_usuario(con, "beto", "Beto Pérez")
            self.caro = crear_usuario(con, "caro", "Carolina Pérez")
            crear_usuario(con, "baja", "Baja Pérez", activo=0)
            seguir(con, self.ana, self.beto)  # ana ya sigue a beto

    def entrar(self, nombre_usuario="ana"):
        cliente = self.app.test_client()
        respuesta = cliente.post(
            "/sesion/iniciar", data={"nombre_usuario": nombre_usuario, "clave": CLAVE}
        )
        self.assertEqual(respuesta.status_code, 302)
        return cliente

    def seguimientos(self) -> int:
        with self.app.app_context():
            return contar(obtener_conexion(), "seguimientos")

    def buscar(self, cliente, criterio):
        return cliente.get("/usuarios/buscar", query_string={"criterio": criterio})

    # --- Acceso ------------------------------------------------------------------------

    def test_sin_sesion_ni_buscar_ni_seguir_y_se_vuelve_al_inicio(self):
        cliente = self.app.test_client()
        for respuesta in (
            cliente.get("/usuarios/buscar?criterio=ana"),
            cliente.post(f"/usuarios/{self.caro}/seguir"),
        ):
            self.assertEqual(respuesta.status_code, 302)
            self.assertEqual(respuesta.headers["Location"], "/")
        self.assertEqual(self.seguimientos(), 1)  # el POST sin sesión no creó nada

    # --- CU0014 ------------------------------------------------------------------------

    def test_la_primera_visita_muestra_solo_el_formulario(self):
        html = self.entrar().get("/usuarios/buscar").get_data(as_text=True)
        self.assertIn('name="criterio"', html)
        self.assertNotIn("No se encontraron usuarios.", html)
        self.assertNotIn("aviso--error", html)  # abrir la pantalla no es buscar nada (ca 14.1)

    def test_ca_14_1_buscar_con_el_campo_vacio_avisa_y_no_lista_nada(self):
        cliente = self.entrar()
        # "" es lo que manda el navegador al apretar Buscar con el campo sin tocar.
        for criterio in ("", "   "):
            with self.subTest(criterio=repr(criterio)):
                html = self.buscar(cliente, criterio).get_data(as_text=True)
                self.assertIn("Ingresá al menos un carácter para buscar.", html)
                self.assertNotIn("tarjeta--resultado", html)

    def test_ca_14_2_sin_coincidencias_dice_que_no_hay_usuarios(self):
        html = self.buscar(self.entrar(), "zzzz").get_data(as_text=True)
        self.assertIn("No se encontraron usuarios.", html)
        self.assertNotIn("tarjeta--resultado", html)

    def test_los_resultados_muestran_nombre_y_usuario_pero_no_el_correo(self):
        html = self.buscar(self.entrar(), "pérez").get_data(as_text=True)  # ignora el acento
        for esperado in ("Beto Pérez", "@beto", "Carolina Pérez", "@caro"):
            self.assertIn(esperado, html)
        self.assertNotIn("@ejemplo.com", html)  # rnf 14.2: el correo no se muestra
        self.assertNotIn("Baja Pérez", html)  # las cuentas inactivas no se listan

    def test_cada_resultado_ofrece_la_accion_que_corresponde(self):
        html = self.buscar(self.entrar(), "pérez").get_data(as_text=True)
        # a Beto ya lo sigue: solo la marca, sin acción
        self.assertIn("Siguiendo", html)
        self.assertNotIn(f'action="/usuarios/{self.beto}/seguir"', html)
        # a Carolina todavía no: botón para seguirla
        self.assertIn(f'action="/usuarios/{self.caro}/seguir"', html)

    def test_en_la_propia_cuenta_no_se_ofrece_ninguna_accion(self):
        html = self.buscar(self.entrar(), "ana").get_data(as_text=True)
        self.assertIn("@ana", html)
        self.assertNotIn(f'action="/usuarios/{self.ana}/seguir"', html)
        self.assertNotIn("Siguiendo", html)

    def test_lo_que_se_escribe_en_la_busqueda_se_muestra_escapado(self):
        html = self.buscar(self.entrar(), "<script>alert(1)</script>").get_data(as_text=True)
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertIn("&lt;script&gt;", html)

    # --- CU0011 ------------------------------------------------------------------------

    def test_seguir_vuelve_a_la_busqueda_y_el_resultado_pasa_a_siguiendo(self):
        cliente = self.entrar()
        respuesta = cliente.post(f"/usuarios/{self.caro}/seguir", data={"criterio": "pérez"})
        self.assertEqual(respuesta.status_code, 302)  # Post/Redirect/Get: recargar no repite el POST
        self.assertIn("/usuarios/buscar?criterio=", respuesta.headers["Location"])
        self.assertEqual(self.seguimientos(), 2)

        html = cliente.get(respuesta.headers["Location"]).get_data(as_text=True)
        self.assertNotIn(f'action="/usuarios/{self.caro}/seguir"', html)
        self.assertEqual(html.count("Siguiendo"), 2)  # Beto y ahora Carolina

    def test_ca_11_3_seguir_otra_vez_no_duplica_ni_muestra_un_error(self):
        cliente = self.entrar()
        respuesta = cliente.post(f"/usuarios/{self.beto}/seguir", data={"criterio": "pérez"})
        self.assertEqual(respuesta.status_code, 302)
        html = cliente.get(respuesta.headers["Location"]).get_data(as_text=True)
        self.assertNotIn("aviso--error", html)
        self.assertEqual(self.seguimientos(), 1)

    def test_ca_11_1_seguir_a_alguien_que_no_existe_avisa_y_no_crea_nada(self):
        cliente = self.entrar()
        respuesta = cliente.post("/usuarios/99999/seguir", data={"criterio": "pérez"})
        self.assertEqual(respuesta.status_code, 302)
        html = cliente.get(respuesta.headers["Location"]).get_data(as_text=True)
        self.assertIn("El usuario no existe o no está disponible.", html)
        self.assertEqual(self.seguimientos(), 1)

    def test_ca_11_2_seguirse_a_uno_mismo_avisa_aunque_se_mande_el_post_a_mano(self):
        # El botón no se ofrece, pero el servidor vuelve a verificar.
        cliente = self.entrar()
        respuesta = cliente.post(f"/usuarios/{self.ana}/seguir", data={"criterio": "ana"})
        html = cliente.get(respuesta.headers["Location"]).get_data(as_text=True)
        self.assertIn("Tus mensajes ya aparecen en tu tablón.", html)
        self.assertEqual(self.seguimientos(), 1)

    def test_seguir_sin_criterio_vuelve_al_formulario_limpio(self):
        # Un POST mandado a mano, sin el campo oculto: no se dispara una búsqueda vacía.
        respuesta = self.entrar().post(f"/usuarios/{self.caro}/seguir")
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(respuesta.headers["Location"], "/usuarios/buscar")
        self.assertEqual(self.seguimientos(), 2)

    def test_un_id_que_no_es_numerico_da_404_y_seguir_por_get_da_405(self):
        cliente = self.entrar()
        self.assertEqual(cliente.post("/usuarios/abc/seguir").status_code, 404)
        self.assertEqual(cliente.get(f"/usuarios/{self.caro}/seguir").status_code, 405)
        self.assertEqual(self.seguimientos(), 1)


if __name__ == "__main__":
    unittest.main()