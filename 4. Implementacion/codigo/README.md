# MiBlog

Sistema de microblogging para empleados de una empresa. Cada persona publica mensajes de hasta 140 caracteres, sigue a otras y ve en su tablón lo que publican las personas a las que sigue, junto con lo propio. Trabajo de Ingeniería de Software.

## Qué se puede hacer

| Función | Estado |
|---|---|
| Registrarse: nombre de usuario (hasta 15 caracteres), correo, clave (al menos 8 caracteres), nombre completo y, de forma opcional, descripción y foto (PNG o JPG) | Disponible |
| Iniciar y cerrar sesión | Disponible |
| Buscar usuarios por nombre de usuario o nombre completo (sin distinguir mayúsculas ni acentos) y seguirlos | Disponible |
| Publicar un mensaje de hasta 140 caracteres | Disponible |
| Ver el tablón: los mensajes propios y los de las personas a las que se sigue, del más reciente al más antiguo | Disponible |
| Editar y borrar un mensaje propio, y republicar el de alguien a quien se sigue | Disponible |

## Cómo funciona un mensaje

- **Largo.** Hasta 140 caracteres, y no puede estar vacío. Se cuentan caracteres reales: un emoji cuenta 1 y un salto de línea cuenta 1. Si el mensaje se pasa, no se guarda ni se recorta: se avisa por cuántos caracteres se pasa y el texto queda en el formulario para corregirlo. Mientras se escribe, un contador muestra cuántos caracteres quedan (pasa a negativo cuando se excede el límite). Ese contador es lo único de la aplicación que usa JavaScript.
- **Etiquetas.** `#` seguido de letras, números o guion bajo, como `#reunion`. Se guardan en minúsculas, así que `#Reunion` y `#reunion` son la misma. No cuenta si antes del `#` hay una letra o una barra (`C#`, o el `#seccion` de una dirección web).
- **Menciones.** `@` seguido de un nombre de usuario, como `@juan.perez`. El nombre puede llevar punto o guion en el medio, pero no al final: en `hola @ana.` el punto es de la frase. La mención se guarda solo si existe un usuario activo con ese nombre; si no, se descarta sin avisar. `ana@empresa.com` no es una mención.
- **Enlaces.** Direcciones que empiezan con `http://` o `https://`. La puntuación del final no cuenta: en `mirá https://sitio.com.` el punto no es parte del enlace.
- **Qué se ve.** Las etiquetas, menciones y enlaces se detectan y se guardan al publicar o al editar, pero en pantalla el texto se muestra tal cual lo escribió la persona: todavía no son clicables.
- **Tablón.** Muestra cada mensaje con su autor, su fecha (`dd/mm/aaaa hh:mm`, hora del servidor) y su texto. Si no hay nada para mostrar, avisa y ofrece buscar usuarios para seguir.
- **Borrador.** Si la sesión vence mientras se escribe un mensaje, el texto se conserva y reaparece una vez al volver a iniciar sesión.
- **Editar.** Solo quien escribió el mensaje. El botón "Editar" abre una página con el texto actual; "Guardar" aplica las mismas reglas de largo que al publicar. Si el texto queda vacío o se pasa, se avisa y el mensaje guardado no cambia. Al guardar se vuelven a calcular las etiquetas, menciones y enlaces, y el mensaje muestra "(editado el dd/mm/aaaa hh:mm)". "Cancelar" vuelve al tablón sin tocar nada.
- **Borrar.** Solo quien escribió el mensaje. El botón "Borrar" abre una página que muestra el mensaje, avisa que no se puede deshacer y pide confirmar. Al confirmar se borran el mensaje, sus republicaciones y sus etiquetas, menciones y enlaces, todo junto o nada. Las etiquetas en sí quedan registradas aunque ningún mensaje las use.
- **Republicar.** El botón "Republicar" aparece en todo mensaje cuyo autor original no es uno mismo, y el servidor decide si corresponde. Solo se puede republicar el mensaje de alguien a quien se sigue, no el propio y una sola vez. Si no corresponde, se avisa por qué. La republicación no copia el texto: apunta al mensaje original, así que si el autor lo edita, la republicación muestra el texto nuevo, y si lo borra, desaparece. Se muestra en el tablón de quienes siguen a quien republicó, con su fecha.

