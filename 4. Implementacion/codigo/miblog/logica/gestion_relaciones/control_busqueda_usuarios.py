"""ControlBusquedaUsuarios: realiza CU0014 Buscar Usuarios.

No sabe de HTTP: recibe el criterio ya leído por la vista y devuelve una lista de
ResultadoBusqueda, o lanza CriterioVacioError (ca 14.1). "Sin resultados" (ca 14.2)
no es un error: es una lista vacía.

Solo lee, así que no abre transacción.
"""

from __future__ import annotations

from dataclasses import dataclass

from miblog.acceso_datos.repositorio_seguimientos import RepositorioSeguimientos
from miblog.acceso_datos.repositorio_usuarios import RepositorioUsuarios
from miblog.logica.dominio.errores import CriterioVacioError
from miblog.logica.dominio.usuario import Usuario


@dataclass
class ResultadoBusqueda:
    """Lo que la pantalla puede mostrar de cada usuario encontrado.

    No tiene campo `email`, a propósito: la vista no puede mostrar el correo
    aunque quiera, porque el dato nunca le llega (rnf 14.2). Tampoco lleva
    `descripcion`: el diseño no la incluye en los resultados.
    """

    id_usuario: int
    nombre_usuario: str
    nombre_completo: str
    url_foto: str | None
    lo_sigue: bool


class ControlBusquedaUsuarios:
    def __init__(
        self,
        repo_usuarios: RepositorioUsuarios,
        repo_seguimientos: RepositorioSeguimientos,
    ) -> None:
        self._repo_usuarios = repo_usuarios
        self._repo_seguimientos = repo_seguimientos

    def buscar(self, criterio: str, usuario: Usuario) -> list[ResultadoBusqueda]:
        """Cuentas activas que coinciden con el criterio, marcando a las que `usuario` ya sigue."""
        criterio_limpio = self._validar_criterio(criterio)
        encontrados = self._repo_usuarios.buscar_activos_por_criterio(criterio_limpio)
        ids_seguidos = self._repo_seguimientos.buscar_ids_seguidos_de(usuario.id_usuario)
        return self._marcar_seguidos(encontrados, ids_seguidos)

    def _validar_criterio(self, criterio: str) -> str:
        """ca 14.1: un criterio vacío o de solo espacios se rechaza antes de buscar."""
        criterio_limpio = criterio.strip()
        if not criterio_limpio:
            raise CriterioVacioError()
        return criterio_limpio

    def _marcar_seguidos(
        self, usuarios: list[Usuario], ids_seguidos: set[int]
    ) -> list[ResultadoBusqueda]:
        """Convierte cada Usuario en un ResultadoBusqueda, sin el correo, con lo_sigue."""
        return [
            ResultadoBusqueda(
                id_usuario=u.id_usuario,
                nombre_usuario=u.nombre_usuario,
                nombre_completo=u.nombre_completo,
                url_foto=u.url_foto,
                lo_sigue=u.id_usuario in ids_seguidos,
            )
            for u in usuarios
        ]