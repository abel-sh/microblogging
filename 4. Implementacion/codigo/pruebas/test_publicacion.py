"""Pruebas de CU0004 Publicar Mensaje en la capa de lógica.

Se prueba Publicacion (la operación del Template Method) y ControlPublicacion, con
repositorios de verdad sobre una base temporal. Cubre ca 4.1, ca 4.2, rnf 4.2 y la
transacción única de rnf 4.4.
"""

from __future__ import annotations

import unittest
from unittest.mock import patch

from miblog.acceso_datos.repositorio_elementos import RepositorioElementos
from miblog.acceso_datos.repositorio_mensajes import RepositorioMensajes
from miblog.acceso_datos.repositorio_republicaciones import RepositorioRepublicaciones
from miblog.acceso_datos.repositorio_usuarios import RepositorioUsuarios
from miblog.logica.dominio.enumeraciones import OrigenPublicacion
from miblog.logica.dominio.errores import ErrorDeNegocio, TextoExcedidoError, TextoVacioError
from miblog.logica.gestion_mensajes.analizador import AnalizadorDeTexto
from miblog.logica.gestion_mensajes.control_publicacion import ControlPublicacion
from miblog.logica.gestion_mensajes.extractores import (
    ExtractorEnlaces,
    ExtractorEtiquetas,
    ExtractorMenciones,
)
from miblog.logica.gestion_mensajes.operaciones_mensaje import (
    Edicion,
    OperacionSobreMensaje,
    Publicacion,
)

from pruebas.ayudas import PruebaConBase, contar, crear_usuario

LIMITE = OperacionSobreMensaje.LIMITE
TABLAS_DE_UN_MENSAJE = ["mensajes", "etiquetas", "mensaje_etiqueta", "menciones", "enlaces"]


