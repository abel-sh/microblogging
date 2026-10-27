"""Datos de demostración para probar MiBlog a mano.

HERRAMIENTA DE APOYO del proyecto. No es parte de la aplicación ni de los diez casos
de uso, y no figura en el diseño (DISEÑO_MiBlog.md §2.4). Sirve solo para llenar la
base con usuarios, seguimientos, mensajes y republicaciones de mentira, y así ver el
tablón y la búsqueda con datos sin cargarlos uno por uno desde la pantalla.

Uso, desde 4. Implementacion/codigo/ y con el entorno virtual activado:

    python sembrar_datos.py            agrega 8 usuarios de demostración con sus datos
    python sembrar_datos.py --borrar   quita SOLO esos usuarios y todo lo que crearon

Trabaja sobre la base que usa la aplicación (instance/miblog.sqlite3, o la que diga
BASE_DE_DATOS en tu .env) y antes de tocarla muestra cuál es y pide confirmación
(escribir SI). No modifica ni borra nada de lo que ya hay: solo agrega, o quita lo que
agregó. Si alguno de los usuarios de demostración ya existe, no hace nada.

Qué usa de la aplicación y qué no. Los mensajes se crean con las mismas clases que
usa la aplicación (MensajePublico, RepositorioMensajes, AnalizadorDeTexto y los tres
extractores), así que las etiquetas, menciones y enlaces quedan guardados igual que si
se hubiera publicado cada mensaje desde la pantalla. Los usuarios, los seguimientos y
las republicaciones se insertan con SQL directo, porque hay que fijar fechas y estados
que ningún caso de uso deja elegir (por ejemplo, el usuario inactivo, H7). Por eso este
archivo tiene SQL y está afuera de miblog/: la regla "el SQL solo vive en acceso_datos"
(RNF25) rige para la aplicación.

Cuidado. Las cuentas son de mentira y comparten una clave pública, CLAVE_DE_DEMOSTRACION
(abajo). No es un secreto, pero por eso mismo no hay que usar este script sobre una base
con datos reales ni en un sitio publicado.
"""

from __future__ import annotations

import os
import sys
from datetime import datetime, timedelta, timezone

from werkzeug.security import generate_password_hash

from miblog import crear_app
from miblog.acceso_datos.conexion import obtener_conexion, transaccion
from miblog.acceso_datos.repositorio_elementos import RepositorioElementos
from miblog.acceso_datos.repositorio_mensajes import RepositorioMensajes
from miblog.logica.dominio.mensaje import MensajePublico
from miblog.logica.dominio.usuario import Usuario
from miblog.logica.gestion_mensajes.analizador import AnalizadorDeTexto
from miblog.logica.gestion_mensajes.extractores import (
    ExtractorEnlaces,
    ExtractorEtiquetas,
    ExtractorMenciones,
)
from miblog.logica.gestion_mensajes.operaciones_mensaje import OperacionSobreMensaje

# Es una clave de mentira para cuentas de mentira: no uses acá una clave de verdad.
CLAVE_DE_DEMOSTRACION = "demo-1234"

# (nombre_usuario, nombre_completo, activo). Dos nombres llevan "." y "-" a propósito,
# para probar las menciones de D-24.
USUARIOS = [
    ("demo_ana", "Ana Pérez", 1),
    ("demo_beto", "Beto Gómez", 1),
    ("demo_carla", "Carla Ruiz", 1),
    ("demo_dani", "Daniel Sosa", 1),
    ("demo.eva", "Eva Martínez", 1),
    ("demo-fer", "Fernanda López", 1),
    ("demo_gus", "Gustavo Ríos", 1),
    ("demo_inactivo", "Usuario Inactivo", 0),
]

# Quién sigue a quién. demo-fer y demo_gus no siguen a nadie, y demo_gus tampoco
# publicó nada: su tablón está vacío (ca 9.1).
SIGUE = {
    "demo_ana": ["demo_beto", "demo_carla", "demo.eva"],
    "demo_beto": ["demo_ana", "demo_carla"],
    "demo_carla": ["demo_ana"],
    "demo_dani": ["demo_ana", "demo_beto", "demo_carla", "demo.eva", "demo-fer"],
    "demo.eva": ["demo-fer"],
}

