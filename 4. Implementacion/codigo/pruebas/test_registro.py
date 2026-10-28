"""Pruebas de CU0001 Registrar Usuario.

Primero el control (ControlRegistro con los repositorios de verdad sobre una base
temporal) y después la pantalla, a través de HTTP con el cliente de Flask.

Las fotos de estas pruebas se guardan en una carpeta temporal. En las pruebas por
HTTP nunca se sube una foto válida, porque se guardaría en la carpeta de fotos de la
aplicación de verdad.
"""

from __future__ import annotations

import os
import tempfile
import unittest
from io import BytesIO
from unittest.mock import patch

from werkzeug.security import check_password_hash

from miblog.acceso_datos.almacen_fotos import AlmacenFotos
from miblog.acceso_datos.conexion import obtener_conexion
from miblog.acceso_datos.repositorio_usuarios import RepositorioUsuarios
from miblog.logica.dominio.elementos import Mencion
from miblog.logica.dominio.errores import DatosInvalidosError, UsuarioDuplicadoError
from miblog.logica.gestion_mensajes.extractores import ExtractorMenciones
from miblog.logica.gestion_usuarios.control_registro import ControlRegistro, DatosRegistro

from pruebas.ayudas import PruebaConApp, PruebaConBase, contar

PNG = b"\x89PNG\r\n\x1a\n" + b"contenido de una imagen"
JPG = b"\xff\xd8\xff" + b"contenido de una imagen"

# Nombres que se pueden registrar y nombres que no (ca 1.1).
NOMBRES_VALIDOS = ["ana", "Ana_99", "juan.perez", "ana-lopez", "María", "ñandú", "_", "a.b-c", "7"]
NOMBRES_INVALIDOS = [
    "Ana Pérez", "ana!", "@ana", ".ana", "ana.", "-ana", "ana-", "a..b", "a--b", "a.-b", "a b",
]


def datos(**cambios) -> DatosRegistro:
    """Un formulario de registro completo y válido. Cada prueba cambia lo que necesita."""
    campos = dict(
        nombre_usuario="ana",
        email="ana@empresa.com",
        clave="clave1234",
        confirmacion_clave="clave1234",
        nombre_completo="Ana Pérez",
        descripcion=None,
        nombre_archivo_foto=None,
        contenido_foto=None,
    )
    campos.update(cambios)
    return DatosRegistro(**campos)


