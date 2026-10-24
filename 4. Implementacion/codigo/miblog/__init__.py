"""MiBlog: raíz de composición.

crear_app() es el único módulo que conoce las cuatro capas: crea los
repositorios, se los da a los controles, les da los controles a las vistas y
registra las rutas. En el bloque 4.1 todavía no hay nada de eso: solo la
configuración, la conexión a la base, el comando iniciar-bd y una página
provisoria.
"""

from __future__ import annotations

import os

import click
from dotenv import load_dotenv
from flask import Flask, render_template

from miblog.acceso_datos.conexion import (
    BaseYaInicializadaError,
    cerrar_conexion,
    inicializar_base,
)


def crear_app() -> Flask:
    # Lee el archivo .env (si existe) y lo vuelca en las variables de entorno.
    load_dotenv()

    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="presentacion/plantillas",
        static_folder="presentacion/estaticos",
    )

    # --- Configuración ---
    clave_secreta = os.environ.get("SECRET_KEY")
    if not clave_secreta:
        raise RuntimeError(
            "Falta SECRET_KEY. Copiá .env.example como .env y completá el valor."
        )
    app.config["SECRET_KEY"] = clave_secreta
    app.config["DURACION_SESION_MINUTOS"] = int(
        os.environ.get("DURACION_SESION_MINUTOS", "60")
    )
    # Mitigación de CSRF sin dependencias extra.
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_HTTPONLY"] = True

    # --- Carpeta instance/ y base de datos (capa de persistencia) ---
    os.makedirs(app.instance_path, exist_ok=True)
    ruta_base = os.environ.get("BASE_DE_DATOS", "miblog.sqlite3")
    if not os.path.isabs(ruta_base):
        ruta_base = os.path.join(app.instance_path, ruta_base)
    app.config["BASE_DE_DATOS"] = ruta_base

    # Una conexión por petición: se abre al pedirla y se cierra acá.
    app.teardown_appcontext(cerrar_conexion)

    # --- Comando:  flask --app miblog iniciar-bd ---
    @app.cli.command("iniciar-bd")
    def iniciar_bd() -> None:
        """Crea las tablas de la base de datos."""
        try:
            inicializar_base()
        except BaseYaInicializadaError as error:
            raise click.ClickException(str(error))
        click.echo(f"Base creada en {app.config['BASE_DE_DATOS']}")

    # --- Página provisoria del bloque 4.1 ---
    # El diseño no tiene ninguna ruta que muestre una página sin un caso de uso
    # (la primera es GET /, de CU0002). Esta se reemplaza en el bloque 4.2.
    @app.get("/")
    def inicio_provisorio():
        return render_template("inicio_provisorio.html")

    return app


# Flask, cuando se lo llama con "--app miblog", busca una función llamada
# create_app o make_app (en inglés). Este alias deja que el comando del diseño
# funcione tal cual sin renombrar crear_app.
create_app = crear_app