# (autor, publicado hace N minutos, texto, editado hace N minutos o None).
# El orden de esta lista importa: REPUBLICACIONES se refiere a los mensajes por posición.
MENSAJES = [
    ("demo_ana", 5, "Buen día equipo ☀️ Arrancamos la semana con #Planificacion. ¿Quién se suma a la reunión de las 10?", None),
    ("demo_beto", 12, "Agenda de hoy: https://ejemplo.com/agenda (cualquier cambio le aviso a @demo_ana) #reunion", None),
    ("demo_carla", 25, "Lanzamos el nuevo portal interno 🚀 Gran laburo de todo el equipo #lanzamiento #portal", None),
    ("demo_dani", 47, "Gracias @demo.eva por la ayuda con el informe #equipo", None),
    ("demo.eva", 90, "Receta del café de la oficina: 2 cucharadas, agua a 92 grados y paciencia ☕ #cafe", None),
    ("demo-fer", 130, "Tip de seguridad: no compartan sus claves con nadie, ni con @demo_inactivo ni con sistemas #seguridad", None),
    ("demo_ana", 200, "Resumen del día\nPrimero: cerramos el informe\nSegundo: falta revisar el presupuesto\n\nMañana seguimos", None),
    ("demo_beto", 380, "Mirá este artículo: https://medium.com/@autora/post-interesante #lectura", None),
    ("demo_carla", 600, "Escribí a nadie@empresa.com o preguntale a @fantasma_inexistente #consulta", None),
    ("demo_dani", 780, "Se viene el viernes de #asado 🍖 ¿Anotados? @demo_ana @demo_beto @demo-fer", None),
    ("demo.eva", 1300, "Cierre del trimestre: gracias a todos 🙌 #equipo #cierre", 1250),
    ("demo_ana", 1500, "Recordatorio: la capacitación de #seguridad es obligatoria. Más info en https://ejemplo.com/capacitacion.", None),
    ("demo_beto", 1700, "¿Alguien tiene un cargador USB-C? 🔌", None),
    ("demo-fer", 2600, "Feliz cumpleaños @demo.eva 🎂 #cumple", None),
    ("demo_carla", 2800, ("Justo en el límite: " + "a" * OperacionSobreMensaje.LIMITE)[: OperacionSobreMensaje.LIMITE], None),
    ("demo_dani", 3000, "Hoy me tocó #cafe sin azúcar 😅 #lunes", None),
    ("demo_ana", 3500, "Subí las fotos del evento: https://ejemplo.com/fotos?album=2026&ver=1 #evento", 3400),
    ("demo_beto", 4000, "Ayer cerramos el #lanzamiento sin incidentes 👏", None),
    ("demo_carla", 4100, "Probando emojis: " + "😀" * 20, None),
]
# Doce mensajes más, de relleno, para que el tablón tenga volumen y haya que bajar.
for _n in range(1, 13):
    _autor = ["demo_ana", "demo_beto", "demo_carla", "demo_dani", "demo.eva"][_n % 5]
    MENSAJES.append((_autor, 4500 + _n * 350, f"Novedad {_n} del día #novedades", None))

# (quién republica, posición del mensaje en MENSAJES, republicado hace N minutos).
REPUBLICACIONES = [
    ("demo_beto", 2, 8),   # ana sigue a beto y a carla: ve el original y la republicación
    ("demo.eva", 9, 60),   # ana sigue a eva pero no a dani: ve solo la republicación (H5)
    ("demo_ana", 1, 3),    # ana republica un mensaje de beto
    ("demo_dani", 4, 40),
    ("demo_carla", 11, 1000),
]


def sembrar() -> None:
    con = obtener_conexion()
    nombres = [nombre for nombre, _, _ in USUARIOS]
    ya_existen = [
        n for n in nombres
        if con.execute("SELECT 1 FROM usuarios WHERE nombre_usuario = ?", (n,)).fetchone()
    ]
    if ya_existen:
        print(f"Ya existen: {', '.join(ya_existen)}. No se hizo nada.")
        print("Si son datos de una vez anterior, quitalos primero con --borrar.")
        return

    ahora = datetime.now(timezone.utc)

    def hace(minutos: int) -> datetime:
        return ahora - timedelta(minutes=minutos)

    # El analizador y los repositorios son los mismos que usa la aplicación: así las
    # etiquetas, menciones y enlaces quedan guardados igual que si se hubiera publicado
    # cada mensaje desde la pantalla.
    analizador = AnalizadorDeTexto([ExtractorEtiquetas(), ExtractorMenciones(), ExtractorEnlaces()])
    repo_mensajes, repo_elementos = RepositorioMensajes(), RepositorioElementos()
    clave_hash = generate_password_hash(CLAVE_DE_DEMOSTRACION)

    # Todo o nada: si algo falla a mitad de camino, no queda nada a medias.
    with transaccion():
        ids = {}
        for nombre, completo, activo in USUARIOS:
            cursor = con.execute(
                "INSERT INTO usuarios (nombre_usuario, email, clave_hash, nombre_completo,"
                " fecha_alta, activo) VALUES (?, ?, ?, ?, ?, ?)",
                (nombre, f"{nombre}@ejemplo.com", clave_hash, completo, hace(60 * 24 * 7).isoformat(), activo),
            )
            ids[nombre] = cursor.lastrowid

        for seguidor, seguidos in SIGUE.items():
            for seguido in seguidos:
                con.execute(
                    "INSERT INTO seguimientos (id_seguidor, id_seguido, fecha_inicio) VALUES (?, ?, ?)",
                    (ids[seguidor], ids[seguido], hace(60 * 24 * 6).isoformat()),
                )

        ids_de_mensajes = []
        for autor, minutos, texto, editado_hace in MENSAJES:
            assert len(texto) <= OperacionSobreMensaje.LIMITE, f"Se pasa del límite: {texto!r}"
            usuario = Usuario(id_usuario=ids[autor], nombre_usuario=autor, nombre_completo=autor)
            mensaje = MensajePublico.publicar(usuario, texto, hace(minutos))
            if editado_hace is not None:
                mensaje.editar(texto, hace(editado_hace))
            id_mensaje = repo_mensajes.crear(mensaje)
            for elemento in analizador.analizar(texto):
                elemento.guardar_en(repo_elementos, id_mensaje)
            ids_de_mensajes.append(id_mensaje)

        for republicador, posicion, minutos in REPUBLICACIONES:
            con.execute(
                "INSERT INTO republicaciones (id_usuario, id_mensaje, fecha_republicacion) VALUES (?, ?, ?)",
                (ids[republicador], ids_de_mensajes[posicion], hace(minutos).isoformat()),
            )

    print(f"Listo: {len(USUARIOS)} usuarios, {len(MENSAJES)} mensajes, "
          f"{sum(len(s) for s in SIGUE.values())} seguimientos y {len(REPUBLICACIONES)} republicaciones.")
    print(f"Todos los usuarios entran con la clave: {CLAVE_DE_DEMOSTRACION}")
    print("Para empezar: demo_ana (tablón variado) y demo_gus (tablón vacío).")


