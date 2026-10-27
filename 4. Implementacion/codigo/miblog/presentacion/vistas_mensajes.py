"""Vistas de CU0004 (Publicar), CU0005 (Editar), CU0006 (Borrar), CU0007 (Republicar)
y CU0009 (Visualizar Tablón).

Son tres clases:

  - VistaTablon: el tablón con su formulario para publicar, y el botón Republicar.
  - DialogoEdicionMensaje: el diálogo para editar un mensaje propio.
  - DialogoConfirmacionBorrado: el diálogo para confirmar el borrado de un mensaje propio.

Los dos diálogos son páginas propias, cada una con su ruta (hallazgo H9): sin
JavaScript no hay ventanas flotantes. El aspecto de recuadro centrado sobre fondo
oscurecido lo da la hoja de estilos, y "Cancelar" es un simple enlace al tablón,
así que no llega ninguna petición a la lógica (ca 5.4, ca 6.3).

Cada método atiende una ruta de Flask: lee la petición, llama a un control, y
elige la plantilla o la redirección. Ninguna regla de negocio vive acá, y esta
capa nunca llega directo a la base de datos.

Todas las rutas pasan por GuardiaSesion (se registran en crear_app), así que
cuando estos métodos corren, g.usuario ya tiene al Usuario de la sesión.
"""

from __future__ import annotations

from datetime import datetime

from flask import flash, g, redirect, render_template, request, session, url_for

from miblog.logica.dominio.errores import (
    AutorNoSeguidoError,
    MensajeInexistenteError,
    MensajePropioError,
    NoEsAutorError,
    RepublicacionExistenteError,
    TextoExcedidoError,
    TextoVacioError,
)
from miblog.logica.gestion_mensajes.control_publicacion import ControlPublicacion
from miblog.logica.gestion_mensajes.control_republicacion import ControlRepublicacion
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
        control_republicacion: ControlRepublicacion,
    ) -> None:
        self._control_tablon = control_tablon
        self._control_publicacion = control_publicacion
        self._control_republicacion = control_republicacion

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

    def republicar(self, id_mensaje: int):
        """POST /mensajes/<int:id_mensaje>/republicar"""
        try:
            self._control_republicacion.republicar(g.usuario, id_mensaje)
        except (
            MensajeInexistenteError,  # ca 7.4
            MensajePropioError,  # ca 7.2
            AutorNoSeguidoError,  # ca 7.1
            RepublicacionExistenteError,  # ca 7.3: solo informa, no ofrece deshacer.
        ) as error:
            flash(error.mensaje, "error")
        # Con o sin error se vuelve al tablón. Si salió bien, la republicación ya
        # aparece arriba de todo, con el autor original y quien republicó (paso 5).
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


class DialogoEdicionMensaje:
    def __init__(self, control_publicacion: ControlPublicacion) -> None:
        self._control_publicacion = control_publicacion

    def abrir(self, id_mensaje: int):
        """GET /mensajes/<int:id_mensaje>/editar

        Abrir el diálogo ES pedir su página, así que la autoría se verifica acá
        (paso 2 de CU0005). Se vuelve a verificar al confirmar.
        """
        try:
            mensaje = self._control_publicacion.verificar_autoria(id_mensaje, g.usuario)
        except (MensajeInexistenteError, NoEsAutorError) as error:  # ca 5.1, ca 5.2
            flash(error.mensaje, "error")
            return redirect(url_for("tablon"))
        return self._pagina(id_mensaje, mensaje.texto)

    def confirmar(self, id_mensaje: int):
        """POST /mensajes/<int:id_mensaje>/editar"""
        texto = request.form.get("texto", "")
        try:
            self._control_publicacion.editar(id_mensaje, g.usuario, texto)
        except (MensajeInexistenteError, NoEsAutorError) as error:  # ca 5.1, ca 5.2
            flash(error.mensaje, "error")
            return redirect(url_for("tablon"))
        except TextoVacioError as error:  # ca 5.3
            flash(error.mensaje, "error")
            return self._pagina(id_mensaje, texto)
        except TextoExcedidoError as error:  # ca 5.3
            flash(
                f"{error.mensaje} El máximo es de {OperacionSobreMensaje.LIMITE} caracteres.",
                "error",
            )
            return self._pagina(id_mensaje, texto)
        # Post/Redirect/Get (paso 8): el mensaje editado ya se ve en el tablón.
        return redirect(url_for("tablon"))

    def _pagina(self, id_mensaje: int, texto: str):
        """El diálogo con el campo relleno con `texto`.

        Al abrirlo, `texto` es el del mensaje. Si hubo un error (ca 5.3) vuelve el que
        el usuario escribió, completo y sin recortar, para que lo corrija; el mensaje
        guardado sigue intacto.
        """
        return render_template(
            "dialogo_edicion.html",
            id_mensaje=id_mensaje,
            texto=texto,
            limite=OperacionSobreMensaje.LIMITE,
        )


class DialogoConfirmacionBorrado:
    def __init__(self, control_publicacion: ControlPublicacion) -> None:
        self._control_publicacion = control_publicacion

    def solicitar_confirmacion(self, id_mensaje: int):
        """GET /mensajes/<int:id_mensaje>/borrar

        Igual que en la edición, abrir el diálogo ES pedir su página: la autoría se
        verifica acá (paso 2 de CU0006).
        """
        try:
            mensaje = self._control_publicacion.verificar_autoria(id_mensaje, g.usuario)
        except MensajeInexistenteError:
            # ca 6.1: el mensaje ya se borró. El objetivo del usuario ya está cumplido,
            # así que se actualiza la vista SIN informar ningún error.
            return redirect(url_for("tablon"))
        except NoEsAutorError as error:  # ca 6.2
            flash(error.mensaje, "error")
            return redirect(url_for("tablon"))
        return render_template(
            "dialogo_borrado.html", id_mensaje=id_mensaje, texto=mensaje.texto
        )

    def confirmar(self, id_mensaje: int):
        """POST /mensajes/<int:id_mensaje>/borrar"""
        try:
            self._control_publicacion.borrar(id_mensaje, g.usuario)
        except MensajeInexistenteError:
            pass  # ca 6.1: sin aviso, como al abrir el diálogo
        except NoEsAutorError as error:  # ca 6.2
            flash(error.mensaje, "error")
        # Post/Redirect/Get (paso 7): el mensaje y sus republicaciones ya no están.
        return redirect(url_for("tablon"))