"""Pruebas de los tres repositorios del bloque 4.4 contra una base de verdad.

Cada prueba arranca con una base vacía (ver ayudas.py). Se prueba la capa de acceso
a datos sola: sin controles ni HTTP.
"""

from __future__ import annotations

import unittest

from miblog.acceso_datos.repositorio_elementos import RepositorioElementos
from miblog.acceso_datos.repositorio_mensajes import RepositorioMensajes
from miblog.acceso_datos.repositorio_republicaciones import RepositorioRepublicaciones
from miblog.logica.dominio.elementos import Enlace, Etiqueta, Mencion, RegistroDeElementos
from miblog.logica.dominio.enumeraciones import OrigenPublicacion
from miblog.logica.dominio.mensaje import MensajePublico
from miblog.logica.dominio.republicacion import Republicacion
from miblog.logica.dominio.usuario import Usuario

from pruebas.ayudas import (
    PruebaConBase,
    contar,
    crear_mensaje,
    crear_usuario,
    en,
    republicar,
    seguir,
)


class PruebaRepositorioElementos(PruebaConBase):
    def setUp(self):
        super().setUp()
        self.ana = crear_usuario(self.con, "ana")
        self.beto = crear_usuario(self.con, "beto")
        crear_usuario(self.con, "inactivo", activo=0)
        self.mensaje_1 = crear_mensaje(self.con, self.ana, "uno")
        self.mensaje_2 = crear_mensaje(self.con, self.ana, "dos")
        self.repo = RepositorioElementos()

    def test_cumple_la_interfaz_del_dominio(self):
        # La lógica depende de RegistroDeElementos, no de este repositorio (inversión
        # de dependencias).
        self.assertIsInstance(self.repo, RegistroDeElementos)

    def test_una_etiqueta_es_una_sola_fila_aunque_la_usen_varios_mensajes(self):
        pizza = Etiqueta("pizza")
        pizza.guardar_en(self.repo, self.mensaje_1)
        Etiqueta("pizza").guardar_en(self.repo, self.mensaje_2)
        Etiqueta("vino").guardar_en(self.repo, self.mensaje_2)
        self.assertEqual(contar(self.con, "etiquetas"), 2)
        self.assertEqual(contar(self.con, "mensaje_etiqueta"), 3)
        self.assertIsNotNone(pizza.id_etiqueta)

    def test_repetir_la_etiqueta_en_el_mismo_mensaje_no_duplica(self):
        Etiqueta("pizza").guardar_en(self.repo, self.mensaje_1)
        Etiqueta("pizza").guardar_en(self.repo, self.mensaje_1)
        self.assertEqual(contar(self.con, "mensaje_etiqueta"), 1)

    def test_mencion_a_un_usuario_existente_no_distingue_mayusculas(self):
        guardada = self.repo.registrar_mencion(self.mensaje_1, Mencion("BETO", 5))
        self.assertTrue(guardada)
        fila = self.con.execute(
            "SELECT id_usuario_mencionado, posicion_en_texto FROM menciones"
        ).fetchone()
        self.assertEqual((fila[0], fila[1]), (self.beto, 5))

    def test_mencion_a_alguien_que_no_existe_se_descarta_sin_error(self):
        self.assertFalse(self.repo.registrar_mencion(self.mensaje_1, Mencion("fantasma", 0)))
        Mencion("fantasma", 0).guardar_en(self.repo, self.mensaje_1)  # tampoco falla
        self.assertEqual(contar(self.con, "menciones"), 0)

    def test_mencion_a_un_usuario_inactivo_se_descarta(self):
        self.assertFalse(self.repo.registrar_mencion(self.mensaje_1, Mencion("inactivo", 0)))
        self.assertEqual(contar(self.con, "menciones"), 0)

    def test_guarda_el_enlace(self):
        Enlace("https://ejemplo.com/x?a=1").guardar_en(self.repo, self.mensaje_1)
        url = self.con.execute("SELECT url FROM enlaces").fetchone()[0]
        self.assertEqual(url, "https://ejemplo.com/x?a=1")

    def test_eliminar_de_mensaje_limpia_solo_ese_mensaje(self):
        for mensaje in (self.mensaje_1, self.mensaje_2):
            Etiqueta("pizza").guardar_en(self.repo, mensaje)
        Mencion("beto", 0).guardar_en(self.repo, self.mensaje_1)
        Enlace("https://a.com").guardar_en(self.repo, self.mensaje_1)

        self.repo.eliminar_de_mensaje(self.mensaje_1)

        self.assertEqual(contar(self.con, "menciones"), 0)
        self.assertEqual(contar(self.con, "enlaces"), 0)
        restantes = self.con.execute("SELECT id_mensaje FROM mensaje_etiqueta").fetchall()
        self.assertEqual([f[0] for f in restantes], [self.mensaje_2])
        # La etiqueta en sí no se borra: puede estar en otros mensajes.
        self.assertEqual(contar(self.con, "etiquetas"), 1)