## Requisitos

- Python 3.10 o más nuevo (probado con 3.13 y 3.14).
- Las dependencias están en `requirements.txt`: Flask 3.1.3 y python-dotenv 1.2.4.
- No hace falta instalar ninguna base de datos: SQLite viene con Python.

## Cómo arrancarlo

Todos los comandos se corren desde la carpeta que contiene este README.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env          # y editá SECRET_KEY: es obligatoria

flask --app miblog iniciar-bd # crea instance/miblog.sqlite3 (una sola vez)
flask --app miblog run        # abre http://127.0.0.1:5000
```

`iniciar-bd` se niega a correr si la base ya existe, para no pisar datos. Para empezar de cero, borrá `instance/miblog.sqlite3` y repetí el comando.

## Configuración

Se hace con un archivo `.env` en esta carpeta (se crea copiando `.env.example`). El `.env` no se sube al repositorio.

| Variable | Obligatoria | Por defecto | Para qué sirve |
|---|---|---|---|
| `SECRET_KEY` | Sí | — | Clave con la que Flask firma la cookie de sesión. Generá una con `python3 -c "import secrets; print(secrets.token_hex(32))"`. |
| `DURACION_SESION_MINUTOS` | No | `60` | Cuánto dura una sesión abierta. |
| `BASE_DE_DATOS` | No | `miblog.sqlite3` | Nombre del archivo de la base dentro de `instance/`, o una ruta absoluta. |
| `TAMANO_MAXIMO_FOTO_BYTES` | No | `2097152` (2 MB) | Tamaño máximo de la foto de perfil. |

## Datos de demostración

Para probar la aplicación con datos, sin cargarlos uno por uno, hay un script que llena la base con usuarios, seguimientos, mensajes y republicaciones de mentira:

```bash
python sembrar_datos.py            # agrega los datos de demostración
python sembrar_datos.py --borrar   # quita solo esos datos
```

- Muestra qué base va a tocar y pide confirmación: hay que escribir `SI` en mayúsculas. No modifica ni borra nada de lo que ya había. Si los usuarios de demostración ya existen, no hace nada.
- Agrega 8 usuarios, 12 seguimientos, 31 mensajes y 5 republicaciones. Todos los usuarios entran con la clave `demo-1234`, que es de mentira.
- Usuarios para probar:
  - `demo_ana`: tablón con variedad. Tiene mensajes propios y de otros, republicaciones, mensajes editados, uno de exactamente 140 caracteres, uno con saltos de línea y otro con emojis.
  - `demo_gus`: no sigue a nadie ni publicó nada, así que su tablón está vacío. Buscá "demo", seguí a `demo_ana` y volvé al tablón para verlo llenarse.
  - `demo.eva` y `demo-fer`: nombres con punto y con guion, para probar menciones como `@demo.eva`.
  - `demo_inactivo`: cuenta inactiva. No puede iniciar sesión, no aparece en la búsqueda y las menciones a ella se descartan.
- Los demás son `demo_beto`, `demo_carla` y `demo_dani`.
- Los datos de los mensajes usan fechas relativas a "ahora". Para renovarlos, hay que quitarlos con `--borrar` y volver a agregarlos.
- Es una herramienta de apoyo: está afuera de `miblog/` y no forma parte de la aplicación. Tiene SQL propio porque necesita fijar fechas y estados que la aplicación no deja elegir, como el usuario inactivo. Los mensajes sí se crean con las mismas clases que usa la aplicación, así que las etiquetas, menciones y enlaces quedan guardados igual que al publicar desde la pantalla.
- La clave pública `demo-1234` no es un secreto, pero por eso mismo el script no debe usarse sobre una base con datos reales ni en un sitio publicado.

## Pruebas

```bash
python -m unittest discover -s pruebas -t . -v
```

Para correr un solo archivo: `python -m unittest pruebas.test_tablon -v`.

Cada prueba arma su propia aplicación con una base temporal, así que nunca toca `instance/miblog.sqlite3`. Cubren:

- los extractores y el analizador de texto;
- los repositorios de mensajes, republicaciones y elementos;
- la publicación de mensajes y el tablón, incluido que una publicación que falla a mitad de camino no deja nada guardado;
- la edición y el borrado de mensajes (quién puede, qué pasa con las etiquetas, menciones, enlaces y republicaciones, y que si algo falla a mitad de camino no queda nada a medias);
- la republicación, con cada uno de sus avisos y el orden en que se verifican;
- la aplicación completa a través de HTTP, con el cliente de pruebas de Flask;
- el rendimiento del tablón (5.000 mensajes y 500 republicaciones, en menos de 3 segundos);
- las reglas de arquitectura que se describen más abajo (por ejemplo, que la presentación no llegue a la base de datos y que el SQL esté solo en `acceso_datos`).

## Estructura del proyecto

```
miblog/
├── __init__.py              crear_app(): arma la aplicación y conecta las capas
├── presentacion/            capa de presentación: lo que ve y toca la persona
│   ├── vistas_usuarios.py     registro, inicio y cierre de sesión
│   ├── vistas_relaciones.py   búsqueda y seguimiento de usuarios
│   ├── vistas_mensajes.py     tablón, publicación, edición, borrado y republicación
│   ├── seguridad_web.py       guardia de sesión: protege las rutas privadas
│   ├── plantillas/            páginas HTML (Jinja2)
│   └── estaticos/             estilos.css, contador.js, fuentes/ y fotos/ (fotos de perfil subidas)
├── logica/                  capa de lógica: las reglas del sistema
│   ├── dominio/               clases del negocio (Usuario, Mensaje, Republicacion...) y errores
│   ├── gestion_usuarios/      registro y autenticación
│   ├── gestion_relaciones/    búsqueda de usuarios y seguimiento
│   └── gestion_mensajes/      publicación, edición, borrado, republicación, tablón y análisis del texto
└── acceso_datos/            capa de acceso a datos: el único lugar con SQL
    ├── conexion.py            conexión a SQLite y transacciones
    ├── esquema.sql            las tablas
    ├── repositorio_*.py       un repositorio por tabla o grupo de tablas
    └── almacen_fotos.py       guarda y borra los archivos de las fotos de perfil
