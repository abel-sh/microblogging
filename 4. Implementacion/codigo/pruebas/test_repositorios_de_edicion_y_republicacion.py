"""Pruebas de los métodos de repositorio que suman CU0005, CU0006 y CU0007.

RepositorioMensajes: buscar_por_id, actualizar_texto, eliminar.
RepositorioRepublicaciones: existe, crear, eliminar_por_mensaje.

Se prueban con una base temporal de verdad. Los datos de partida se cargan con SQL
directo (ver ayudas.py) para que un error de estos repositorios no rompa también la
preparación de la prueba.
"""

from __future__ import annotations

import sqlite3
import unittest
from datetime import datetime

from miblog.acceso_datos.repositorio_mensajes import RepositorioMensajes
from miblog.acceso_datos.repositorio_republicaciones import RepositorioRepublicaciones

from pruebas.ayudas import (
    AHORA,
    PruebaConBase,
    contar,
    crear_mensaje,
    crear_usuario,
    en,
    republicar,
)


class PruebaRepositorioMensajesEdicion(PruebaConBase):
    def setUp(self):
        super().setUp()
        self.ana = crear_usuario(self.con, "ana", "Ana Pérez")
        self.beto = crear_usuario(self.con, "beto", "Beto Pérez")
        self.id_mensaje = crear_mensaje(self.con, self.ana, "texto original", en(-10))
        self.repo = RepositorioMensajes()

    # --- buscar_por_id -------------------------------------------------------------

    def test_buscar_por_id_trae_el_mensaje_completo_con_su_autor(self):
        mensaje = self.repo.buscar_por_id(self.id_mensaje)
        self.assertEqual(mensaje.id_mensaje, self.id_mensaje)
        self.assertEqual(mensaje.texto, "texto original")
        self.assertFalse(mensaje.editado)
        self.assertIsNone(mensaje.fecha_ultima_edicion)
        self.assertEqual(mensaje.autor.id_usuario, self.ana)
        self.assertEqual(mensaje.autor.nombre_usuario, "ana")
        self.assertEqual(mensaje.autor.nombre_completo, "Ana Pérez")
        self.assertIsInstance(mensaje.fecha_publicacion, datetime)

    def test_buscar_por_id_de_un_mensaje_que_no_existe_devuelve_none(self):
        self.assertIsNone(self.repo.buscar_por_id(9999))

    def test_buscar_por_id_no_depende_de_quien_pregunta(self):
        # Quién puede hacer qué con el mensaje lo decide la lógica, no esta consulta.
        otro = crear_mensaje(self.con, self.beto, "de beto", en(-5))
        self.assertEqual(self.repo.buscar_por_id(otro).autor.id_usuario, self.beto)

    # --- actualizar_texto ----------------------------------------------------------

    def test_actualizar_texto_guarda_texto_marca_y_fecha_juntos(self):
        mensaje = self.repo.buscar_por_id(self.id_mensaje)
        mensaje.editar("texto nuevo", en(0))
        self.assertEqual(self.repo.actualizar_texto(mensaje), 1)

        fila = self.con.execute(
            "SELECT texto, editado, fecha_ultima_edicion FROM mensajes WHERE id_mensaje = ?",
            (self.id_mensaje,),
        ).fetchone()
        self.assertEqual(fila["texto"], "texto nuevo")
        self.assertEqual(fila["editado"], 1)
        self.assertEqual(fila["fecha_ultima_edicion"], en(0).isoformat())

        releido = self.repo.buscar_por_id(self.id_mensaje)
        self.assertTrue(releido.editado)
        self.assertEqual(releido.fecha_ultima_edicion, en(0))

    def test_actualizar_texto_no_cambia_autor_ni_fecha_de_publicacion(self):
        antes = self.repo.buscar_por_id(self.id_mensaje)
        antes.editar("otro texto", en(3))
        self.repo.actualizar_texto(antes)
        despues = self.repo.buscar_por_id(self.id_mensaje)
        self.assertEqual(despues.autor.id_usuario, self.ana)
        self.assertEqual(despues.fecha_publicacion, en(-10))
        self.assertEqual(despues.origen, antes.origen)

    def test_actualizar_texto_de_un_mensaje_inexistente_cambia_cero_filas(self):
        mensaje = self.repo.buscar_por_id(self.id_mensaje)
        mensaje.id_mensaje = 9999
        mensaje.editar("no existe", en(0))
        self.assertEqual(self.repo.actualizar_texto(mensaje), 0)

    # --- eliminar ------------------------------------------------------------------

    def test_eliminar_borra_solo_ese_mensaje_y_dice_cuantas_filas(self):
        otro = crear_mensaje(self.con, self.ana, "otro mensaje", en(-1))
        self.assertEqual(self.repo.eliminar(self.id_mensaje), 1)
        self.assertIsNone(self.repo.buscar_por_id(self.id_mensaje))
        self.assertIsNotNone(self.repo.buscar_por_id(otro))

    def test_eliminar_un_mensaje_que_no_existe_borra_cero_filas(self):
        self.assertEqual(self.repo.eliminar(9999), 0)
        self.assertEqual(contar(self.con, "mensajes"), 1)

    def test_las_claves_foraneas_impiden_borrar_un_mensaje_republicado(self):
        # La red de seguridad del borrado en cascada (DISEÑO §6.6): si el código se
        # olvidara de borrar primero las republicaciones, el DELETE fallaría.
        republicar(self.con, self.beto, self.id_mensaje)
        with self.assertRaises(sqlite3.IntegrityError):
            self.repo.eliminar(self.id_mensaje)
        self.assertEqual(contar(self.con, "mensajes"), 1)


