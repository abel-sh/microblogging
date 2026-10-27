"""Pruebas de CU0005 Editar y CU0006 Borrar Mensaje Propio en la capa de lógica.

Se prueba Edicion (la segunda operación del Template Method) y los métodos
verificar_autoria, editar y borrar de ControlPublicacion, con repositorios de verdad
sobre una base temporal. Cubre ca 5.1 a ca 5.3, ca 6.1, ca 6.2, rnf 5.1, rnf 5.2,
rnf 6.1 y rnf 6.3, y el caso directo del Decorator: editar un mensaje
republicado y comprobar que la republicación muestra el texto nuevo.
"""

from __future__ import annotations

import unittest
from unittest.mock import patch

from miblog.acceso_datos.repositorio_elementos import RepositorioElementos
from miblog.acceso_datos.repositorio_mensajes import RepositorioMensajes
from miblog.acceso_datos.repositorio_republicaciones import RepositorioRepublicaciones
from miblog.acceso_datos.repositorio_usuarios import RepositorioUsuarios
from miblog.logica.dominio.errores import (
    MensajeInexistenteError,
    NoEsAutorError,
    TextoExcedidoError,
    TextoVacioError,
)
from miblog.logica.gestion_mensajes.analizador import AnalizadorDeTexto
from miblog.logica.gestion_mensajes.control_publicacion import ControlPublicacion
from miblog.logica.gestion_mensajes.control_tablon import ControlTablon
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

from pruebas.ayudas import PruebaConBase, contar, crear_usuario, republicar, seguir

LIMITE = OperacionSobreMensaje.LIMITE
TABLAS_DE_UN_MENSAJE = ["mensajes", "etiquetas", "mensaje_etiqueta", "menciones", "enlaces"]
TEXTO_ORIGINAL = "Hola @beto #viejo https://viejo.com/a"


class PruebaConLaLogicaArmada(PruebaConBase):
    """Arma los repositorios, las dos operaciones y el control, como lo hace crear_app()."""

    def setUp(self):
        super().setUp()
        self.id_ana = crear_usuario(self.con, "ana", "Ana Pérez")
        self.id_beto = crear_usuario(self.con, "beto", "Beto Pérez")
        self.id_carla = crear_usuario(self.con, "carla", "Carla Gómez")
        repo_usuarios = RepositorioUsuarios()
        self.ana = repo_usuarios.buscar_activo_por_id(self.id_ana)
        self.beto = repo_usuarios.buscar_activo_por_id(self.id_beto)

        self.repo_mensajes = RepositorioMensajes()
        self.repo_republicaciones = RepositorioRepublicaciones()
        self.repo_elementos = RepositorioElementos()
        analizador = AnalizadorDeTexto(
            [ExtractorEtiquetas(), ExtractorMenciones(), ExtractorEnlaces()]
        )
        self.publicacion = Publicacion(analizador, self.repo_mensajes, self.repo_elementos)
        self.edicion = Edicion(analizador, self.repo_mensajes, self.repo_elementos)
        self.control = ControlPublicacion(
            self.publicacion,
            self.edicion,
            self.repo_mensajes,
            self.repo_republicaciones,
            self.repo_elementos,
        )

    def contadores(self):
        return {tabla: contar(self.con, tabla) for tabla in TABLAS_DE_UN_MENSAJE}

    def fila_del_mensaje(self, id_mensaje):
        return self.con.execute(
            "SELECT texto, editado, fecha_ultima_edicion FROM mensajes WHERE id_mensaje = ?",
            (id_mensaje,),
        ).fetchone()

    def enlaces_del_mensaje(self, id_mensaje):
        return [f[0] for f in self.con.execute(
            "SELECT url FROM enlaces WHERE id_mensaje = ?", (id_mensaje,))]

    def etiquetas_del_mensaje(self, id_mensaje):
        return [f[0] for f in self.con.execute(
            "SELECT e.nombre FROM etiquetas AS e JOIN mensaje_etiqueta AS me"
            " ON me.id_etiqueta = e.id_etiqueta WHERE me.id_mensaje = ?", (id_mensaje,))]


