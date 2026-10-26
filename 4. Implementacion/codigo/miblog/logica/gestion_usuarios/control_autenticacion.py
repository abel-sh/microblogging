"""ControlAutenticacion: realiza CU0002 Iniciar Sesión y CU0003 Cerrar Sesión, 
y responde a GuardiaSesion si hay una sesión vigente.

No toca flask.session ni la cookie: devuelve o recibe el token, y la vista es
la que lo guarda o lo lee. Por eso este control también serviría para la API.

La sesión es una fila de la tabla sesiones (hallazgo H1): el token viaja en la
cookie y en la base queda solo su hash SHA-256.
"""

from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from werkzeug.security import check_password_hash, generate_password_hash

from miblog.acceso_datos.repositorio_sesiones import RepositorioSesiones
from miblog.acceso_datos.repositorio_usuarios import RepositorioUsuarios
from miblog.logica.dominio.errores import CredencialesInvalidasError, DatosInvalidosError
from miblog.logica.dominio.usuario import Usuario


def _ahora() -> datetime:
    return datetime.now(timezone.utc)


def _hash_de(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


class ControlAutenticacion:
    def __init__(
        self,
        repo_usuarios: RepositorioUsuarios,
        repo_sesiones: RepositorioSesiones,
        duracion_sesion: timedelta,
    ) -> None:
        self._repo_usuarios = repo_usuarios
        self._repo_sesiones = repo_sesiones
        self._duracion_sesion = duracion_sesion
        # Hash de una clave al azar que nadie conoce. Se usa cuando el usuario
        # no existe, para que la respuesta tarde lo mismo que con un usuario real.
        self._hash_ficticio = generate_password_hash(secrets.token_hex(16))

    # --- CU0002 ---------------------------------------------------------

    def autenticar(self, nombre_usuario: str, clave: str) -> str:
        """Verifica las credenciales, abre la sesión y devuelve el token."""
        self._validar_campos(nombre_usuario, clave)
        usuario = self._repo_usuarios.buscar_activo_por_nombre_usuario(nombre_usuario.strip())
        if not self._verificar_clave(usuario, clave):
            raise CredencialesInvalidasError()
        return self._abrir_sesion(usuario)

    def _validar_campos(self, nombre_usuario: str, clave: str) -> None:
        errores: dict[str, str] = {}
        if not nombre_usuario.strip():
            errores["nombre_usuario"] = "Ingresá tu nombre de usuario."
        if not clave:
            errores["clave"] = "Ingresá tu clave."
        if errores:
            raise DatosInvalidosError(errores)

    def _verificar_clave(self, usuario: Usuario | None, clave: str) -> bool:
        # Siempre se hace una comparación, exista o no el usuario.
        hash_a_comparar = usuario.clave_hash if usuario is not None else self._hash_ficticio
        coincide = check_password_hash(hash_a_comparar, clave)
        return usuario is not None and coincide

    def _abrir_sesion(self, usuario: Usuario) -> str:
        ahora = _ahora()
        # Limpieza general: incluye las sesiones abandonadas, que nadie vuelve a validar.
        self._repo_sesiones.eliminar_vencidas(ahora)
        token = secrets.token_urlsafe(32)
        self._repo_sesiones.crear(_hash_de(token), usuario.id_usuario, ahora + self._duracion_sesion)
        return token

    # --- CU0003 ---------------------------------------------------------

    def cerrar_sesion(self, token: str | None) -> None:
        """Invalida la sesión en el servidor. Sin token, no hace nada y no falla (ca 3.1)."""
        if token:
            self._invalidar_sesion(token)

    def _invalidar_sesion(self, token: str) -> int:
        return self._repo_sesiones.eliminar(_hash_de(token))

    # --- Para GuardiaSesion ---------------------------------------------

    def obtener_usuario_en_sesion(self, token: str | None) -> Usuario | None:
        """El Usuario dueño de ese token, o None si no hay sesión vigente."""
        if not token:
            return None
        hash_token = _hash_de(token)
        ahora = _ahora()
        usuario = self._repo_sesiones.buscar_usuario_vigente(hash_token, ahora)
        if usuario is None:
            # Si la fila existe pero venció, se borra ahora (limpieza al validar).
            self._repo_sesiones.eliminar_si_vencida(hash_token, ahora)
        return usuario