class PruebaRepositorioRepublicacionesNuevas(PruebaConBase):
    def setUp(self):
        super().setUp()
        self.ana = crear_usuario(self.con, "ana")
        self.beto = crear_usuario(self.con, "beto")
        self.carla = crear_usuario(self.con, "carla")
        self.mensaje_a = crear_mensaje(self.con, self.ana, "mensaje A", en(-10))
        self.mensaje_b = crear_mensaje(self.con, self.ana, "mensaje B", en(-9))
        self.repo = RepositorioRepublicaciones()

    # --- existe --------------------------------------------------------------------

    def test_existe_responde_por_el_par_usuario_mensaje(self):
        republicar(self.con, self.beto, self.mensaje_a)
        self.assertTrue(self.repo.existe(self.beto, self.mensaje_a))
        self.assertFalse(self.repo.existe(self.beto, self.mensaje_b))  # otro mensaje
        self.assertFalse(self.repo.existe(self.carla, self.mensaje_a))  # otro usuario

    # --- crear ---------------------------------------------------------------------

    def test_crear_devuelve_el_id_y_guarda_quien_cuando_y_la_referencia(self):
        id_republicacion = self.repo.crear(self.beto, self.mensaje_a, en(0))
        fila = self.con.execute(
            "SELECT * FROM republicaciones WHERE id_republicacion = ?", (id_republicacion,)
        ).fetchone()
        self.assertEqual(fila["id_usuario"], self.beto)
        self.assertEqual(fila["id_mensaje"], self.mensaje_a)
        self.assertEqual(fila["fecha_republicacion"], en(0).isoformat())

    def test_la_tabla_no_tiene_columna_de_texto_la_republicacion_no_copia_nada(self):
        # C23: una republicación apunta al original, no lo copia.
        columnas = [f["name"] for f in self.con.execute("PRAGMA table_info(republicaciones)")]
        self.assertNotIn("texto", columnas)
        self.assertEqual(
            sorted(columnas),
            ["fecha_republicacion", "id_mensaje", "id_republicacion", "id_usuario"],
        )

    def test_crear_dos_veces_lo_mismo_choca_con_el_unique_de_la_tabla(self):
        # Segunda barrera de ca 7.3: la primera es existe(), en la lógica.
        self.repo.crear(self.beto, self.mensaje_a, AHORA)
        with self.assertRaises(sqlite3.IntegrityError):
            self.repo.crear(self.beto, self.mensaje_a, AHORA)
        self.assertEqual(contar(self.con, "republicaciones"), 1)

    def test_dos_usuarios_pueden_republicar_el_mismo_mensaje(self):
        self.repo.crear(self.beto, self.mensaje_a, AHORA)
        self.repo.crear(self.carla, self.mensaje_a, AHORA)
        self.assertEqual(contar(self.con, "republicaciones"), 2)

    # --- eliminar_por_mensaje ------------------------------------------------------

    def test_eliminar_por_mensaje_borra_solo_las_de_ese_mensaje(self):
        republicar(self.con, self.beto, self.mensaje_a)
        republicar(self.con, self.carla, self.mensaje_a)
        republicar(self.con, self.beto, self.mensaje_b)
        self.assertEqual(self.repo.eliminar_por_mensaje(self.mensaje_a), 2)
        self.assertFalse(self.repo.existe(self.beto, self.mensaje_a))
        self.assertFalse(self.repo.existe(self.carla, self.mensaje_a))
        self.assertTrue(self.repo.existe(self.beto, self.mensaje_b))

    def test_eliminar_por_mensaje_sin_republicaciones_borra_cero(self):
        self.assertEqual(self.repo.eliminar_por_mensaje(self.mensaje_a), 0)


if __name__ == "__main__":
    unittest.main()