class PruebaControlRegistro(PruebaConBase):
    def setUp(self):
        super().setUp()
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.carpeta_fotos = carpeta.name
        self.control = ControlRegistro(RepositorioUsuarios(), AlmacenFotos(carpeta.name))

    def errores(self, formulario: DatosRegistro, control: ControlRegistro | None = None) -> dict:
        """Los errores por campo que lanza el registro de este formulario."""
        with self.assertRaises(DatosInvalidosError) as contexto:
            (control or self.control).registrar_usuario(formulario)
        return contexto.exception.errores_por_campo

    def fotos_guardadas(self) -> list[str]:
        return os.listdir(self.carpeta_fotos)

    # --- Curso normal ---------------------------------------------------------

    def test_curso_normal_crea_la_cuenta_activa_con_rol_empleado_y_fecha_de_alta(self):
        usuario = self.control.registrar_usuario(datos(descripcion="Hola"))
        fila = self.con.execute("SELECT * FROM usuarios WHERE id_usuario = ?",
                                (usuario.id_usuario,)).fetchone()
        self.assertEqual(fila["nombre_usuario"], "ana")
        self.assertEqual(fila["email"], "ana@empresa.com")
        self.assertEqual(fila["nombre_completo"], "Ana Pérez")
        self.assertEqual(fila["descripcion"], "Hola")
        self.assertEqual(fila["rol"], "EMPLEADO")
        self.assertEqual(fila["activo"], 1)
        self.assertTrue(fila["fecha_alta"])
        self.assertIsNone(fila["url_foto"])

    def test_se_recortan_los_espacios_de_los_extremos_y_la_descripcion_vacia_queda_nula(self):
        usuario = self.control.registrar_usuario(
            datos(nombre_usuario="  ana  ", email=" ana@empresa.com ", nombre_completo=" Ana ",
                  descripcion="   ")
        )
        self.assertEqual(usuario.nombre_usuario, "ana")
        self.assertEqual(usuario.email, "ana@empresa.com")
        self.assertEqual(usuario.nombre_completo, "Ana")
        self.assertIsNone(usuario.descripcion)

    def test_rnf_1_2_la_clave_se_guarda_con_hash_y_salt_nunca_en_texto_plano(self):
        self.control.registrar_usuario(datos())
        self.control.registrar_usuario(datos(nombre_usuario="beto", email="beto@empresa.com"))
        hashes = [f[0] for f in self.con.execute("SELECT clave_hash FROM usuarios ORDER BY id_usuario")]
        for guardado in hashes:
            self.assertNotIn("clave1234", guardado)
            self.assertTrue(check_password_hash(guardado, "clave1234"))
        self.assertNotEqual(hashes[0], hashes[1])  # misma clave, distinto hash: hay salt

    # --- ca 1.1: datos obligatorios incompletos o con formato inválido ---------

    def test_ca_1_1_los_campos_vacios_se_informan_campo_por_campo(self):
        errores = self.errores(datos(nombre_usuario="", email="", clave="", confirmacion_clave="",
                                     nombre_completo="   "))
        self.assertEqual(
            set(errores),
            {"nombre_usuario", "email", "clave", "confirmacion_clave", "nombre_completo"},
        )
        self.assertEqual(contar(self.con, "usuarios"), 0)

    def test_rnf_1_1_el_nombre_de_usuario_admite_hasta_15_caracteres(self):
        self.assertIn("nombre_usuario", self.errores(datos(nombre_usuario="a" * 16)))
        usuario = self.control.registrar_usuario(datos(nombre_usuario="a" * 15))
        self.assertEqual(len(usuario.nombre_usuario), 15)

    def test_ca_1_1_un_correo_mal_formado_se_rechaza(self):
        for correo in ["sin-arroba", "a@b", "a b@c.com", "@c.com", "a@@c.com"]:
            with self.subTest(correo=correo):
                self.assertIn("email", self.errores(datos(email=correo)))

    def test_rnf_1_1_la_clave_tiene_al_menos_8_caracteres_y_se_confirma(self):
        self.assertIn("clave", self.errores(datos(clave="1234567", confirmacion_clave="1234567")))
        self.assertIn("confirmacion_clave", self.errores(datos(confirmacion_clave="otra-clave-1")))
        self.control.registrar_usuario(datos(clave="12345678", confirmacion_clave="12345678"))

    def test_ca_1_1_el_nombre_de_usuario_solo_admite_lo_que_una_mencion_reconoce(self):
        for nombre in NOMBRES_INVALIDOS:
            with self.subTest(rechazado=nombre):
                self.assertIn("nombre_usuario", self.errores(datos(nombre_usuario=nombre)))
        self.assertEqual(contar(self.con, "usuarios"), 0)
        for posicion, nombre in enumerate(NOMBRES_VALIDOS):
            with self.subTest(aceptado=nombre):
                usuario = self.control.registrar_usuario(
                    datos(nombre_usuario=nombre, email=f"u{posicion}@empresa.com")
                )
                self.assertEqual(usuario.nombre_usuario, nombre)

    def test_todo_nombre_de_usuario_que_se_puede_registrar_se_puede_mencionar(self):
        # Ata la regla del registro con el ExtractorMenciones: si una cambia sin
        # la otra, esta prueba falla. Es el motivo de la regla.
        for nombre in NOMBRES_VALIDOS:
            with self.subTest(nombre=nombre):
                menciones = ExtractorMenciones().extraer(f"hola @{nombre} que tal")
                self.assertEqual(
                    [m.nombre_usuario_mencionado for m in menciones if isinstance(m, Mencion)],
                    [nombre],
                )
        # Y al revés: un nombre que no se puede registrar se mencionaría cortado.
        for nombre in NOMBRES_INVALIDOS:
            with self.subTest(nombre=nombre):
                menciones = ExtractorMenciones().extraer(f"hola @{nombre} que tal")
                self.assertNotEqual([m.nombre_usuario_mencionado for m in menciones], [nombre])

    # --- ca 1.2: nombre de usuario o correo en uso -------------------------------

    def test_ca_1_2_informa_cual_esta_en_uso_sin_distinguir_mayusculas(self):
        self.control.registrar_usuario(datos())
        casos = [
            (datos(nombre_usuario="ANA", email="otra@empresa.com"), ["nombre_usuario"]),
            (datos(nombre_usuario="otra", email="ANA@EMPRESA.COM"), ["email"]),
            (datos(), ["nombre_usuario", "email"]),
        ]
        for formulario, esperado in casos:
            with self.subTest(esperado=esperado):
                with self.assertRaises(UsuarioDuplicadoError) as contexto:
                    self.control.registrar_usuario(formulario)
                self.assertEqual(contexto.exception.campos, esperado)
        self.assertEqual(contar(self.con, "usuarios"), 1)

    # --- ca 1.3: foto de perfil ---------------------------------------------------

    def test_ca_1_3_una_foto_con_extension_firma_o_tamano_invalidos_se_rechaza(self):
        chico = ControlRegistro(RepositorioUsuarios(), AlmacenFotos(self.carpeta_fotos),
                                tamano_maximo_foto=100)
        casos = [
            (self.control, "foto.gif", PNG),             # extensión no admitida
            (self.control, "foto.png", JPG),             # dice PNG pero empieza como JPG
            (self.control, "foto.jpg", PNG),             # dice JPG pero empieza como PNG
            (self.control, "foto.png", b""),             # vacía
            (chico, "foto.png", PNG + b"0" * 100),       # más de 100 bytes
        ]
        for control, nombre, contenido in casos:
            with self.subTest(nombre=nombre, bytes=len(contenido)):
                errores = self.errores(
                    datos(nombre_archivo_foto=nombre, contenido_foto=contenido), control
                )
                self.assertEqual(list(errores), ["foto"])
        self.assertEqual(self.fotos_guardadas(), [])
        self.assertEqual(contar(self.con, "usuarios"), 0)

    def test_una_foto_valida_se_guarda_con_un_nombre_que_inventa_el_sistema(self):
        for posicion, (nombre, contenido, extension) in enumerate(
            [("Mi Foto.PNG", PNG, ".png"), ("otra.jpeg", JPG, ".jpeg"), ("x.jpg", JPG, ".jpg")]
        ):
            with self.subTest(nombre=nombre):
                usuario = self.control.registrar_usuario(datos(
                    nombre_usuario=f"u{posicion}", email=f"u{posicion}@empresa.com",
                    nombre_archivo_foto=nombre, contenido_foto=contenido))
                self.assertTrue(usuario.url_foto.endswith(extension))
                self.assertNotIn(nombre, usuario.url_foto)
                with open(os.path.join(self.carpeta_fotos, usuario.url_foto), "rb") as archivo:
                    self.assertEqual(archivo.read(), contenido)

    def test_rnf_1_3_si_falla_el_alta_no_queda_ni_la_cuenta_ni_la_foto(self):
        with patch.object(RepositorioUsuarios, "crear", side_effect=RuntimeError("falla")):
            with self.assertRaises(RuntimeError):
                self.control.registrar_usuario(
                    datos(nombre_archivo_foto="foto.png", contenido_foto=PNG)
                )
        self.assertEqual(contar(self.con, "usuarios"), 0)
        self.assertEqual(self.fotos_guardadas(), [])  # la acción compensatoria borró el archivo


