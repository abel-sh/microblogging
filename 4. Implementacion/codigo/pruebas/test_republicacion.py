"""Pruebas de CU0007 Republicar Mensaje en la capa de lógica.

Se prueba ControlRepublicacion con repositorios de verdad sobre una base temporal.
Cubre el curso normal (la republicación guarda quién, cuándo y a qué apunta, sin
copiar texto) y los cuatro cursos alternativos: ca 7.1 (no se sigue al autor),
ca 7.2 (mensaje propio), ca 7.3 (ya republicado) y ca 7.4 (el mensaje ya no existe),
más el orden en que se verifican.
"""

from __future__ import annotations

import unittest
from unittest.mock import patch

from miblog.acceso_datos.repositorio_mensajes import RepositorioMensajes
from miblog.acceso_datos.repositorio_republicaciones import RepositorioRepublicaciones
from miblog.acceso_datos.repositorio_seguimientos import RepositorioSeguimientos
from miblog.acceso_datos.repositorio_usuarios import RepositorioUsuarios
from miblog.logica.dominio.errores import (
    AutorNoSeguidoError,
    ErrorDeNegocio,
    MensajeInexistenteError,
    MensajePropioError,
    RepublicacionExistenteError,
)
from miblog.logica.gestion_mensajes.control_republicacion import ControlRepublicacion
from miblog.logica.gestion_mensajes.control_tablon import ControlTablon

from pruebas.ayudas import PruebaConBase, contar, crear_mensaje, crear_usuario, en, seguir


