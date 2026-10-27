"""Vista de CU0004 (Publicar Mensaje) y CU0009 (Visualizar Tablón).

Las dos ocurren en la misma pantalla: arriba el formulario para publicar y abajo
el listado del tablón. Por eso las dos rutas las atiende una sola clase,
VistaTablon.

Cada método atiende una ruta de Flask: lee la petición, llama a un control, y
elige la plantilla o la redirección. Ninguna regla de negocio vive acá, y esta
capa nunca llega directo a la base de datos.

Las dos rutas pasan por GuardiaSesion (se registran en crear_app), así que
cuando estos métodos corren, g.usuario ya tiene al Usuario de la sesión.
"""

from __future__ import annotations

from datetime import datetime

from flask import flash, g, redirect, render_template, request, session, url_for

from miblog.logica.dominio.errores import TextoExcedidoError, TextoVacioError
from miblog.logica.gestion_mensajes.control_publicacion import ControlPublicacion
from miblog.logica.gestion_mensajes.control_tablon import ControlTablon
from miblog.logica.gestion_mensajes.operaciones_mensaje import OperacionSobreMensaje


def formatear_fecha(fecha: datetime) -> str:
    """Una fecha lista para mostrar, en la hora local de esta computadora.

    Las fechas se guardan en UTC; acá se convierten solo para mostrarlas. crear_app
    registra esta función como filtro de las plantillas, con el nombre "fecha".
    """
    return fecha.astimezone().strftime("%d/%m/%Y %H:%M")


class VistaTablon:
    def __init__(
        self,
        control_tablon: ControlTablon,
        control_publicacion: ControlPublicacion,
    ) -> None:
        self._control_tablon = control_tablon
        self._control_publicacion = control_publicacion

    def mostrar(self):
        """GET /tablon"""
        # ca 4.3: si la sesión expiró mientras el usuario escribía, GuardiaSesion guardó
        # el texto en la sesión y CU0002 lo conservó al iniciar sesión de nuevo. Se saca
        # de la sesión (pop) para que aparezca una sola vez.
        borrador = session.pop("borrador", "")
        return self._pagina(borrador)

    def publicar(self):
        """POST /mensajes"""
        texto = request.form.get("texto", "")
        try:
            self._control_publicacion.publicar(g.usuario, texto)
        except TextoVacioError as error:  # ca 4.1
            flash(error.mensaje, "error")
            return self._pagina(texto)
        except TextoExcedidoError as error:  # ca 4.2
            flash(
                f"{error.mensaje} El máximo es de {OperacionSobreMensaje.LIMITE} caracteres.",
                "error",
            )
            return self._pagina(texto)
        # Post/Redirect/Get: si el usuario recarga la página después de publicar, el
        # navegador no vuelve a enviar el mensaje.
        return redirect(url_for("tablon"))

    def _pagina(self, texto: str):
        """El tablón con el campo de redacción relleno con `texto`.

        Cuando hubo un error el texto vuelve completo, tal como se escribió y sin
        recortar (ca 4.2), para que el usuario lo corrija en vez de reescribirlo.
        """
        elementos = self._control_tablon.obtener_tablon(g.usuario)
        return render_template(
            "tablon.html",
            elementos=elementos,
            texto=texto,
            limite=OperacionSobreMensaje.LIMITE,
        )