class PruebaEdicion(PruebaConLaLogicaArmada):
    def setUp(self):
        super().setUp()
        self.mensaje = self.publicacion.ejecutar(self.ana, TEXTO_ORIGINAL)

    # --- La forma del Template Method ---------------------------------------------

    def test_edicion_es_la_segunda_clase_concreta_del_template_method(self):
        self.assertTrue(issubclass(Edicion, OperacionSobreMensaje))
        self.assertIs(Edicion.ejecutar, OperacionSobreMensaje.ejecutar)

    def test_edicion_completa_solo_sus_pasos_y_comparte_los_demas(self):
        # Los pasos invariantes (validar el texto y reemplazar los elementos) están
        # una sola vez, en la clase base: la regla del límite no se repite.
        for compartido in ["ejecutar", "_validar_texto", "_reemplazar_elementos"]:
            with self.subTest(paso=compartido):
                self.assertNotIn(compartido, vars(Edicion))
                self.assertIn(compartido, vars(OperacionSobreMensaje))
        for propio in ["_autorizar", "_persistir_mensaje"]:
            with self.subTest(paso=propio):
                self.assertIn(propio, vars(Edicion))

    # --- Curso normal --------------------------------------------------------------

    def test_edita_el_texto_marca_editado_y_pone_la_fecha(self):
        editado = self.edicion.ejecutar(self.ana, "  texto nuevo  ", id_mensaje=self.mensaje.id_mensaje)
        self.assertEqual(editado.id_mensaje, self.mensaje.id_mensaje)
        self.assertEqual(editado.texto, "texto nuevo")  # mismo recorte que al publicar 
        self.assertTrue(editado.editado)
        self.assertIsNotNone(editado.fecha_ultima_edicion)

        fila = self.fila_del_mensaje(self.mensaje.id_mensaje)
        self.assertEqual(fila["texto"], "texto nuevo")
        self.assertEqual(fila["editado"], 1)
        self.assertIsNotNone(fila["fecha_ultima_edicion"])

    def test_no_cambia_el_autor_el_origen_ni_la_fecha_de_publicacion(self):
        self.edicion.ejecutar(self.ana, "otro texto", id_mensaje=self.mensaje.id_mensaje)
        releido = self.repo_mensajes.buscar_por_id(self.mensaje.id_mensaje)
        self.assertEqual(releido.autor.id_usuario, self.id_ana)
        self.assertEqual(releido.origen, self.mensaje.origen)
        self.assertEqual(releido.fecha_publicacion, self.mensaje.fecha_publicacion)

    def test_editar_no_crea_un_mensaje_nuevo(self):
        self.edicion.ejecutar(self.ana, "otro texto", id_mensaje=self.mensaje.id_mensaje)
        self.assertEqual(contar(self.con, "mensajes"), 1)

    def test_editar_otra_vez_actualiza_la_fecha_de_la_ultima_edicion(self):
        primera = self.edicion.ejecutar(self.ana, "uno", id_mensaje=self.mensaje.id_mensaje)
        segunda = self.edicion.ejecutar(self.ana, "dos", id_mensaje=self.mensaje.id_mensaje)
        self.assertGreaterEqual(segunda.fecha_ultima_edicion, primera.fecha_ultima_edicion)
        self.assertEqual(self.fila_del_mensaje(self.mensaje.id_mensaje)["texto"], "dos")

    def test_edita_con_justo_el_limite_y_no_con_uno_mas(self):
        self.edicion.ejecutar(self.ana, "z" * LIMITE, id_mensaje=self.mensaje.id_mensaje)
        with self.assertRaises(TextoExcedidoError):
            self.edicion.ejecutar(self.ana, "z" * (LIMITE + 1), id_mensaje=self.mensaje.id_mensaje)

    # --- Paso 6: se recalculan los elementos ---------------------------------------

    def test_los_elementos_viejos_se_reemplazan_por_los_del_texto_nuevo(self):
        id_mensaje = self.mensaje.id_mensaje
        self.assertEqual(self.etiquetas_del_mensaje(id_mensaje), ["viejo"])
        self.assertEqual(contar(self.con, "menciones"), 1)

        self.edicion.ejecutar(self.ana, "Chau #nueva https://nuevo.com/b", id_mensaje=id_mensaje)

        self.assertEqual(self.etiquetas_del_mensaje(id_mensaje), ["nueva"])
        self.assertEqual(self.enlaces_del_mensaje(id_mensaje), ["https://nuevo.com/b"])
        self.assertEqual(contar(self.con, "menciones"), 0)  # la mención a @beto se fue

    def test_la_etiqueta_que_queda_sin_uso_sigue_registrada(self):
        # {Ob 6.2}: las etiquetas no se borran, solo se libera su asociación.
        self.edicion.ejecutar(self.ana, "sin etiquetas", id_mensaje=self.mensaje.id_mensaje)
        self.assertEqual(self.etiquetas_del_mensaje(self.mensaje.id_mensaje), [])
        self.assertEqual(contar(self.con, "etiquetas"), 1)

    def test_las_menciones_se_vuelven_a_validar_con_el_texto_nuevo(self):
        # Paso 7 de CU0004, que CU0005 repite: una mención a alguien que no existe se descarta.
        self.edicion.ejecutar(
            self.ana, "ahora @carla y @fantasma", id_mensaje=self.mensaje.id_mensaje
        )
        mencionados = [f[0] for f in self.con.execute("SELECT id_usuario_mencionado FROM menciones")]
        self.assertEqual(mencionados, [self.id_carla])

    # --- ca 5.1 y ca 5.2: se verifica DENTRO de la operación (rnf 5.1) -------------

    def test_ca_5_1_si_el_mensaje_ya_no_existe_lanza_el_error_y_no_escribe(self):
        antes = self.contadores()
        with self.assertRaises(MensajeInexistenteError):
            self.edicion.ejecutar(self.ana, "texto", id_mensaje=9999)
        self.assertEqual(self.contadores(), antes)

    def test_ca_5_2_quien_no_es_el_autor_no_puede_editar_aunque_mande_el_pedido_directo(self):
        with self.assertRaises(NoEsAutorError):
            self.edicion.ejecutar(self.beto, "texto de beto", id_mensaje=self.mensaje.id_mensaje)
        fila = self.fila_del_mensaje(self.mensaje.id_mensaje)
        self.assertEqual(fila["texto"], TEXTO_ORIGINAL)
        self.assertEqual(fila["editado"], 0)

    def test_la_autoria_se_verifica_antes_que_el_texto(self):
        # Con un texto vacío y sin ser el autor, el error es de autoría: no se le
        # cuenta a un extraño qué tiene mal el texto.
        with self.assertRaises(NoEsAutorError):
            self.edicion.ejecutar(self.beto, "   ", id_mensaje=self.mensaje.id_mensaje)

    # --- ca 5.3: el texto original queda intacto -----------------------------------

    def test_ca_5_3_texto_vacio_conserva_todo_lo_original(self):
        antes = self.contadores()
        for vacio in ["", "   ", "\n\r\n"]:
            with self.subTest(texto=repr(vacio)), self.assertRaises(TextoVacioError):
                self.edicion.ejecutar(self.ana, vacio, id_mensaje=self.mensaje.id_mensaje)
        fila = self.fila_del_mensaje(self.mensaje.id_mensaje)
        self.assertEqual((fila["texto"], fila["editado"]), (TEXTO_ORIGINAL, 0))
        self.assertEqual(self.contadores(), antes)

    def test_ca_5_3_texto_excedido_informa_cuanto_sobra_y_conserva_todo(self):
        with self.assertRaises(TextoExcedidoError) as contexto:
            self.edicion.ejecutar(self.ana, "x" * (LIMITE + 4), id_mensaje=self.mensaje.id_mensaje)
        self.assertEqual(contexto.exception.excedente, 4)
        fila = self.fila_del_mensaje(self.mensaje.id_mensaje)
        self.assertEqual((fila["texto"], fila["editado"]), (TEXTO_ORIGINAL, 0))
        self.assertEqual(self.etiquetas_del_mensaje(self.mensaje.id_mensaje), ["viejo"])

    # --- rnf 4.4 aplicado a editar: todo o nada ------------------------------------

    def test_si_falla_un_paso_a_mitad_no_queda_nada_a_medias(self):
        antes = self.contadores()
        with patch.object(
            self.repo_elementos, "registrar_enlace", side_effect=RuntimeError("falla simulada")
        ):
            with self.assertRaises(RuntimeError):
                self.edicion.ejecutar(
                    self.ana, "otro #etiquetanueva https://roto.com", id_mensaje=self.mensaje.id_mensaje
                )
        fila = self.fila_del_mensaje(self.mensaje.id_mensaje)
        self.assertEqual((fila["texto"], fila["editado"]), (TEXTO_ORIGINAL, 0))
        self.assertEqual(self.etiquetas_del_mensaje(self.mensaje.id_mensaje), ["viejo"])
        self.assertEqual(self.contadores(), antes)
        self.assertFalse(self.con.in_transaction)

    # --- ControlPublicacion --------------------------------------------------------

    def test_el_control_editar_delega_en_la_operacion(self):
        editado = self.control.editar(self.mensaje.id_mensaje, self.ana, "por el control")
        self.assertEqual(editado.texto, "por el control")
        self.assertTrue(editado.editado)

    def test_el_control_propaga_los_errores_de_negocio_para_que_la_vista_los_muestre(self):
        casos = [
            (9999, self.ana, "x", MensajeInexistenteError),
            (self.mensaje.id_mensaje, self.beto, "x", NoEsAutorError),
            (self.mensaje.id_mensaje, self.ana, " ", TextoVacioError),
            (self.mensaje.id_mensaje, self.ana, "x" * 500, TextoExcedidoError),
        ]
        for id_mensaje, usuario, texto, error in casos:
            with self.subTest(error=error.__name__), self.assertRaises(error):
                self.control.editar(id_mensaje, usuario, texto)

    # --- Decorator: el caso directo de ANALISIS -------------------------------

    def test_editar_un_mensaje_republicado_hace_que_la_republicacion_muestre_el_texto_nuevo(self):
        # carla sigue a beto; beto republica el mensaje de ana; ana lo edita.
        # Ningún mensaje se dirige a la republicación: la tabla ni se toca.
        seguir(self.con, self.id_carla, self.id_beto)
        republicar(self.con, self.id_beto, self.mensaje.id_mensaje)
        republicaciones_antes = self.con.execute("SELECT * FROM republicaciones").fetchall()
        control_tablon = ControlTablon(self.repo_mensajes, self.repo_republicaciones)
        carla = RepositorioUsuarios().buscar_activo_por_id(self.id_carla)

        antes = control_tablon.obtener_tablon(carla)
        self.assertEqual([e.obtener_texto_vigente() for e in antes], [TEXTO_ORIGINAL])
        self.assertFalse(antes[0].esta_editado())

        self.control.editar(self.mensaje.id_mensaje, self.ana, "texto editado por ana")

        despues = control_tablon.obtener_tablon(carla)
        self.assertEqual(len(despues), 1)
        republicacion = despues[0]
        self.assertEqual(republicacion.obtener_republicador().nombre_usuario, "beto")
        self.assertEqual(republicacion.obtener_texto_vigente(), "texto editado por ana")
        self.assertTrue(republicacion.esta_editado())
        self.assertIsNotNone(republicacion.obtener_fecha_ultima_edicion())
        self.assertEqual(
            self.con.execute("SELECT * FROM republicaciones").fetchall(), republicaciones_antes
        )