class PruebaRepositorioMensajes(PruebaConBase):
    def setUp(self):
        super().setUp()
        self.ana = crear_usuario(self.con, "ana")
        self.beto = crear_usuario(self.con, "beto", nombre_completo="Beto Pérez")
        self.carla = crear_usuario(self.con, "carla")
        seguir(self.con, self.ana, self.beto)  # ana sigue a beto; nadie sigue a carla
        self.repo = RepositorioMensajes()

    def publicar(self, id_autor, texto, minutos=0):
        autor = Usuario(id_usuario=id_autor, nombre_usuario="x", nombre_completo="x")
        return self.repo.crear(MensajePublico.publicar(autor, texto, en(minutos)))

    def test_crear_devuelve_el_id_y_guarda_los_datos(self):
        id_mensaje = self.publicar(self.ana, "hola", minutos=3)
        fila = self.con.execute("SELECT * FROM mensajes WHERE id_mensaje = ?", (id_mensaje,)).fetchone()
        self.assertEqual(fila["id_autor"], self.ana)
        self.assertEqual(fila["texto"], "hola")
        self.assertEqual(fila["origen"], OrigenPublicacion.WEB.value)
        self.assertEqual(fila["editado"], 0)
        self.assertIsNone(fila["fecha_ultima_edicion"])

    def test_el_tablon_trae_lo_propio_y_lo_de_los_seguidos_pero_no_lo_de_otros(self):
        mio = self.publicar(self.ana, "mío")
        de_beto = self.publicar(self.beto, "de beto")
        self.publicar(self.carla, "de carla")
        ids = sorted(m.id_mensaje for m in self.repo.buscar_publicos_para_tablon(self.ana))
        self.assertEqual(ids, sorted([mio, de_beto]))

    def test_el_autor_llega_resumido_sin_email_ni_clave(self):
        self.publicar(self.beto, "de beto")
        [mensaje] = self.repo.buscar_publicos_para_tablon(self.beto)
        self.assertEqual(mensaje.autor.nombre_usuario, "beto")
        self.assertEqual(mensaje.autor.nombre_completo, "Beto Pérez")
        self.assertIsNone(mensaje.autor.email)
        self.assertIsNone(mensaje.autor.clave_hash)

    def test_un_mensaje_comun_no_tiene_republicador_ni_esta_editado(self):
        self.publicar(self.beto, "de beto")
        [mensaje] = self.repo.buscar_publicos_para_tablon(self.beto)
        self.assertIsNone(mensaje.obtener_republicador())
        self.assertFalse(mensaje.esta_editado())

    def test_la_fecha_vuelve_con_zona_horaria(self):
        self.publicar(self.beto, "de beto", minutos=5)
        [mensaje] = self.repo.buscar_publicos_para_tablon(self.beto)
        self.assertIsNotNone(mensaje.fecha_publicacion.tzinfo)
        self.assertEqual(mensaje.fecha_publicacion, en(5))

    def test_quien_no_sigue_a_nadie_ni_publico_ve_el_tablon_vacio(self):
        dani = crear_usuario(self.con, "dani")
        self.assertEqual(self.repo.buscar_publicos_para_tablon(dani), [])


class PruebaRepositorioRepublicaciones(PruebaConBase):
    def setUp(self):
        super().setUp()
        self.ana = crear_usuario(self.con, "ana")
        self.beto = crear_usuario(self.con, "beto")
        self.carla = crear_usuario(self.con, "carla", nombre_completo="Carla Gómez")
        self.dani = crear_usuario(self.con, "dani")
        seguir(self.con, self.ana, self.beto)
        # Carla publica; beto (a quien sigue ana) y dani (a quien no) la republican.
        self.original = crear_mensaje(self.con, self.carla, "original de carla", en(0))
        republicar(self.con, self.beto, self.original, en(10))
        republicar(self.con, self.dani, self.original, en(20))
        self.repo = RepositorioRepublicaciones()

    def test_se_filtra_por_quien_republico_no_por_el_autor_del_original(self):
        # Ana no sigue a carla (la autora), pero sí a beto (quien republicó): lo ve.
        # La republicación de dani no, porque ana no lo sigue a él.
        [republicacion] = self.repo.buscar_para_tablon(self.ana)
        self.assertIsInstance(republicacion, Republicacion)
        self.assertEqual(republicacion.obtener_republicador().nombre_usuario, "beto")

    def test_conserva_al_autor_original_y_su_texto(self):
        [republicacion] = self.repo.buscar_para_tablon(self.ana)
        self.assertEqual(republicacion.obtener_autor_original().nombre_usuario, "carla")
        self.assertEqual(republicacion.obtener_texto_vigente(), "original de carla")
        self.assertEqual(republicacion.obtener_id_mensaje(), self.original)

    def test_para_ordenar_usa_la_fecha_de_la_republicacion(self):
        [republicacion] = self.repo.buscar_para_tablon(self.ana)
        self.assertEqual(republicacion.obtener_fecha_de_orden(), en(10))

    def test_si_el_original_se_edita_la_republicacion_muestra_el_texto_nuevo(self):
        self.con.execute(
            "UPDATE mensajes SET texto = 'editado por carla', editado = 1, "
            "fecha_ultima_edicion = ? WHERE id_mensaje = ?",
            (en(30).isoformat(), self.original),
        )
        [republicacion] = self.repo.buscar_para_tablon(self.ana)
        self.assertEqual(republicacion.obtener_texto_vigente(), "editado por carla")
        self.assertTrue(republicacion.esta_editado())

    def test_cada_uno_ve_las_republicaciones_propias(self):
        self.assertEqual(len(self.repo.buscar_para_tablon(self.dani)), 1)
        self.assertEqual(len(self.repo.buscar_para_tablon(self.beto)), 1)

    def test_quien_no_republico_ni_sigue_a_nadie_no_ve_ninguna(self):
        self.assertEqual(self.repo.buscar_para_tablon(self.carla), [])


if __name__ == "__main__":
    unittest.main()