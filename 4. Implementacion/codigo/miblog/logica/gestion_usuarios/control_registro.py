"""ControlRegistro: realiza CU0001 Registrar Usuario.

No sabe de HTTP: recibe un DatosRegistro ya armado por la vista y devuelve el
Usuario creado, o lanza un error de negocio que la vista sabe mostrar.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from werkzeug.security import generate_password_hash

from miblog.acceso_datos.almacen_fotos import AlmacenFotos
from miblog.acceso_datos.conexion import transaccion
from miblog.acceso_datos.repositorio_usuarios import RepositorioUsuarios
from miblog.logica.dominio.errores import DatosInvalidosError, UsuarioDuplicadoError
from miblog.logica.dominio.usuario import Usuario


@dataclass
class DatosRegistro:
    """Los siete campos del formulario viajando juntos entre la vista y el control."""

    nombre_usuario: str
    email: str
    clave: str
    confirmacion_clave: str
    nombre_completo: str
    descripcion: str | None
    nombre_archivo_foto: str | None
    contenido_foto: bytes | None


class ControlRegistro:
    LIMITE_NOMBRE_USUARIO = 15
    LONGITUD_MINIMA_CLAVE = 8

    # Fotos de perfil (ca 1.3): extensiones admitidas y cómo tiene que empezar
    # el archivo de cada una. La extensión sola no alcanza: un "foto.png" puede
    # ser cualquier cosa renombrada.
    _FIRMAS_FOTO = {
        "png": (b"\x89PNG\r\n\x1a\n",),
        "jpg": (b"\xff\xd8\xff",),
        "jpeg": (b"\xff\xd8\xff",),
    }
    _PATRON_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    # Forma del nombre de usuario (ca 1.1): letras, números y "_", y además "." o "-"
    # pero solo EN EL MEDIO ("juan.perez", "ana-lopez"). Es la misma forma que reconoce
    # ExtractorMenciones: todo nombre que se puede registrar se puede mencionar
    # con @. Si una cambia, la otra también (hay una prueba que las ata).
    _PATRON_NOMBRE_USUARIO = re.compile(r"\w+(?:[.\-]\w+)*")

    def __init__(
        self,
        repo_usuarios: RepositorioUsuarios,
        almacen_fotos: AlmacenFotos,
        tamano_maximo_foto: int = 2 * 1024 * 1024,
    ) -> None:
        self._repo_usuarios = repo_usuarios
        self._almacen_fotos = almacen_fotos
        self._tamano_maximo_foto = tamano_maximo_foto

    def registrar_usuario(self, datos: DatosRegistro) -> Usuario:
        # 1. Validar todo antes de escribir nada (la foto también).
        self._validar_datos(datos)

        nombre_usuario = datos.nombre_usuario.strip()
        email = datos.email.strip()

        # 2. Unicidad.
        self._verificar_unicidad(nombre_usuario, email)

        # 3. Cifrar la clave y, si hay foto, guardar el archivo.
        clave_hash = self._cifrar_clave(datos.clave)
        nombre_foto = None
        try:
            if datos.nombre_archivo_foto:
                extension = datos.nombre_archivo_foto.rsplit(".", 1)[-1].lower()
                nombre_foto = self._almacen_fotos.guardar(datos.contenido_foto, extension)

            # 4. Crear el usuario dentro de una transacción.
            with transaccion():
                usuario = Usuario(
                    nombre_usuario=nombre_usuario,
                    email=email,
                    clave_hash=clave_hash,
                    nombre_completo=datos.nombre_completo.strip(),
                    descripcion=(datos.descripcion or "").strip() or None,
                    url_foto=nombre_foto,
                )
                usuario.id_usuario = self._repo_usuarios.crear(usuario)
        except BaseException:
            # Acción compensatoria: un archivo no entra en una transacción de
            # SQLite, así que si la fila no quedó, se borra el archivo a mano.
            if nombre_foto is not None:
                self._almacen_fotos.eliminar(nombre_foto)
            raise
        return usuario

    def _validar_datos(self, datos: DatosRegistro) -> None:
        errores: dict[str, str] = {}

        nombre_usuario = datos.nombre_usuario.strip()
        if not nombre_usuario:
            errores["nombre_usuario"] = "Ingresá un nombre de usuario."
        elif len(nombre_usuario) > self.LIMITE_NOMBRE_USUARIO:
            errores["nombre_usuario"] = (
                f"El nombre de usuario puede tener hasta {self.LIMITE_NOMBRE_USUARIO} caracteres."
            )
        elif not self._PATRON_NOMBRE_USUARIO.fullmatch(nombre_usuario):
            errores["nombre_usuario"] = (
                "Usá solo letras, números y guion bajo. Los puntos y guiones se admiten "
                "únicamente en el medio."
            )

        email = datos.email.strip()
        if not email:
            errores["email"] = "Ingresá tu correo electrónico."
        elif not self._PATRON_EMAIL.match(email):
            errores["email"] = "El correo electrónico no tiene un formato válido."

        if not datos.clave:
            errores["clave"] = "Ingresá una clave."
        elif len(datos.clave) < self.LONGITUD_MINIMA_CLAVE:
            errores["clave"] = (
                f"La clave tiene que tener al menos {self.LONGITUD_MINIMA_CLAVE} caracteres."
            )

        if not datos.confirmacion_clave:
            errores["confirmacion_clave"] = "Repetí la clave."
        elif datos.clave != datos.confirmacion_clave:
            errores["confirmacion_clave"] = "Las dos claves no coinciden."

        if not datos.nombre_completo.strip():
            errores["nombre_completo"] = "Ingresá tu nombre completo."

        if datos.nombre_archivo_foto:
            error_foto = self._validar_foto(datos.nombre_archivo_foto, datos.contenido_foto)
            if error_foto:
                errores["foto"] = error_foto

        if errores:
            raise DatosInvalidosError(errores)

    def _validar_foto(self, nombre_archivo: str, contenido: bytes | None) -> str | None:
        """Devuelve el texto del error, o None si la foto sirve."""
        extension = nombre_archivo.rsplit(".", 1)[-1].lower() if "." in nombre_archivo else ""
        mensaje = (
            "La foto tiene que ser PNG o JPG y pesar hasta "
            f"{self._tamano_maximo_foto // (1024 * 1024)} MB."
        )
        if extension not in self._FIRMAS_FOTO:
            return mensaje
        if not contenido or len(contenido) > self._tamano_maximo_foto:
            return mensaje
        if not contenido.startswith(self._FIRMAS_FOTO[extension]):
            return mensaje
        return None

    def _verificar_unicidad(self, nombre_usuario: str, email: str) -> None:
        en_uso = []
        if self._repo_usuarios.existe_nombre_usuario(nombre_usuario):
            en_uso.append("nombre_usuario")
        if self._repo_usuarios.existe_email(email):
            en_uso.append("email")
        if en_uso:
            raise UsuarioDuplicadoError(en_uso)

    def _cifrar_clave(self, clave: str) -> str:
        # Hash con salt. La clave en texto plano no se guarda ni se escribe en ningún log.
        return generate_password_hash(clave)