"""GuardiaSesion: exige sesión antes de cada ruta protegida.

Vive en presentación porque trabaja con la petición HTTP (la cookie, g, los
redireccionamientos). La decisión de si la sesión vale la toma
ControlAutenticacion.
"""

from __future__ import annotations

import functools
from typing import Callable

from flask import flash, g, redirect, request, session

from miblog.logica.gestion_usuarios.control_autenticacion import ControlAutenticacion


class GuardiaSesion:
    def __init__(self, control_autenticacion: ControlAutenticacion) -> None:
        self._control_autenticacion = control_autenticacion

    def requiere_sesion(self, vista: Callable, conservar_borrador: bool = False) -> Callable:
        """Envuelve una vista: si hay sesión vigente deja al usuario en g.usuario y la
        ejecuta; si no, redirige al inicio de sesión.

        conservar_borrador=True es solo para la ruta de publicar (ca 4.3): guarda
        en la sesión el texto que el usuario estaba escribiendo.
        """

        @functools.wraps(vista)
        def vista_protegida(*args, **kwargs):
            usuario = self._control_autenticacion.obtener_usuario_en_sesion(session.get("token"))
            if usuario is None:
                if conservar_borrador:
                    session["borrador"] = request.form.get("texto", "")
                flash("Tu sesión expiró. Volvé a iniciar sesión.", "error")
                return redirect("/")
            g.usuario = usuario
            return vista(*args, **kwargs)

        return vista_protegida