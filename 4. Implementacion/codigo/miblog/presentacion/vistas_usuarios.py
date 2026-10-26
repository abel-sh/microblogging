"""Vistas de CU0001, CU0002 y CU0003.

Cada método atiende una ruta de Flask: lee la petición, llama a un control, y
elige la plantilla o la redirección. Ninguna regla de negocio vive acá, y esta
capa nunca llega directo a la base de datos.
"""

from __future__ import annotations

from flask import flash, redirect, render_template, request, session

from miblog.logica.dominio.errores import (
    CredencialesInvalidasError,
    DatosInvalidosError,
    UsuarioDuplicadoError,
)
from miblog.logica.gestion_usuarios.control_autenticacion import ControlAutenticacion
from miblog.logica.gestion_usuarios.control_registro import ControlRegistro, DatosRegistro


class VistaRegistro:
    def __init__(self, control_registro: ControlRegistro) -> None:
        self._control_registro = control_registro

    def mostrar(self):
        """GET /registro"""
        return render_template("registro.html", errores={}, valores={})

    def registrar(self):
        """POST /registro"""
        datos = self._leer_formulario()
        try:
            usuario = self._control_registro.registrar_usuario(datos)
        except DatosInvalidosError as error:
            return self._formulario_con_errores(datos, error.errores_por_campo)
        except UsuarioDuplicadoError as error:
            errores = {}
            if "nombre_usuario" in error.campos:
                errores["nombre_usuario"] = "Ese nombre de usuario ya está en uso."
            if "email" in error.campos:
                errores["email"] = "Ese correo electrónico ya está en uso."
            return self._formulario_con_errores(datos, errores)
        return render_template("registro_ok.html", usuario=usuario)

    def _leer_formulario(self) -> DatosRegistro:
        foto = request.files.get("foto")
        hay_foto = foto is not None and foto.filename != ""
        return DatosRegistro(
            nombre_usuario=request.form.get("nombre_usuario", ""),
            email=request.form.get("email", ""),
            clave=request.form.get("clave", ""),
            confirmacion_clave=request.form.get("confirmacion_clave", ""),
            nombre_completo=request.form.get("nombre_completo", ""),
            descripcion=request.form.get("descripcion"),
            nombre_archivo_foto=foto.filename if hay_foto else None,
            contenido_foto=foto.read() if hay_foto else None,
        )

    def _formulario_con_errores(self, datos: DatosRegistro, errores: dict[str, str]):
        # Se devuelven los datos escritos, menos las claves (ca 1.1.2).
        valores = {
            "nombre_usuario": datos.nombre_usuario,
            "email": datos.email,
            "nombre_completo": datos.nombre_completo,
            "descripcion": datos.descripcion or "",
        }
        return render_template("registro.html", errores=errores, valores=valores)


class VistaInicioSesion:
    def __init__(self, control_autenticacion: ControlAutenticacion) -> None:
        self._control_autenticacion = control_autenticacion

    def mostrar(self):
        """GET /"""
        return render_template("inicio_sesion.html", errores={}, valores={})

    def iniciar_sesion(self):
        """POST /sesion/iniciar"""
        nombre_usuario = request.form.get("nombre_usuario", "")
        clave = request.form.get("clave", "")
        try:
            token = self._control_autenticacion.autenticar(nombre_usuario, clave)
        except DatosInvalidosError as error:
            return render_template(
                "inicio_sesion.html",
                errores=error.errores_por_campo,
                valores={"nombre_usuario": nombre_usuario},
            )
        except CredencialesInvalidasError as error:
            flash(error.mensaje, "error")
            return render_template(
                "inicio_sesion.html",
                errores={},
                valores={"nombre_usuario": nombre_usuario},
            )

        # El borrador (ca 4.3) sobrevive al session.clear(): se saca antes y se vuelve a poner.
        borrador = session.get("borrador")
        session.clear()
        session["token"] = token
        if borrador is not None:
            session["borrador"] = borrador
        return redirect("/tablon")


class VistaConfirmacionCierreSesion:
    def __init__(self, control_autenticacion: ControlAutenticacion) -> None:
        self._control_autenticacion = control_autenticacion

    def solicitar_confirmacion(self):
        """GET /sesion/cerrar"""
        return render_template("cerrar_sesion.html")

    def confirmar(self):
        """POST /sesion/cerrar"""
        self._control_autenticacion.cerrar_sesion(session.get("token"))
        session.clear()
        return redirect("/")