"""Pruebas de CU0009 Visualizar Tablón en la capa de lógica (ControlTablon).

Se arma un caso con varios usuarios, seguimientos, mensajes y republicaciones, y se
comprueba qué entra en el tablón de ana y en qué orden (rnf 9.1 y rnf 9.2).
"""

from __future__ import annotations

import unittest

from miblog.acceso_datos.repositorio_mensajes import RepositorioMensajes
from miblog.acceso_datos.repositorio_republicaciones import RepositorioRepublicaciones
from miblog.acceso_datos.repositorio_usuarios import RepositorioUsuarios
from miblog.logica.dominio.mensaje import ElementoDeTablon
from miblog.logica.gestion_mensajes.control_tablon import ControlTablon

from pruebas.ayudas import (
    PruebaConBase,
    crear_mensaje,
    crear_usuario,
    en,
    republicar,
    seguir,
)


class PruebaControlTablon(PruebaConBase):
    def setUp(self):
        super().setUp()
        self.ana = crear_usuario(self.con, "ana")
        self.beto = crear_usuario(self.con, "beto")
        self.carla = crear_usuario(self.con, "carla")
        self.dani = crear_usuario(self.con, "dani")
        seguir(self.con, self.ana, self.beto)  # ana sigue solo a beto

        self.de_ana = crear_mensaje(self.con, self.ana, "A de ana", en(0))
        crear_mensaje(self.con, self.beto, "B de beto", en(5))
        self.de_carla = crear_mensaje(self.con, self.carla, "C de carla", en(-20))
        crear_mensaje(self.con, self.dani, "D de dani", en(7))  # ana no sigue a dani

        # beto republica el mensaje de ana y el de carla; dani republica el de beto.
        republicar(self.con, self.beto, self.de_ana, en(10))
        republicar(self.con, self.beto, self.de_carla, en(3))
        republicar(self.con, self.dani, 2, en(12))

        self.control = ControlTablon(RepositorioMensajes(), RepositorioRepublicaciones())
        self.usuario_ana = RepositorioUsuarios().buscar_activo_por_id(self.ana)

    def resumen(self, tablon):
        """[(texto, quién republicó o None), ...] en el orden del tablón."""
        return [
            (e.obtener_texto_vigente(),
             e.obtener_republicador().nombre_usuario if e.obtener_republicador() else None)
            for e in tablon
        ]

    def test_mezcla_mensajes_y_republicaciones_del_mas_nuevo_al_mas_viejo(self):
        tablon = self.control.obtener_tablon(self.usuario_ana)
        self.assertEqual(
            self.resumen(tablon),
            [
                ("A de ana", "beto"),     # republicación de beto, t = 10
                ("B de beto", None),      # t = 5
                ("C de carla", "beto"),   # republicación de beto, t = 3
                ("A de ana", None),       # t = 0
            ],
        )

    def test_no_aparece_lo_de_quien_no_se_sigue(self):
        textos = [texto for texto, _ in self.resumen(self.control.obtener_tablon(self.usuario_ana))]
        self.assertNotIn("D de dani", textos)  # mensaje de dani
        # Carla no es seguida: su mensaje solo está porque beto lo republicó.
        self.assertEqual(textos.count("C de carla"), 1)

    def test_todo_es_un_elemento_de_tablon_y_la_fecha_de_orden_baja(self):
        tablon = self.control.obtener_tablon(self.usuario_ana)
        self.assertTrue(all(isinstance(e, ElementoDeTablon) for e in tablon))
        fechas = [e.obtener_fecha_de_orden() for e in tablon]
        self.assertEqual(fechas, sorted(fechas, reverse=True))

    def test_ca_9_1_tablon_vacio_es_una_lista_vacia_no_un_error(self):
        eva = crear_usuario(self.con, "eva")
        usuario_eva = RepositorioUsuarios().buscar_activo_por_id(eva)
        self.assertEqual(self.control.obtener_tablon(usuario_eva), [])

    def test_un_mensaje_editado_se_ve_editado_tambien_en_su_republicacion(self):
        self.con.execute(
            "UPDATE mensajes SET texto = 'A editado', editado = 1, fecha_ultima_edicion = ? "
            "WHERE id_mensaje = ?",
            (en(30).isoformat(), self.de_ana),
        )
        tablon = self.control.obtener_tablon(self.usuario_ana)
        del_mensaje = [e for e in tablon if e.obtener_id_mensaje() == self.de_ana]
        self.assertEqual(len(del_mensaje), 2)  # el original y la republicación de beto
        for elemento in del_mensaje:
            self.assertEqual(elemento.obtener_texto_vigente(), "A editado")
            self.assertTrue(elemento.esta_editado())


if __name__ == "__main__":
    unittest.main()