pruebas/                     pruebas automáticas (unittest)
sembrar_datos.py             llena la base con datos de demostración
requirements.txt             dependencias
.env.example                 modelo del archivo de configuración
instance/                    se crea al correr: acá queda la base de datos
```

## Arquitectura

El sistema tiene cuatro capas, y cada una solo le habla a la siguiente: presentación → lógica → acceso a datos → base de datos (SQLite).

- La presentación nunca importa `acceso_datos` ni `sqlite3`: pide todo a la lógica.
- Todo el SQL está en `acceso_datos`, siempre con parámetros (`?`), nunca armado con texto.
- El dominio (`logica/dominio/`) no depende de `acceso_datos`: define lo que necesita y la capa de datos lo implementa.
- `crear_app()` es el único lugar que elige las piezas concretas y las conecta entre sí.

Patrones de diseño que se usan:

- **Strategy y Factory Method:** `ExtractorEtiquetas`, `ExtractorMenciones` y `ExtractorEnlaces` comparten una interfaz, y `AnalizadorDeTexto` los recibe sin saber cuáles son. Sumar un tipo de elemento nuevo no obliga a tocar el analizador.
- **Template Method:** publicar y editar un mensaje siguen siempre los mismos pasos, todos dentro de una transacción (autorizar, validar el texto, analizarlo, guardar el mensaje y guardar sus elementos), fijados en `OperacionSobreMensaje.ejecutar`. `Publicacion` y `Edicion` solo completan lo que cambia: publicar crea el mensaje y editar lo actualiza, después de comprobar que quien edita es el autor. El límite de 140 caracteres está escrito en un solo lugar.
- **Decorator:** en el tablón, un mensaje y una republicación se muestran de la misma manera, sin que el código pregunte de qué tipo es cada uno. Los botones de cada tarjeta tampoco lo preguntan: se deciden por el autor original, que todo elemento sabe responder. Como la republicación le pide el texto al mensaje original, editarlo no obliga a tocar las republicaciones.

## Base de datos

SQLite, en `instance/miblog.sqlite3`, con las claves foráneas activadas. Las fechas se guardan en UTC, en formato ISO 8601.

| Tabla | Qué guarda |
|---|---|
| `usuarios` | Las cuentas. La clave se guarda con hash y salt, nunca en claro. |
| `sesiones` | Las sesiones abiertas. De cada una se guarda solo el hash SHA-256 de su token. |
| `seguimientos` | Quién sigue a quién. |
| `mensajes` | Los mensajes, con su autor, su fecha y si fueron editados. |
| `republicaciones` | Quién republicó qué mensaje, y cuándo. Referencia al original, no copia el texto. |
| `etiquetas` | Las etiquetas, una fila por nombre. |
| `mensaje_etiqueta` | Qué mensajes usan qué etiquetas. |
| `menciones` | Qué mensajes mencionan a qué usuarios. |
| `enlaces` | Los enlaces de cada mensaje. |

## Seguridad

- Las claves se guardan con hash y salt.
- La sesión es una fila de la tabla `sesiones`. El token viaja en la cookie (`HttpOnly`, `SameSite=Lax`) y en la base queda solo su hash, así que una copia del archivo de la base no sirve para armar una cookie. Al cerrar sesión, el token deja de valer en el servidor.
- Los errores de inicio de sesión son siempre el mismo mensaje ("Usuario o clave incorrectos."), para no revelar qué usuarios existen.
- El texto de los mensajes se escapa automáticamente al mostrarse, y todas las consultas SQL usan parámetros.
- Editar y borrar solo puede hacerlo el autor, y eso se verifica en el servidor dos veces: al abrir la página del diálogo y de nuevo al confirmar. Esconder un botón no es un control: un pedido hecho a mano por otra persona se rechaza. Republicar también se decide en el servidor, aunque el botón se vea.
- Los cambios de datos (editar, borrar, republicar) solo se aceptan por POST; abrir un enlace nunca borra ni edita nada.
- Límite conocido: no hay tokens contra CSRF; la protección es la cookie `SameSite=Lax`.

## Límites conocidos

- El tablón no tiene paginación: muestra todos los mensajes.
- Las etiquetas, menciones y enlaces no son clicables, y no hay búsqueda por etiqueta ni perfil de usuario.
- Un mensaje con muchísimos saltos de línea ocupa una tarjeta muy alta.
- Un borrador muy largo (más de unos 4 KB) no se conserva cuando vence la sesión.
- Un doble clic en "Publicar" crea dos mensajes. Un doble clic en "Republicar" no duplica nada, pero el segundo clic muestra el aviso de que ya se republicó.
- Guardar una edición sin cambiar el texto igual marca el mensaje como editado.
- No se puede deshacer una republicación ni borrar solo la propia republicación.
- Republicar con éxito no muestra ningún aviso: se nota porque la republicación aparece arriba de todo en el tablón.
- El registro no restringe el formato del nombre de usuario: uno con espacios o símbolos no se puede mencionar.
- No hay recuperación de clave ni edición del perfil.