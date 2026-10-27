"""MiBlog: raíz de composición.

crear_app() es el único módulo que conoce las cuatro capas: crea los
repositorios, se los da a los controles, les da los controles a las vistas y
registra las rutas. En el bloque 4.2 están las rutas de la sesión: registro,
inicio y cierre de sesión (CU0001, CU0002, CU0003). En el bloque 4.3 se suman
las primeras rutas protegidas: buscar usuarios y seguirlos (CU0014, CU0011). En
el bloque 4.4 llegan el tablón y la publicación de mensajes (CU0009, CU0004).
"""

from __future__ import annotations

import os
from datetime import timedelta

import click
from dotenv import load_dotenv
from flask import Flask

from miblog.acceso_datos.almacen_fotos import AlmacenFotos
from miblog.acceso_datos.conexion import (
    BaseYaInicializadaError,
    cerrar_conexion,
    inicializar_base,
)
from miblog.acceso_datos.repositorio_elementos import RepositorioElementos
from miblog.acceso_datos.repositorio_mensajes import RepositorioMensajes
from miblog.acceso_datos.repositorio_republicaciones import RepositorioRepublicaciones
from miblog.acceso_datos.repositorio_seguimientos import RepositorioSeguimientos
from miblog.acceso_datos.repositorio_sesiones import RepositorioSesiones
from miblog.acceso_datos.repositorio_usuarios import RepositorioUsuarios
from miblog.logica.gestion_mensajes.analizador import AnalizadorDeTexto
from miblog.logica.gestion_mensajes.control_publicacion import ControlPublicacion
from miblog.logica.gestion_mensajes.control_tablon import ControlTablon
from miblog.logica.gestion_mensajes.extractores import (
    ExtractorEnlaces,
    ExtractorEtiquetas,
    ExtractorMenciones,
)
from miblog.logica.gestion_mensajes.operaciones_mensaje import Publicacion
from miblog.logica.gestion_relaciones.control_busqueda_usuarios import ControlBusquedaUsuarios
from miblog.logica.gestion_relaciones.control_seguimiento import ControlSeguimiento
from miblog.logica.gestion_usuarios.control_autenticacion import ControlAutenticacion
from miblog.logica.gestion_usuarios.control_registro import ControlRegistro
from miblog.presentacion.seguridad_web import GuardiaSesion
from miblog.presentacion.vistas_mensajes import VistaTablon, formatear_fecha
from miblog.presentacion.vistas_relaciones import VistaBusquedaUsuarios
from miblog.presentacion.vistas_usuarios import (
    VistaConfirmacionCierreSesion,
    VistaInicioSesion,
    VistaRegistro,
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

    # Fotos de perfil (ca 1.3): tamaño máximo configurable. MAX_CONTENT_LENGTH es el
    # tope duro de Flask para toda la petición, un poco por encima del de la foto.
    tamano_maximo_foto = int(os.environ.get("TAMANO_MAXIMO_FOTO_BYTES", str(2 * 1024 * 1024)))
    app.config["TAMANO_MAXIMO_FOTO_BYTES"] = tamano_maximo_foto
    app.config["MAX_CONTENT_LENGTH"] = tamano_maximo_foto + 1024 * 1024

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

    # --- Capa 3: repositorios y almacén de fotos ---
    repo_usuarios = RepositorioUsuarios()
    repo_sesiones = RepositorioSesiones()
    repo_seguimientos = RepositorioSeguimientos()
    repo_mensajes = RepositorioMensajes()
    repo_republicaciones = RepositorioRepublicaciones()
    repo_elementos = RepositorioElementos()
    almacen_fotos = AlmacenFotos(os.path.join(app.static_folder, "fotos"))

    # --- Capa 2: controles ---
    control_registro = ControlRegistro(repo_usuarios, almacen_fotos, tamano_maximo_foto)
    control_autenticacion = ControlAutenticacion(
        repo_usuarios,
        repo_sesiones,
        timedelta(minutes=app.config["DURACION_SESION_MINUTOS"]),
    )
    control_busqueda = ControlBusquedaUsuarios(repo_usuarios, repo_seguimientos)
    control_seguimiento = ControlSeguimiento(repo_usuarios, repo_seguimientos)

    # Strategy: este es el único lugar que nombra los extractores concretos. El
    # analizador los recibe ya armados y no sabe cuáles son. Para sumar un cuarto
    # tipo de elemento se agrega una clase y se la suma a esta lista.
    analizador = AnalizadorDeTexto(
        [ExtractorEtiquetas(), ExtractorMenciones(), ExtractorEnlaces()]
    )
    # Template Method: la operación de publicar, con todo lo que necesita ya adentro.
    publicacion = Publicacion(analizador, repo_mensajes, repo_elementos)
    control_publicacion = ControlPublicacion(publicacion)
    control_tablon = ControlTablon(repo_mensajes, repo_republicaciones)

    # --- Capa 1: guardia y vistas ---
    # La guardia envuelve las rutas protegidas: buscar y seguir (bloque 4.3), y el
    # tablón y publicar (bloque 4.4).
    guardia = GuardiaSesion(control_autenticacion)
    vista_inicio_sesion = VistaInicioSesion(control_autenticacion)
    vista_registro = VistaRegistro(control_registro)
    vista_cierre = VistaConfirmacionCierreSesion(control_autenticacion)
    vista_busqueda = VistaBusquedaUsuarios(control_busqueda, control_seguimiento)
    vista_tablon = VistaTablon(control_tablon, control_publicacion)

    # Filtro de las plantillas para mostrar fechas: {{ fecha_del_mensaje|fecha }}.
    app.add_template_filter(formatear_fecha, "fecha")

    # --- Rutas públicas: ninguna de estas pasa por la guardia. ---
    app.add_url_rule("/", "inicio_sesion", vista_inicio_sesion.mostrar)
    app.add_url_rule("/sesion/iniciar", "iniciar_sesion", vista_inicio_sesion.iniciar_sesion,
                     methods=["POST"])
    app.add_url_rule("/registro", "registro", vista_registro.mostrar)
    app.add_url_rule("/registro", "registrar", vista_registro.registrar, methods=["POST"])
    app.add_url_rule("/sesion/cerrar", "solicitar_cierre_sesion",
                     vista_cierre.solicitar_confirmacion)
    app.add_url_rule("/sesion/cerrar", "confirmar_cierre_sesion", vista_cierre.confirmar,
                     methods=["POST"])

    # --- Rutas protegidas: sin sesión vigente, la guardia redirige al inicio. ---
    app.add_url_rule("/usuarios/buscar", "buscar_usuarios",
                     guardia.requiere_sesion(vista_busqueda.buscar))
    app.add_url_rule("/usuarios/<int:id_seguido>/seguir", "seguir_usuario",
                     guardia.requiere_sesion(vista_busqueda.seguir), methods=["POST"])
    app.add_url_rule("/tablon", "tablon", guardia.requiere_sesion(vista_tablon.mostrar))
    # conservar_borrador=True: si la sesión expiró mientras el usuario escribía, la
    # guardia guarda el texto para devolvérselo al volver a iniciar sesión (ca 4.3).
    app.add_url_rule("/mensajes", "publicar_mensaje",
                     guardia.requiere_sesion(vista_tablon.publicar, conservar_borrador=True),
                     methods=["POST"])

    return app


# Flask, cuando se lo llama con "--app miblog", busca una función llamada
# create_app o make_app (en inglés). Este alias deja que el comando del diseño
# funcione tal cual sin renombrar crear_app.
create_app = crear_app