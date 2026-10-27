"""ControlPublicacion: realiza CU0004 Publicar, CU0005 Editar y CU0006 Borrar Mensaje.

No sabe de HTTP ni de SQL, y tampoco repite los pasos de publicar ni de editar:
recibe armadas las dos operaciones del Template Method (Publicacion y Edicion) y
le pide a cada una que se ejecute. Por eso publicar() y editar() quedan en una
línea.

Borrar NO usa el Template Method: no valida texto, no analiza ni guarda un
mensaje, así que no comparte el esqueleto. Es un método común de
este control, que reutiliza verificar_autoria().
"""

from __future__ import annotations

from miblog.acceso_datos.conexion import transaccion
from miblog.acceso_datos.repositorio_elementos import RepositorioElementos
from miblog.acceso_datos.repositorio_mensajes import RepositorioMensajes
from miblog.acceso_datos.repositorio_republicaciones import RepositorioRepublicaciones
from miblog.logica.dominio.errores import MensajeInexistenteError
from miblog.logica.dominio.mensaje import MensajePublico
from miblog.logica.dominio.usuario import Usuario
from miblog.logica.gestion_mensajes.operaciones_mensaje import Edicion, Publicacion


class ControlPublicacion:
    def __init__(
        self,
        publicacion: Publicacion,
        edicion: Edicion,
        repo_mensajes: RepositorioMensajes,
        repo_republicaciones: RepositorioRepublicaciones,
        repo_elementos: RepositorioElementos,
    ) -> None:
        self._publicacion = publicacion
        self._edicion = edicion
        self._repo_mensajes = repo_mensajes
        self._repo_republicaciones = repo_republicaciones
        self._repo_elementos = repo_elementos

    def publicar(self, autor: Usuario, texto: str) -> MensajePublico:
        """Publica el texto como mensaje de `autor`, o lanza el error del curso alternativo.

        Los errores posibles son TextoVacioError (ca 4.1) y TextoExcedidoError
        (ca 4.2). La sesión expirada (ca 4.3) no llega hasta acá: la atiende
        GuardiaSesion antes de que se ejecute la vista.
        """
        return self._publicacion.ejecutar(autor, texto)

    def verificar_autoria(self, id_mensaje: int, usuario: Usuario) -> MensajePublico:
        """Devuelve el mensaje si `usuario` es su autor; si no, lanza el error que corresponda.

        Lo llaman los dos diálogos al abrirse (CU0005 y CU0006, paso 2) y borrar()
        al confirmar. Lanza MensajeInexistenteError (ca 5.1, ca 6.1) o
        NoEsAutorError (ca 5.2, ca 6.2). Solo lee: no abre transacción.
        """
        mensaje = self._repo_mensajes.buscar_por_id(id_mensaje)
        if mensaje is None:
            raise MensajeInexistenteError()
        mensaje.verificar_autoria(usuario.id_usuario)
        return mensaje

    def editar(self, id_mensaje: int, usuario: Usuario, texto: str) -> MensajePublico:
        """Cambia el texto del mensaje de `usuario`, o lanza el error del curso alternativo.

        Los errores posibles son MensajeInexistenteError (ca 5.1), NoEsAutorError
        (ca 5.2), TextoVacioError y TextoExcedidoError (ca 5.3). La autoría se
        vuelve a verificar adentro de la operación .
        """
        return self._edicion.ejecutar(usuario, texto, id_mensaje=id_mensaje)
    def borrar(self, id_mensaje: int, usuario: Usuario) -> None:
        """Borra el mensaje de `usuario` y todo lo que depende de él (CU0006).

        Todo ocurre en una transacción y en este orden:
        primero las republicaciones, después los elementos (menciones, enlaces y
        asociaciones con etiquetas) y por último el mensaje. Las etiquetas quedan
        registradas. Si cualquier paso falla, no se borra nada.

        La autoría se verifica de nuevo adentro de la transacción. Como
        la transacción toma el bloqueo de escritura al empezar, nadie puede
        cambiar el mensaje entre la verificación y el borrado.
        """
        with transaccion():
            self.verificar_autoria(id_mensaje, usuario)
            self._repo_republicaciones.eliminar_por_mensaje(id_mensaje)
            self._repo_elementos.eliminar_de_mensaje(id_mensaje)
            self._repo_mensajes.eliminar(id_mensaje)