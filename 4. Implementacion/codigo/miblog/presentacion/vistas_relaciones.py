"""Vista de CU0014 (Buscar Usuarios) y CU0011 (Seguir Usuario).

Cada método atiende una ruta de Flask: lee la petición, llama a un control, y
elige la plantilla o la redirección. Ninguna regla de negocio vive acá, y esta
capa nunca llega directo a la base de datos.

Las dos rutas pasan por GuardiaSesion (se registran en crear_app), así que
cuando estos métodos corren, g.usuario ya tiene al Usuario de la sesión.
"""

from __future__ import annotations

from flask import flash, g, redirect, render_template, request, url_for

from miblog.logica.dominio.errores import (
    AutoSeguimientoError,
    CriterioVacioError,
    SeguimientoExistenteError,
    UsuarioInexistenteError,
)
from miblog.logica.gestion_relaciones.control_busqueda_usuarios import ControlBusquedaUsuarios
from miblog.logica.gestion_relaciones.control_seguimiento import ControlSeguimiento


class VistaBusquedaUsuarios:
    def __init__(
        self,
        control_busqueda: ControlBusquedaUsuarios,
        control_seguimiento: ControlSeguimiento,
    ) -> None:
        self._control_busqueda = control_busqueda
        self._control_seguimiento = control_seguimiento

    def buscar(self):
        """GET /usuarios/buscar?criterio=..."""
        criterio = request.args.get("criterio")
        # Primera visita: la URL no trae el parámetro. Solo se muestra el formulario
        # y no se llama al control (DISEÑO §6.10).
        if criterio is None:
            return render_template("busqueda.html", criterio="", resultados=None)
        try:
            resultados = self._control_busqueda.buscar(criterio, g.usuario)
        except CriterioVacioError as error:  # ca 14.1
            flash(error.mensaje, "error")
            return render_template("busqueda.html", criterio=criterio, resultados=None)
        # resultados puede ser una lista vacía (ca 14.2): la plantilla distingue
        # "no se buscó" (None) de "se buscó y no hay nada" ([]).
        return render_template("busqueda.html", criterio=criterio, resultados=resultados)

    def seguir(self, id_seguido: int):
        """POST /usuarios/<int:id_seguido>/seguir"""
        criterio = request.form.get("criterio", "")
        try:
            self._control_seguimiento.seguir(g.usuario, id_seguido)
        except SeguimientoExistenteError:
            # ca 11.3: no hay nada que avisar. Al volver a la búsqueda, ese resultado
            # ya aparece como "Siguiendo" (sin botón: dejar de seguir es CU0012).
            pass
        except (UsuarioInexistenteError, AutoSeguimientoError) as error:  # ca 11.1, ca 11.2
            flash(error.mensaje, "error")
        return self._volver_a_la_busqueda(criterio)

    def _volver_a_la_busqueda(self, criterio: str):
        """Post/Redirect/Get: vuelve a la búsqueda conservando el criterio.

        Si el criterio vino vacío (alguien mandó el POST a mano), vuelve al
        formulario limpio: no tiene sentido disparar una búsqueda que daría error.
        """
        if criterio.strip():
            return redirect(url_for("buscar_usuarios", criterio=criterio))
        return redirect(url_for("buscar_usuarios"))