class PruebaWebRegistro(PruebaConApp):
    FORMULARIO = {
        "nombre_usuario": "ana",
        "email": "ana@empresa.com",
        "clave": "clave1234",
        "confirmacion_clave": "clave1234",
        "nombre_completo": "Ana Pérez",
    }

    def registrar(self, cliente=None, **cambios):
        formulario = dict(self.FORMULARIO, **cambios)
        return (cliente or self.app.test_client()).post("/registro", data=formulario)

    def filas(self, tabla):
        with self.app.app_context():
            return contar(obtener_conexion(), tabla)

    def test_el_formulario_pide_la_clave_enmascarada_y_explica_el_formato_del_usuario(self):
        html = self.app.test_client().get("/registro").get_data(as_text=True)
        self.assertEqual(html.count('type="password"'), 2)
        self.assertIn("Puntos y guiones, solo en el medio", html)
        self.assertIn('enctype="multipart/form-data"', html)  # sin esto no llega la foto

    def test_ca_1_4_cancelar_es_un_enlace_a_la_pantalla_inicial(self):
        html = self.app.test_client().get("/registro").get_data(as_text=True)
        self.assertRegex(html, r'<a class="boton boton--secundario" href="/">Cancelar</a>')

    def test_curso_normal_informa_el_alta_y_despues_se_puede_iniciar_sesion(self):
        respuesta = self.registrar()
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("Cuenta creada", respuesta.get_data(as_text=True))
        self.assertEqual(self.filas("usuarios"), 1)

        entrada = self.app.test_client().post(
            "/sesion/iniciar", data={"nombre_usuario": "ana", "clave": "clave1234"}
        )
        self.assertEqual(entrada.status_code, 302)
        self.assertTrue(entrada.headers["Location"].endswith("/tablon"))

    def test_ca_1_1_vuelve_al_formulario_con_los_datos_menos_la_clave(self):
        respuesta = self.registrar(nombre_usuario="Ana Pérez", clave="clave-secreta-1",
                                   confirmacion_clave="clave-secreta-1", descripcion="Una frase")
        html = respuesta.get_data(as_text=True)
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("Usá solo letras, números y guion bajo.", html)
        self.assertIn('value="ana@empresa.com"', html)   # se conserva lo escrito
        self.assertIn("Una frase", html)
        self.assertNotIn("clave-secreta-1", html)        # la clave nunca vuelve
        self.assertEqual(self.filas("usuarios"), 0)

    def test_ca_1_2_dice_cual_de_los_dos_esta_en_uso(self):
        self.registrar()
        self.assertIn("Ese nombre de usuario ya está en uso.",
                      self.registrar(email="otro@empresa.com").get_data(as_text=True))
        html = self.registrar(nombre_usuario="otro").get_data(as_text=True)
        self.assertIn("Ese correo electrónico ya está en uso.", html)
        self.assertNotIn("Ese nombre de usuario ya está en uso.", html)
        self.assertEqual(self.filas("usuarios"), 1)

    def test_ca_1_3_una_foto_que_no_sirve_se_informa_y_no_se_guarda_nada(self):
        respuesta = self.app.test_client().post(
            "/registro",
            data=dict(self.FORMULARIO, foto=(BytesIO(b"no soy una imagen"), "foto.png")),
            content_type="multipart/form-data",
        )
        self.assertIn("La foto tiene que ser PNG o JPG y pesar hasta 2 MB.",
                      respuesta.get_data(as_text=True))
        self.assertEqual(self.filas("usuarios"), 0)


if __name__ == "__main__":
    unittest.main()