class PruebaVerificarAutoria(PruebaConLaLogicaArmada):
    def setUp(self):
        super().setUp()
        self.mensaje = self.publicacion.ejecutar(self.ana, "mensaje de ana")

    def test_devuelve_el_mensaje_si_es_el_autor(self):
        mensaje = self.control.verificar_autoria(self.mensaje.id_mensaje, self.ana)
        self.assertEqual(mensaje.id_mensaje, self.mensaje.id_mensaje)
        self.assertEqual(mensaje.texto, "mensaje de ana")

    def test_ca_5_1_ca_6_1_mensaje_inexistente(self):
        with self.assertRaises(MensajeInexistenteError):
            self.control.verificar_autoria(9999, self.ana)

    def test_ca_5_2_ca_6_2_no_es_el_autor(self):
        with self.assertRaises(NoEsAutorError):
            self.control.verificar_autoria(self.mensaje.id_mensaje, self.beto)

    def test_solo_lee_no_deja_una_transaccion_abierta(self):
        self.control.verificar_autoria(self.mensaje.id_mensaje, self.ana)
        self.assertFalse(self.con.in_transaction)


class PruebaBorrado(PruebaConLaLogicaArmada):
    def setUp(self):
        super().setUp()
        # El mensaje a borrar tiene etiqueta, mención y enlace, y dos republicaciones.
        self.mensaje = self.publicacion.ejecutar(self.ana, TEXTO_ORIGINAL)
        self.id_mensaje = self.mensaje.id_mensaje
        republicar(self.con, self.id_beto, self.id_mensaje)
        republicar(self.con, self.id_carla, self.id_mensaje)
        # Otro mensaje de ana, también republicado, que NO se tiene que tocar.
        self.otro = self.publicacion.ejecutar(self.ana, "el otro #conservada https://otro.com")
        republicar(self.con, self.id_beto, self.otro.id_mensaje)

    # --- Curso normal: la cascada --------------------------------------------------

    def test_borra_el_mensaje_sus_republicaciones_y_sus_elementos(self):
        self.control.borrar(self.id_mensaje, self.ana)

        self.assertIsNone(self.repo_mensajes.buscar_por_id(self.id_mensaje))
        self.assertFalse(self.repo_republicaciones.existe(self.id_beto, self.id_mensaje))
        self.assertFalse(self.repo_republicaciones.existe(self.id_carla, self.id_mensaje))
        self.assertEqual(self.etiquetas_del_mensaje(self.id_mensaje), [])
        self.assertEqual(self.enlaces_del_mensaje(self.id_mensaje), [])
        mencionados = self.con.execute(
            "SELECT COUNT(*) FROM menciones WHERE id_mensaje = ?", (self.id_mensaje,)
        ).fetchone()[0]
        self.assertEqual(mencionados, 0)

    def test_no_toca_el_otro_mensaje_ni_sus_republicaciones_ni_sus_elementos(self):
        self.control.borrar(self.id_mensaje, self.ana)

        otro = self.otro.id_mensaje
        self.assertIsNotNone(self.repo_mensajes.buscar_por_id(otro))
        self.assertTrue(self.repo_republicaciones.existe(self.id_beto, otro))
        self.assertEqual(self.etiquetas_del_mensaje(otro), ["conservada"])
        self.assertEqual(self.enlaces_del_mensaje(otro), ["https://otro.com"])

    def test_las_etiquetas_quedan_registradas(self):
        # {Ob 6.2}: se libera la asociación, la etiqueta no se borra.
        self.control.borrar(self.id_mensaje, self.ana)
        nombres = sorted(f[0] for f in self.con.execute("SELECT nombre FROM etiquetas"))
        self.assertEqual(nombres, ["conservada", "viejo"])

    def test_el_mensaje_borrado_desaparece_de_los_tablones_donde_estaba_republicado(self):
        seguir(self.con, self.id_carla, self.id_beto)  # carla ve lo que republica beto
        control_tablon = ControlTablon(self.repo_mensajes, self.repo_republicaciones)
        carla = RepositorioUsuarios().buscar_activo_por_id(self.id_carla)
        textos = lambda: sorted(e.obtener_texto_vigente() for e in control_tablon.obtener_tablon(carla))
        self.assertIn(TEXTO_ORIGINAL, textos())

        self.control.borrar(self.id_mensaje, self.ana)

        self.assertNotIn(TEXTO_ORIGINAL, textos())

    def test_el_orden_es_primero_republicaciones_despues_elementos_y_al_final_el_mensaje(self):
        # Pasos 5 y 6: al revés quedaría una republicación apuntando a nada.
        llamadas = []

        def registrando(nombre, original):
            def envoltorio(*args, **kwargs):
                llamadas.append(nombre)
                return original(*args, **kwargs)
            return envoltorio

        with patch.object(
            self.repo_republicaciones, "eliminar_por_mensaje",
            side_effect=registrando("republicaciones", self.repo_republicaciones.eliminar_por_mensaje),
        ), patch.object(
            self.repo_elementos, "eliminar_de_mensaje",
            side_effect=registrando("elementos", self.repo_elementos.eliminar_de_mensaje),
        ), patch.object(
            self.repo_mensajes, "eliminar",
            side_effect=registrando("mensaje", self.repo_mensajes.eliminar),
        ):
            self.control.borrar(self.id_mensaje, self.ana)

        self.assertEqual(llamadas, ["republicaciones", "elementos", "mensaje"])

    # --- ca 6.1 y ca 6.2: se verifica DENTRO de la operación (rnf 6.1) -------------

    def test_ca_6_1_si_el_mensaje_ya_no_existe_lanza_el_error_y_no_borra_nada(self):
        antes = (self.contadores(), contar(self.con, "republicaciones"))
        with self.assertRaises(MensajeInexistenteError):
            self.control.borrar(9999, self.ana)
        self.assertEqual((self.contadores(), contar(self.con, "republicaciones")), antes)

    def test_ca_6_2_quien_no_es_el_autor_no_borra_nada_aunque_mande_el_pedido_directo(self):
        antes = (self.contadores(), contar(self.con, "republicaciones"))
        with self.assertRaises(NoEsAutorError):
            self.control.borrar(self.id_mensaje, self.beto)
        self.assertEqual((self.contadores(), contar(self.con, "republicaciones")), antes)

    def test_borrar_dos_veces_la_segunda_es_ca_6_1(self):
        self.control.borrar(self.id_mensaje, self.ana)
        with self.assertRaises(MensajeInexistenteError):
            self.control.borrar(self.id_mensaje, self.ana)

    # --- rnf 6.3: todo o nada ------------------------------------------------------

    def test_si_falla_el_ultimo_paso_no_se_borra_nada(self):
        antes = (self.contadores(), contar(self.con, "republicaciones"))
        with patch.object(self.repo_mensajes, "eliminar", side_effect=RuntimeError("falla simulada")):
            with self.assertRaises(RuntimeError):
                self.control.borrar(self.id_mensaje, self.ana)
        # Se habían borrado las republicaciones y los elementos ANTES de la falla:
        # la transacción los tiene que haber devuelto.
        self.assertEqual((self.contadores(), contar(self.con, "republicaciones")), antes)
        self.assertTrue(self.repo_republicaciones.existe(self.id_beto, self.id_mensaje))
        self.assertFalse(self.con.in_transaction)

    def test_despues_de_un_fallo_se_puede_borrar(self):
        with patch.object(self.repo_mensajes, "eliminar", side_effect=RuntimeError("falla simulada")):
            with self.assertRaises(RuntimeError):
                self.control.borrar(self.id_mensaje, self.ana)
        self.control.borrar(self.id_mensaje, self.ana)
        self.assertIsNone(self.repo_mensajes.buscar_por_id(self.id_mensaje))


if __name__ == "__main__":
    unittest.main()