class PruebaControlRepublicacion(PruebaConBase):
    def setUp(self):
        super().setUp()
        self.id_ana = crear_usuario(self.con, "ana", "Ana Pérez")
        self.id_beto = crear_usuario(self.con, "beto", "Beto Pérez")
        self.id_carla = crear_usuario(self.con, "carla", "Carla Gómez")
        repo_usuarios = RepositorioUsuarios()
        self.ana = repo_usuarios.buscar_activo_por_id(self.id_ana)
        self.beto = repo_usuarios.buscar_activo_por_id(self.id_beto)
        self.carla = repo_usuarios.buscar_activo_por_id(self.id_carla)

        # ana sigue a beto. beto escribió un mensaje. carla no sigue a nadie.
        seguir(self.con, self.id_ana, self.id_beto)
        self.mensaje_de_beto = crear_mensaje(self.con, self.id_beto, "mensaje de beto", en(-30))

        self.repo_mensajes = RepositorioMensajes()
        self.repo_republicaciones = RepositorioRepublicaciones()
        self.control = ControlRepublicacion(
            self.repo_mensajes, RepositorioSeguimientos(), self.repo_republicaciones
        )

    def republicaciones(self):
        return self.con.execute("SELECT * FROM republicaciones").fetchall()

    # --- Curso normal --------------------------------------------------------------

    def test_republica_y_devuelve_el_id_de_la_republicacion(self):
        id_republicacion = self.control.republicar(self.ana, self.mensaje_de_beto)
        fila = self.con.execute(
            "SELECT * FROM republicaciones WHERE id_republicacion = ?", (id_republicacion,)
        ).fetchone()
        self.assertEqual(fila["id_usuario"], self.id_ana)
        self.assertEqual(fila["id_mensaje"], self.mensaje_de_beto)
        self.assertIsNotNone(fila["fecha_republicacion"])

    def test_no_copia_ni_toca_el_mensaje_original(self):
        # la republicación apunta al original. No hay un mensaje nuevo ni se modifica el viejo.
        self.control.republicar(self.ana, self.mensaje_de_beto)
        self.assertEqual(contar(self.con, "mensajes"), 1)
        original = self.repo_mensajes.buscar_por_id(self.mensaje_de_beto)
        self.assertEqual(original.texto, "mensaje de beto")
        self.assertEqual(original.autor.id_usuario, self.id_beto)
        self.assertFalse(original.editado)

    def test_la_republicacion_aparece_en_los_tablones_de_quienes_siguen_al_que_republico(self):
        # carla sigue a ana; ana republica lo de beto (a quien carla NO sigue): carla lo ve.
        seguir(self.con, self.id_carla, self.id_ana)
        self.control.republicar(self.ana, self.mensaje_de_beto)

        tablon_de_carla = ControlTablon(self.repo_mensajes, self.repo_republicaciones).obtener_tablon(
            self.carla
        )
        self.assertEqual(len(tablon_de_carla), 1)
        elemento = tablon_de_carla[0]
        self.assertEqual(elemento.obtener_republicador().nombre_usuario, "ana")
        self.assertEqual(elemento.obtener_autor_original().nombre_usuario, "beto")
        self.assertEqual(elemento.obtener_texto_vigente(), "mensaje de beto")

    def test_dos_usuarios_pueden_republicar_el_mismo_mensaje(self):
        seguir(self.con, self.id_carla, self.id_beto)
        self.control.republicar(self.ana, self.mensaje_de_beto)
        self.control.republicar(self.carla, self.mensaje_de_beto)
        self.assertEqual(contar(self.con, "republicaciones"), 2)

    def test_se_puede_republicar_un_mensaje_que_uno_mismo_no_vio_en_el_tablon(self):
        # No se exige que el mensaje "esté en mi tablón": se exige seguir al autor (H5).
        otro = crear_mensaje(self.con, self.id_beto, "uno viejo", en(-5000))
        self.control.republicar(self.ana, otro)
        self.assertEqual(contar(self.con, "republicaciones"), 1)

    # --- ca 7.4: el mensaje ya no existe --------------------------------------------

    def test_ca_7_4_mensaje_inexistente(self):
        with self.assertRaises(MensajeInexistenteError):
            self.control.republicar(self.ana, 9999)
        self.assertEqual(contar(self.con, "republicaciones"), 0)

    # --- ca 7.2: mensaje propio ------------------------------------------------------

    def test_ca_7_2_no_se_puede_republicar_un_mensaje_propio(self):
        propio = crear_mensaje(self.con, self.id_ana, "mensaje de ana", en(-1))
        with self.assertRaises(MensajePropioError):
            self.control.republicar(self.ana, propio)
        self.assertEqual(contar(self.con, "republicaciones"), 0)

    # --- ca 7.1: no se sigue al autor (H5: el botón aparece igual, decide el servidor) ----

    def test_ca_7_1_no_se_puede_republicar_el_mensaje_de_alguien_a_quien_no_se_sigue(self):
        with self.assertRaises(AutorNoSeguidoError):
            self.control.republicar(self.carla, self.mensaje_de_beto)
        self.assertEqual(contar(self.con, "republicaciones"), 0)

    def test_ca_7_1_caso_de_h5_ver_una_republicacion_ajena_no_alcanza_para_republicar(self):
        # carla sigue a ana, ana republicó lo de beto: carla VE el mensaje de beto en su
        # tablón (con botón Republicar), pero no sigue a beto, así que el servidor lo rechaza.
        seguir(self.con, self.id_carla, self.id_ana)
        self.control.republicar(self.ana, self.mensaje_de_beto)
        with self.assertRaises(AutorNoSeguidoError):
            self.control.republicar(self.carla, self.mensaje_de_beto)
        self.assertEqual(contar(self.con, "republicaciones"), 1)

    def test_seguir_al_autor_en_un_solo_sentido_alcanza_pero_hay_que_ser_el_seguidor(self):
        # beto no sigue a ana: no puede republicar los mensajes de ana aunque ana siga a beto.
        de_ana = crear_mensaje(self.con, self.id_ana, "mensaje de ana", en(-2))
        with self.assertRaises(AutorNoSeguidoError):
            self.control.republicar(self.beto, de_ana)

    # --- ca 7.3: ya republicado ------------------------------------------------------

    def test_ca_7_3_no_se_puede_republicar_dos_veces_el_mismo_mensaje(self):
        self.control.republicar(self.ana, self.mensaje_de_beto)
        antes = self.republicaciones()
        with self.assertRaises(RepublicacionExistenteError):
            self.control.republicar(self.ana, self.mensaje_de_beto)
        # solo informa. No se deshace nada.
        self.assertEqual(self.republicaciones(), antes)

    # --- El orden de las verificaciones (DISEÑO §6.7) ---------------------------------

    def test_primero_que_exista_antes_que_cualquier_otra_cosa(self):
        with self.assertRaises(MensajeInexistenteError):
            self.control.republicar(self.carla, 9999)  # carla ni siquiera sigue a nadie

    def test_propio_se_verifica_antes_que_seguir_al_autor(self):
        # Uno no puede seguirse a sí mismo (ca 11.2): sin este orden, un mensaje propio
        # caería en ca 7.1 con un aviso que no corresponde.
        propio = crear_mensaje(self.con, self.id_carla, "de carla", en(-1))
        with self.assertRaises(MensajePropioError):
            self.control.republicar(self.carla, propio)

    def test_seguir_al_autor_se_verifica_antes_que_el_duplicado(self):
        # ana ya republicó, pero después deja de seguir a beto: el aviso es el de
        # "no seguís al autor", no el de "ya republicaste".
        self.control.republicar(self.ana, self.mensaje_de_beto)
        self.con.execute(
            "DELETE FROM seguimientos WHERE id_seguidor = ? AND id_seguido = ?",
            (self.id_ana, self.id_beto),
        )
        with self.assertRaises(AutorNoSeguidoError):
            self.control.republicar(self.ana, self.mensaje_de_beto)

    # --- Todos los cursos alternativos son errores de negocio -------------------------

    def test_los_errores_son_de_negocio_para_que_la_vista_los_muestre(self):
        propio = crear_mensaje(self.con, self.id_ana, "de ana", en(-1))
        casos = [(self.ana, 9999), (self.ana, propio), (self.carla, self.mensaje_de_beto)]
        for usuario, id_mensaje in casos:
            with self.subTest(id_mensaje=id_mensaje):
                with self.assertRaises(ErrorDeNegocio):
                    self.control.republicar(usuario, id_mensaje)

    # --- Todo o nada -----------------------------------------------------------------

    def test_si_falla_al_guardar_no_queda_nada_y_se_puede_reintentar(self):
        with patch.object(
            self.repo_republicaciones, "crear", side_effect=RuntimeError("falla simulada")
        ):
            with self.assertRaises(RuntimeError):
                self.control.republicar(self.ana, self.mensaje_de_beto)
        self.assertEqual(contar(self.con, "republicaciones"), 0)
        self.assertFalse(self.con.in_transaction)
        self.control.republicar(self.ana, self.mensaje_de_beto)
        self.assertEqual(contar(self.con, "republicaciones"), 1)


if __name__ == "__main__":
    unittest.main()