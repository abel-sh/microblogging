"""ControlSeguimiento: realiza CU0011 Seguir Usuario.

No sabe de HTTP. Recibe quién sigue (el Usuario de la sesión) y a quién (un id,
porque viene en la URL), y o registra el seguimiento o lanza el error de negocio
del curso alternativo que corresponda.

Abre una transacción: "verificar que no existe" y "crear" tienen que quedar bajo
el mismo bloqueo, para que dos clics casi simultáneos no pasen los dos la
verificación (Transacciones; ca 11.3).
"""

from __future__ import annotations

from datetime import datetime, timezone

from miblog.acceso_datos.conexion import transaccion
from miblog.acceso_datos.repositorio_seguimientos import RepositorioSeguimientos
from miblog.acceso_datos.repositorio_usuarios import RepositorioUsuarios
from miblog.logica.dominio.errores import (
    AutoSeguimientoError,
    SeguimientoExistenteError,
    UsuarioInexistenteError,
)
from miblog.logica.dominio.seguimiento import Seguimiento
from miblog.logica.dominio.usuario import Usuario


class ControlSeguimiento:
    def __init__(
        self,
        repo_usuarios: RepositorioUsuarios,
        repo_seguimientos: RepositorioSeguimientos,
    ) -> None:
        self._repo_usuarios = repo_usuarios
        self._repo_seguimientos = repo_seguimientos

    def seguir(self, usuario: Usuario, id_seguido: int) -> None:
        """Registra que `usuario` sigue a `id_seguido`, o lanza el error del curso alternativo."""
        with transaccion():
            # Paso 2 (ca 11.1): la cuenta a seguir existe y está activa.
            if self._repo_usuarios.buscar_activo_por_id(id_seguido) is None:
                raise UsuarioInexistenteError()
            # Paso 3 (ca 11.2).
            self._verificar_no_es_el_mismo(usuario, id_seguido)
            # Paso 4 (ca 11.3).
            self._verificar_no_existe(usuario, id_seguido)
            # Paso 5: se registra con su fecha de inicio (rnf 11.1, rnf 11.2).
            seguimiento = Seguimiento(
                id_seguidor=usuario.id_usuario,
                id_seguido=id_seguido,
                fecha_inicio=datetime.now(timezone.utc),
            )
            self._repo_seguimientos.crear(seguimiento)

    def _verificar_no_es_el_mismo(self, usuario: Usuario, id_seguido: int) -> None:
        if usuario.id_usuario == id_seguido:
            raise AutoSeguimientoError()

    def _verificar_no_existe(self, usuario: Usuario, id_seguido: int) -> None:
        if self._repo_seguimientos.existe(usuario.id_usuario, id_seguido):
            raise SeguimientoExistenteError()