"""Manejo de errores y registro de eventos (RNF16 y RNF24).

La idea. Hay dos clases de error y se tratan distinto:

* Los esperados son los cursos alternativos (un texto vacío, una clave incorrecta,
  un usuario que no existe). La lógica los lanza como ErrorDeNegocio, cada vista los
  captura y los muestra con flash(). Esos no llegan nunca a este módulo.
* Los inesperados son fallas: un error de programación, un archivo que no se puede
  escribir, una página que no existe. Esos sí llegan acá. Quedan anotados en el
  archivo de registro, con fecha y hora, y la persona ve una página con un texto
  genérico: nunca el detalle técnico.

Este módulo hace dos cosas: configurar_registro() prepara el archivo de registro y
registrar_manejadores_de_error() le enseña a Flask qué página mostrar en cada caso.
Las dos las llama crear_app().
"""

from __future__ import annotations

import logging

from flask import Flask, current_app, render_template, request
from werkzeug.exceptions import HTTPException

# Nombre con el que se reconoce el manejador del archivo. Sirve para no agregarlo dos
# veces si crear_app() se llama más de una vez en el mismo proceso (las pruebas lo hacen).
_NOMBRE_DEL_MANEJADOR = "miblog-archivo"

_FORMATO = "%(asctime)s %(levelname)s %(message)s"
_FORMATO_DE_FECHA = "%d/%m/%Y %H:%M:%S"


def configurar_registro(app: Flask, ruta_archivo: str) -> None:
    """Hace que app.logger escriba en `ruta_archivo`, con fecha y hora (RNF24).

    Guarda avisos y errores, no el funcionamiento normal. El archivo recién se crea
    cuando hay algo que anotar. Los errores también siguen saliendo por la consola,
    que es lo que Flask hace por su cuenta.
    """
    for existente in list(app.logger.handlers):
        if existente.get_name() == _NOMBRE_DEL_MANEJADOR:
            app.logger.removeHandler(existente)
            existente.close()

    manejador = logging.FileHandler(ruta_archivo, encoding="utf-8", delay=True)
    manejador.set_name(_NOMBRE_DEL_MANEJADOR)
    manejador.setLevel(logging.WARNING)
    manejador.setFormatter(logging.Formatter(_FORMATO, _FORMATO_DE_FECHA))
    app.logger.addHandler(manejador)


def registrar_manejadores_de_error(app: Flask) -> None:
    """Registra las páginas de error. Flask busca el manejador más específico primero:
    404 y 413 antes que cualquier error HTTP, y cualquier error HTTP antes que el
    manejador general. Por eso un 405 sigue siendo 405 y no se convierte en un 500.
    """
    app.register_error_handler(404, _pagina_inexistente)
    app.register_error_handler(413, _pedido_demasiado_grande)
    app.register_error_handler(HTTPException, _pedido_rechazado)
    app.register_error_handler(Exception, _error_inesperado)


def _pagina_inexistente(error: HTTPException):
    return _pagina_de_error(
        404,
        "Esa página no existe",
        "La dirección que abriste no existe o ya no está disponible.",
    )


def _pedido_demasiado_grande(error: HTTPException):
    # Pasa cuando el pedido supera MAX_CONTENT_LENGTH, que se fija un poco por encima
    # del tamaño máximo de la foto ("Archivos subidos").
    return _pagina_de_error(
        413,
        "Lo que enviaste pesa demasiado",
        "Si era una foto de perfil, elegí una más liviana.",
    )


def _pedido_rechazado(error: HTTPException):
    # Cualquier otro error HTTP (un 405 por abrir con GET algo que es solo POST, por
    # ejemplo). Se conserva su código y no se anota: no es una falla del sistema.
    return _pagina_de_error(
        error.code or 400,
        "No se pudo atender el pedido",
        "Volvé al inicio y probá de nuevo.",
    )


def _error_inesperado(error: Exception):
    # Se anota el mensaje y el recorrido completo del error (RNF24). Del pedido solo
    # se guardan el método y la ruta: nunca el formulario, que puede traer una clave.
    current_app.logger.error(
        "Error inesperado en %s %s", request.method, request.path, exc_info=error
    )
    return _pagina_de_error(
        500,
        "Algo salió mal",
        "Tuvimos un problema inesperado y quedó anotado. Probá de nuevo en unos minutos.",
    )


def _pagina_de_error(codigo: int, titulo: str, mensaje: str):
    return render_template("error.html", codigo=codigo, titulo=titulo, mensaje=mensaje), codigo