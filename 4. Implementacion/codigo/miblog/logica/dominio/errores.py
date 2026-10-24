"""Errores de negocio.

Cada curso alternativo que rechaza una operación es una subclase de
ErrorDeNegocio. La lógica la lanza; la vista la captura y muestra `mensaje`.

Ningún mensaje escribe el límite de caracteres: la vista lo toma de
OperacionSobreMensaje.LIMITE.
"""

from __future__ import annotations


class ErrorDeNegocio(Exception):
    """Base de todos los errores esperados. `mensaje` está pensado para el usuario."""

    def __init__(self, mensaje: str) -> None:
        super().__init__(mensaje)
        self.mensaje = mensaje


class DatosInvalidosError(ErrorDeNegocio):
    """ca 1.1, ca 1.3, ca 2.2. `errores_por_campo` es {nombre_del_campo: texto del error}."""

    def __init__(self, errores_por_campo: dict[str, str]) -> None:
        super().__init__("Hay datos que tenés que corregir.")
        self.errores_por_campo = errores_por_campo


class UsuarioDuplicadoError(ErrorDeNegocio):
    """ca 1.2. `campos` dice cuáles están en uso: ["nombre_usuario"], ["email"] o los dos."""

    def __init__(self, campos: list[str]) -> None:
        super().__init__("Ya existe una cuenta con esos datos.")
        self.campos = campos


class CredencialesInvalidasError(ErrorDeNegocio):
    """ca 2.1. Un solo mensaje para usuario inexistente, inactivo o clave incorrecta (rnf 2.3)."""

    def __init__(self) -> None:
        super().__init__("Usuario o clave incorrectos.")


class TextoVacioError(ErrorDeNegocio):
    """ca 4.1, ca 5.3."""

    def __init__(self) -> None:
        super().__init__("El mensaje no puede estar vacío.")


class TextoExcedidoError(ErrorDeNegocio):
    """ca 4.2, ca 5.3. `excedente` es cuántos caracteres sobran."""

    def __init__(self, excedente: int) -> None:
        super().__init__(f"El mensaje se pasa por {excedente} caracteres.")
        self.excedente = excedente


class MensajeInexistenteError(ErrorDeNegocio):
    """ca 5.1, ca 6.1, ca 7.4."""

    def __init__(self) -> None:
        super().__init__("El mensaje ya no está disponible.")


class NoEsAutorError(ErrorDeNegocio):
    """ca 5.2, ca 6.2. Un solo mensaje sirve para editar y para borrar."""

    def __init__(self) -> None:
        super().__init__("Solo el autor puede editar o borrar este mensaje.")


class AutorNoSeguidoError(ErrorDeNegocio):
    """ca 7.1."""

    def __init__(self) -> None:
        super().__init__("Solo podés republicar mensajes de usuarios a los que seguís.")


class MensajePropioError(ErrorDeNegocio):
    """ca 7.2."""

    def __init__(self) -> None:
        super().__init__("No podés republicar tus propios mensajes.")


class RepublicacionExistenteError(ErrorDeNegocio):
    """ca 7.3."""

    def __init__(self) -> None:
        super().__init__("Ya republicaste este mensaje.")


class UsuarioInexistenteError(ErrorDeNegocio):
    """ca 11.1."""

    def __init__(self) -> None:
        super().__init__("El usuario no existe o no está disponible.")


class AutoSeguimientoError(ErrorDeNegocio):
    """ca 11.2."""

    def __init__(self) -> None:
        super().__init__("Tus mensajes ya aparecen en tu tablón.")


class SeguimientoExistenteError(ErrorDeNegocio):
    """ca 11.3."""

    def __init__(self) -> None:
        super().__init__("Ya seguís a este usuario.")


class CriterioVacioError(ErrorDeNegocio):
    """ca 14.1."""

    def __init__(self) -> None:
        super().__init__("Ingresá al menos un carácter para buscar.")