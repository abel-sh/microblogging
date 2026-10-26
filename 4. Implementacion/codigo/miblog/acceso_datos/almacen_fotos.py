"""AlmacenFotos: guarda y borra los archivos de las fotos de perfil.

Diseño: Persistencia, "Fotos de perfil" y clase AlmacenFotos.
Es la única clase que toca el disco por las fotos. No decide si una foto
es válida (eso lo hace ControlRegistro, ca 1.3): solo escribe y borra.
"""

import uuid
from pathlib import Path


class AlmacenFotos:

    def __init__(self, carpeta: Path | str) -> None:
        self._carpeta = Path(carpeta)

    def guardar(self, contenido: bytes, extension: str) -> str:
        """Escribe la foto y devuelve el nombre del archivo.

        La extensión va sin punto y en minúscula: "png", "jpg" o "jpeg".
        El nombre lo inventa el sistema, nunca el usuario.
        """
        self._carpeta.mkdir(parents=True, exist_ok=True)
        nombre_archivo = f"{uuid.uuid4().hex}.{extension}"
        (self._carpeta / nombre_archivo).write_bytes(contenido)
        return nombre_archivo

    def eliminar(self, nombre_archivo: str) -> None:
        """Borra el archivo. Si ya no está, no hace nada."""
        # Path(...).name descarta cualquier ruta: solo se borra dentro de la carpeta.
        ruta = self._carpeta / Path(nombre_archivo).name
        ruta.unlink(missing_ok=True)