def borrar() -> None:
    con = obtener_conexion()
    nombres = [nombre for nombre, _, _ in USUARIOS]
    with transaccion():
        marcas = ",".join("?" * len(nombres))
        ids = [f[0] for f in con.execute(
            f"SELECT id_usuario FROM usuarios WHERE nombre_usuario IN ({marcas})", nombres)]
        if not ids:
            print("No hay usuarios de demostración. No se hizo nada.")
            return
        u = ",".join("?" * len(ids))
        mensajes_demo = f"SELECT id_mensaje FROM mensajes WHERE id_autor IN ({u})"

        # Las etiquetas que usaron los mensajes de demostración: al final se borran las
        # que no use ningún otro mensaje. Hay que anotarlas antes de soltar los mensajes.
        etiquetas = [f[0] for f in con.execute(
            f"SELECT DISTINCT id_etiqueta FROM mensaje_etiqueta WHERE id_mensaje IN ({mensajes_demo})", ids)]

        # De adentro hacia afuera: primero lo que apunta a otras filas, y al final los
        # usuarios. (Las claves foráneas no dejan borrar un usuario del que algo depende.)
        borrados = {}
        pasos = [
            ("republicaciones", f"DELETE FROM republicaciones WHERE id_usuario IN ({u}) OR id_mensaje IN ({mensajes_demo})", ids + ids),
            ("menciones", f"DELETE FROM menciones WHERE id_mensaje IN ({mensajes_demo}) OR id_usuario_mencionado IN ({u})", ids + ids),
            ("enlaces", f"DELETE FROM enlaces WHERE id_mensaje IN ({mensajes_demo})", ids),
            ("mensaje_etiqueta", f"DELETE FROM mensaje_etiqueta WHERE id_mensaje IN ({mensajes_demo})", ids),
            ("mensajes", f"DELETE FROM mensajes WHERE id_autor IN ({u})", ids),
            ("seguimientos", f"DELETE FROM seguimientos WHERE id_seguidor IN ({u}) OR id_seguido IN ({u})", ids + ids),
            ("sesiones", f"DELETE FROM sesiones WHERE id_usuario IN ({u})", ids),
            ("usuarios", f"DELETE FROM usuarios WHERE id_usuario IN ({u})", ids),
        ]
        for tabla, sql, parametros in pasos:
            borrados[tabla] = con.execute(sql, parametros).rowcount
        for id_etiqueta in etiquetas:
            borrados["etiquetas"] = borrados.get("etiquetas", 0) + con.execute(
                "DELETE FROM etiquetas WHERE id_etiqueta = ?"
                " AND id_etiqueta NOT IN (SELECT id_etiqueta FROM mensaje_etiqueta)",
                (id_etiqueta,),
            ).rowcount
    print("Quitado: " + ", ".join(f"{n} {tabla}" for tabla, n in borrados.items() if n))


def main() -> int:
    borrando = "--borrar" in sys.argv[1:]
    app = crear_app()
    ruta = app.config["BASE_DE_DATOS"]
    if not os.path.exists(ruta):
        print(f"La base de datos no existe todavía ({ruta}).")
        print("Primero creala con:  flask --app miblog iniciar-bd")
        return 1
    print(f"Base de datos: {ruta}")
    accion = "QUITAR los datos de demostración" if borrando else "AGREGAR datos de demostración"
    if input(f"Vas a {accion}. Escribí SI para continuar: ").strip() != "SI":
        print("No se hizo nada.")
        return 0
    with app.app_context():
        if borrando:
            borrar()
        else:
            sembrar()
    return 0


if __name__ == "__main__":
    sys.exit(main())