class PruebaPublicacion(PruebaConBase):
    def setUp(self):
        super().setUp()
        crear_usuario(self.con, "ana")
        crear_usuario(self.con, "beto")
        self.ana = RepositorioUsuarios().buscar_activo_por_nombre_usuario("ana")
        self.repo_elementos = RepositorioElementos()
        self.publicacion = Publicacion(
            AnalizadorDeTexto([ExtractorEtiquetas(), ExtractorMenciones(), ExtractorEnlaces()]),
            RepositorioMensajes(),
            self.repo_elementos,
        )

    def contadores(self):
        return {tabla: contar(self.con, tabla) for tabla in TABLAS_DE_UN_MENSAJE}

    # --- La forma del Template Method ---------------------------------------------

    def test_la_operacion_base_es_abstracta(self):
        with self.assertRaises(TypeError):
            OperacionSobreMensaje(None, None, None)

    def test_ninguna_subclase_redefine_ejecutar(self):
        # Template Method: el orden de los pasos se escribe una sola vez, en la clase base.
        self.assertIs(Publicacion.ejecutar, OperacionSobreMensaje.ejecutar)
        self.assertIs(Edicion.ejecutar, OperacionSobreMensaje.ejecutar)

    # --- Curso normal --------------------------------------------------------------

    def test_publica_y_devuelve_el_mensaje_con_sus_datos(self):
        mensaje = self.publicacion.ejecutar(self.ana, "  Hola mundo  ")
        self.assertEqual(mensaje.id_mensaje, 1)
        self.assertEqual(mensaje.texto, "Hola mundo")  # rnf 4.5: sin espacios de más
        self.assertEqual(mensaje.autor.id_usuario, self.ana.id_usuario)
        self.assertEqual(mensaje.origen, OrigenPublicacion.WEB)
        self.assertFalse(mensaje.editado)

    def test_guarda_etiquetas_menciones_y_enlaces_en_la_misma_operacion(self):
        self.publicacion.ejecutar(
            self.ana, "Hola @Beto y @fantasma #Pizza #pizza https://ejemplo.com/x"
        )
        self.assertEqual(contar(self.con, "etiquetas"), 1)  # #Pizza y #pizza son una sola
        self.assertEqual(contar(self.con, "mensaje_etiqueta"), 1)
        self.assertEqual(contar(self.con, "menciones"), 1)  # @fantasma no existe: se descarta
        url = self.con.execute("SELECT url FROM enlaces").fetchone()[0]
        self.assertEqual(url, "https://ejemplo.com/x")

    # --- ca 4.1 y ca 4.2: se valida en el servidor (rnf 4.2) ----------------------

    def test_ca_4_1_texto_vacio_o_solo_espacios_no_se_guarda(self):
        for vacio in ["", "   ", "\n\n  \r\n"]:
            with self.subTest(texto=repr(vacio)), self.assertRaises(TextoVacioError):
                self.publicacion.ejecutar(self.ana, vacio)
        self.assertEqual(contar(self.con, "mensajes"), 0)

    def test_ca_4_2_texto_excedido_informa_cuanto_sobra_y_no_se_guarda(self):
        with self.assertRaises(TextoExcedidoError) as contexto:
            self.publicacion.ejecutar(self.ana, "x" * (LIMITE + 7))
        self.assertEqual(contexto.exception.excedente, 7)
        self.assertEqual(contar(self.con, "mensajes"), 0)

    def test_justo_en_el_limite_se_acepta_y_uno_mas_no(self):
        self.publicacion.ejecutar(self.ana, "y" * LIMITE)
        with self.assertRaises(TextoExcedidoError):
            self.publicacion.ejecutar(self.ana, "y" * (LIMITE + 1))
        self.assertEqual(contar(self.con, "mensajes"), 1)

    def test_un_enter_cuenta_como_un_caracter(self):
        # El navegador manda cada Enter como "\r\n"; se cuenta como uno solo, igual
        # que en el contador de la pantalla.
        texto = "a\r\nb\r\n" + "c" * (LIMITE - 4)  # 1 + 1 + 1 + 1 + (LIMITE - 4) = LIMITE
        mensaje = self.publicacion.ejecutar(self.ana, texto)
        self.assertEqual(len(mensaje.texto), LIMITE)
        self.assertNotIn("\r", mensaje.texto)

    def test_un_emoji_cuenta_como_un_caracter(self):
        # Igual que Array.from(...) en contador.js: se cuentan caracteres, no bytes.
        self.publicacion.ejecutar(self.ana, "😀" * LIMITE)
        with self.assertRaises(TextoExcedidoError):
            self.publicacion.ejecutar(self.ana, "😀" * (LIMITE + 1))

    # --- rnf 4.4: todo o nada -----------------------------------------------------

    def test_si_falla_un_paso_a_mitad_no_queda_nada_del_mensaje(self):
        antes = self.contadores()
        with patch.object(
            self.repo_elementos, "registrar_enlace", side_effect=RuntimeError("falla simulada")
        ):
            with self.assertRaises(RuntimeError):
                self.publicacion.ejecutar(self.ana, "nuevo #etiquetanueva @beto https://roto.com")
        self.assertEqual(self.contadores(), antes)
        self.assertFalse(self.con.in_transaction)

    def test_despues_de_un_fallo_se_puede_seguir_publicando(self):
        with patch.object(
            self.repo_elementos, "registrar_enlace", side_effect=RuntimeError("falla simulada")
        ):
            with self.assertRaises(RuntimeError):
                self.publicacion.ejecutar(self.ana, "https://roto.com")
        self.publicacion.ejecutar(self.ana, "después del fallo")
        self.assertEqual(contar(self.con, "mensajes"), 1)


class PruebaControlPublicacion(PruebaConBase):
    def setUp(self):
        super().setUp()
        crear_usuario(self.con, "ana")
        self.ana = RepositorioUsuarios().buscar_activo_por_nombre_usuario("ana")
        analizador = AnalizadorDeTexto(
            [ExtractorEtiquetas(), ExtractorMenciones(), ExtractorEnlaces()]
        )
        repo_mensajes, repo_elementos = RepositorioMensajes(), RepositorioElementos()
        self.control = ControlPublicacion(
            Publicacion(analizador, repo_mensajes, repo_elementos),
            Edicion(analizador, repo_mensajes, repo_elementos),
            repo_mensajes,
            RepositorioRepublicaciones(),
            repo_elementos,
        )

    def test_publicar_delega_en_la_operacion(self):
        mensaje = self.control.publicar(self.ana, "primer mensaje #miblog")
        self.assertEqual(mensaje.id_mensaje, 1)
        self.assertEqual(mensaje.autor.id_usuario, self.ana.id_usuario)

    def test_los_errores_son_de_negocio_para_que_la_vista_los_muestre(self):
        for texto, error in [("   ", TextoVacioError), ("x" * 500, TextoExcedidoError)]:
            with self.subTest(error=error.__name__):
                with self.assertRaises(error) as contexto:
                    self.control.publicar(self.ana, texto)
                self.assertIsInstance(contexto.exception, ErrorDeNegocio)
        self.assertEqual(contar(self.con, "mensajes"), 0)


if __name__ == "__main__":
    unittest.main()