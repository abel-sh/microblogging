# PLAN DEL PROYECTO — Sistema MiBlog
 
**Versión:** 1.15 · **Última modificación:** 28/10/2026 · **Etapa:** Gestión del proyecto
 
**Materia:** Ingeniería de Software · **Alumno:** Abel
**Qué se rinde:** Final = entrega del proyecto + defensa oral (práctica y teórica)
**Modalidad:** proyecto pensado para grupos de ocho personas, cursado y entregado **en solitario**. El recorte de alcance que eso obligó es una **decisión propia del alumno**, no un acuerdo con la cátedra; el fundamento está en la §7, riesgo 3.
**Fecha de entrega y defensa:** **24/11/2026**
**Alcance:** 21 casos de uso especificados · **10 realizados** (6 → 9 → 10, cerrado el 13/09)
**Este archivo reemplaza a `PLAN_6_DIAS.md` y a `PROMPTS_POR_ETAPA.md`.**
 
---
 
## 1. Lo que ya está listo
 
| Documento | Contenido | Estado |
|---|---|---|
| `REQUISITOS_CANDIDATOS_MiBlog.md` | C01–C38, características evaluadas con su estado | Listo |
| `REQUISITOS_FUNCIONALES_MiBlog.md` | RF01–RF21 y reglas automáticas RA01–RA11 | Listo |
| `REQUISITOS_NO_FUNCIONALES_MiBlog.md` | RNF01–RNF42 y las dependencias declaradas (§8.0) | Listo, con la decisión tecnológica cerrada. Versión 1.1 |
| `DIA1_REQUISITOS_MiBlog.md` | 6 actores · catálogo de 21 CU priorizado · modelo de dominio (15 clases) · diagrama único de casos de uso · alcance de la iteración | Listo |
| `ESPECIFICACIONES_CASOS_DE_USO_MiBlog.md` | Los 21 casos de uso especificados con la plantilla de la cátedra | Listo y verificado. Versión 1.3 (28/10): suma la forma admitida del nombre de usuario y apunta a las pantallas del prototipo; la 1.2 traía las correcciones del Diseño |
| `Prototipo de Interfaces.pdf` | Las vistas de la aplicación | Listo (14/09); actualizado el 28/10 al diseño visual implementado. Es el artefacto de Requisitos: fija qué elementos tiene cada vista y cómo se navega |
| `ANALISIS_MiBlog.md` | 23 clases de análisis, paquetes, diez colaboraciones, patrones con anclaje real | Etapa 2 cerrada. Versión 2.2, con las correcciones del Diseño |
| `DISEÑO_MiBlog.md` | Arquitectura y mecanismos, diagrama de clases integral, despliegue, subsistemas, diez secuencias, estados | Etapa 3 cerrada. Versión 1.4 (28/10): pasó al diseño los desvíos DV-4 a DV-8 (miembros de apoyo y una nota en el diagrama de clases, endpoints de las rutas, errores y registro); ningún nombre de clase, método ni ruta cambió. La 1.3 (24/10) había corregido la §2.4 por la estructura real del repositorio |
| `CONTEXTO_IMPLEMENTACION_MiBlog.md` | Traspaso entre los seis bloques de la Etapa 4: repositorio real, decisiones, desvíos, pendientes, informes de cierre | Versión 1.8 (28/10), con los seis bloques de la Etapa 4 cerrados |
 
**En resumen: los flujos de Requisitos, Análisis y Diseño están cerrados.** Son los tres más largos del proyecto.
 
### 1.1 Lo que queda abierto de Requisitos
 
Nada de contenido. Queda un detalle menor para la pasada de coherencia final: el campo **Documentación anexa** de las 21 especificaciones. Desde ESPECIFICACIONES 1.3 (28/10) las cuatro filas de prototipo de interfaz (CU0001, CU0002, CU0004 y CU0009) apuntan a las pantallas del `Prototipo de Interfaces`; siguen en «Pendiente» las de API y plantilla de correo de los casos de uso fuera del alcance. Falta además el encabezado de versión de `DIA1_REQUISITOS_MiBlog.md` (riesgo 4 de §7).
 
### 1.2 El stack, ya decidido
 
Python 3 · Flask · plantillas Jinja2 · hojas de estilo propias · SQLite por `sqlite3` · Linux.
Sin ORM, sin framework de frontend, sin servidor de aplicaciones de producción. El acceso a datos se encapsula en un módulo con SQL parametrizado. Dos dependencias declaradas en `REQUISITOS_NO_FUNCIONALES_MiBlog.md` §8.0: Flask y `python-dotenv`.
**No se cambia.** Tiene que aparecer igual en la arquitectura, el despliegue, los subsistemas, el plan de pruebas y el código.
 
---
 
## 2. El alcance: 10 casos de uso
 
De los 21 especificados, se **realizan** (análisis, diseño, código y pruebas) estos diez:
 
| CU | Nombre | Nota |
|---|---|---|
| CU0001 | Registrar Usuario | |
| CU0002 | Iniciar Sesión | |
| CU0003 | Cerrar Sesión | |
| CU0004 | Publicar Mensaje | |
| CU0005 | Editar Mensaje Propio | Agregado el 13/09 |
| CU0006 | Borrar Mensaje Propio | Agregado el 13/09 |
| CU0007 | Republicar Mensaje | Agregado el 13/09 |
| CU0009 | Visualizar Tablón | |
| CU0011 | Seguir Usuario | |
| CU0014 | Buscar Usuarios | Agregado el 13/09: es el punto de entrada de CU0011 |
 
Ejecutados en orden muestran el sistema entero funcionando: me registro, entro, busco a alguien, lo sigo, publico, edito, republico, borro y veo el resultado en el tablón. Eso se puede mostrar en vivo en la defensa.
 
Los otros once quedan especificados y ahí terminan su recorrido.
 
### 2.0 Tres consecuencias técnicas de los agregados
 
Hay que tenerlas presentes desde el Análisis, porque tocan casos de uso que ya estaban en alcance:
 
1. **CU0007 modifica CU0009.** El tablón deja de ser solo los mensajes de los seguidos y los propios: pasa a incluir también las republicaciones de unos y otros. La consulta se rehace.
2. **CU0006 borra en cascada.** Al eliminar un mensaje se eliminan sus republicaciones. **CU0005 no propaga nada**, porque la republicación referencia al mensaje original en lugar de copiar su texto: al editarlo, el cambio se ve solo.
3. **CU0014 es el punto de entrada de CU0011.** El tablón solo muestra a quienes ya se siguen, así que sin búsqueda no hay forma de alcanzar a un usuario nuevo y seguirlo. La pantalla de búsqueda lleva el botón "Seguir" en cada resultado.
### 2.1 La regla que ordena todo lo que falta
 
**Requisitos: los 21. Análisis, Diseño, Implementación y Prueba: solo los 10.**
 
### 2.2 Las tres excepciones
 
Estas tres cosas se hacen completas aunque solo se construyan 10 casos de uso, porque describen el sistema y no una operación:
 
- La **arquitectura** (las capas).
- El **diagrama de despliegue**.
- El **diagrama de subsistemas o paquetes**.
### 2.3 La frase que no puede faltar
 
Tiene que estar escrita en el documento de arquitectura y en el plan de pruebas:
 
> Esta iteración realiza los casos de uso CU0001, CU0002, CU0003, CU0004, CU0005, CU0006, CU0007, CU0009, CU0011 y CU0014. Los restantes quedan especificados en el flujo de Requisitos y no forman parte del alcance de implementación de esta versión.
 
Con esa frase, diez casos de uso son una decisión. Sin ella, son once que faltan.
 
---
 
## 3. Las cinco etapas
 
Un chat por etapa, siguiendo los flujos del Proceso Unificado. La Etapa 4 se subdivide en seis chats (§ETAPA 4).
 
| Etapa | Flujo del PU | Estado |
|---|---|---|
| 1 | Requerimientos | **Cerrada** el 13/09/2026 (prototipos incluidos, 14/09) |
| 2 | Análisis | **Cerrada** el 14/09/2026 — `ANALISIS_MiBlog.md` 2.2 |
| 3 | Diseño | **Cerrada** el 15/09/2026 — `DISEÑO_MiBlog.md` 1.4 (28/10) |
| 4 | Implementación | **Cerrada** el 28/10/2026, en seis bloques. **4.1 y 4.2 cerrados el 24/10, 4.3 el 26/10, 4.4 y 4.5 el 27/10 y 4.6 el 28/10** (los 10 casos de uso funcionando y el código cerrado) |
| 5 | Prueba | Pendiente. **Siguiente** |
| — | Cierre y defensa | Pendiente |
 
---
 
# ETAPA 1 — REQUERIMIENTOS
 
## Estado
 
**Cerrada.**
 
- Las correcciones al documento de especificaciones: aplicadas y verificadas.
- La decisión tecnológica: tomada el 13/09 (sección 8 de los requisitos no funcionales). **Python 3 + Flask + plantillas Jinja2 + SQLite sobre Linux**, sin ORM ni framework de frontend, con módulo de acceso a datos y SQL parametrizado.
- El alcance: cerrado en 10 casos de uso.
- Los prototipos: siete vistas, en `Prototipo de Interfaces.pdf` (actualizado el 28/10 al diseño visual implementado).
---
 
# ETAPA 2 — ANÁLISIS
 
## Estado
 
**Cerrada el 14/09/2026.** Todo en `ANALISIS_MiBlog.md`, hoy en versión 2.2 por las correcciones que pidió el Diseño.
 
- Los cuatro entregables producidos: 23 clases de análisis, diagrama de clases, diagrama de paquetes y los diez diagramas de colaboración con mensajes numerados.
- Cinco decisiones de modelado tomadas y documentadas (§1 de ese archivo).
- **Un entregable extra que no estaba previsto acá:** la evaluación de los patrones de diseño (§8). Los cuatro patrones que este plan proponía para la Etapa 3 se apoyaban en casos de uso fuera de alcance, así que se reemplazaron por cuatro con anclaje real. **La lista de patrones candidatos de la Etapa 3 de este plan quedó obsoleta: la que vale es `ESTADO_MI_PROYECTO.md` §5.1.**
## Teoría para la defensa
 
Flujo de Análisis: para qué sirve, qué trabajadores intervienen (Arquitecto, Ingeniero de Casos de Uso, Ingeniero de Componentes), en qué actividades. La diferencia entre análisis y diseño. Por qué existen los tres estereotipos.
Dónde está: `Ingeniería_de_Software.pdf` págs. 17–25 · `Resumen_Proceso_Unificado_54_pags.pdf` §7.
 
---
 
# ETAPA 3 — DISEÑO
 
## Estado
 
**Cerrada el 15/09/2026.** Todo en `DISEÑO_MiBlog.md`, hoy en versión 1.4 (la 1.3 corrigió la §2.4 por la estructura real del repositorio y la 1.4 pasó al diseño los desvíos DV-4 a DV-8 del código: el diagrama de clases suma miembros de apoyo y una nota, y ningún nombre cambió), en estado `[DECIDIDO]`.
 
- Los seis artefactos producidos, con los 17 diagramas en PlantUML compilados y su imagen (la de `clases.png` hay que regenerarla por la versión 1.4: P-18). El de subsistemas tiene dos vistas: se entrega la de paquetes anidados por capa, en el formato que usan los demás proyectos de la cátedra.
- **Los diez casos de uso se realizan.** No hubo que forzar ningún diagrama.
- **Doce hallazgos, los doce resueltos.** Seis decisiones confirmadas: H1 (tabla `sesiones`, con limpieza de las vencidas), H2 (`analizar(texto)`), H5 (`ca 7.1` alcanzable), H7 (se conserva `Usuario.activo`), H9 (diálogos como páginas) y H10 (`python-dotenv`). Los otros seis eran correcciones y quedaron aplicadas.
- **Documentos anteriores corregidos** antes de abrir la Etapa 4: `ESPECIFICACIONES_CASOS_DE_USO_MiBlog.md` 1.2, `ANALISIS_MiBlog.md` 2.2 y `REQUISITOS_NO_FUNCIONALES_MiBlog.md` 1.1.
- **Un entregable de más respecto de lo previsto:** la §9 del documento, con lo que la Etapa 4 recibe ya decidido (carpetas, rutas, esquema SQL, excepciones, dependencias y seis comprobaciones mecánicas).
## Teoría para la defensa
 
Flujo de Diseño: trabajadores y actividades. Qué es una realización de caso de uso. Por qué el análisis es el "qué" y el diseño el "cómo". Qué son los mecanismos genéricos de diseño.
Dónde está: `Ingeniería_de_Software.pdf` págs. 26–42 · `Notes_251125_135315.pdf` pág. 9.
 
---
 
# ETAPA 4 — IMPLEMENTACIÓN
 
**Cerrada el 28/10/2026** (empezó el 23/10). Se hizo **en chats de este proyecto, no en Claude Code.**
 
## Por qué en el chat y no en Claude Code
 
La recomendación original era Claude Code, cuando el plazo era de cuatro días: trabaja directo sobre el repositorio, crea los archivos y hace los commits. Con la entrega el 24/11 ese argumento dejó de aplicar, y pesa más otro: **en la defensa hay que poder explicar el código**. Escribirlo archivo por archivo es más lento, pero es lo que permite contestar.
 
**El costo, dicho claro.** Son unos cuarenta archivos que hay que copiar al editor a mano. Y todo lo que Claude Code hace solo lo hace Abel: crear el entorno virtual, instalar, arrancar el servidor, leer el error y traerlo al chat. Esa última parte es la que más enseña.
 
## Por qué seis chats y no uno
 
Un solo chat no entra con cuarenta archivos más los documentos de diseño. Se queda sin espacio y empieza a olvidar lo que escribió al principio, que es justo cuando aparecen las incoherencias.
 
Cada bloque termina en algo que **se puede correr y probar**. No se pasa al siguiente hasta que el anterior arranca.
 
| Chat | Qué se construye | Al terminar, funciona | Estado |
|---|---|---|---|
| **4.1 Cimientos** | Estructura de carpetas, `.gitignore`, `.env`, `requirements.txt`, `conexion.py`, `esquema.sql`, entidades del dominio y errores de negocio, `crear_app()` mínimo, `estilos.css`, plantilla base | El servidor arranca y muestra una página; la base se crea con el comando `iniciar-bd` | **Cerrado 24/10** |
| **4.2 Sesión** | CU0001, CU0002, CU0003 · `ControlRegistro`, `ControlAutenticacion`, `GuardiaSesion`, `RepositorioUsuarios`, `RepositorioSesiones`, `AlmacenFotos` y sus cuatro plantillas | Registrarse, entrar y salir | **Cerrado 24/10** |
| **4.3 Relaciones** | CU0014, CU0011 · `ControlBusquedaUsuarios`, `ControlSeguimiento`, `RepositorioSeguimientos`, `busqueda.html` | Buscar un usuario y seguirlo | **Cerrado 26/10** |
| **4.4 Mensajes y tablón** | CU0004, CU0009 · `OperacionSobreMensaje`, `Publicacion`, `AnalizadorDeTexto`, los tres extractores, `ControlTablon`, `RepositorioMensajes`, `RepositorioElementos`, `RepositorioRepublicaciones`, `tablon.html`, `contador.js` | Publicar un mensaje y verlo en el tablón | **Cerrado 27/10** |
| **4.5 Edición y republicación** | CU0005, CU0006, CU0007 · `Edicion`, `ControlRepublicacion`, los dos diálogos | Editar, borrar y republicar | **Cerrado 27/10** |
| **4.6 Cierre del código** | Manejo de errores y registro (`errores_web.py`, `error.html`), forma del nombre de usuario, franja de marca, pruebas de la sesión y de las relaciones, `README.md` final con los límites conocidos, las seis comprobaciones mecánicas de `DISEÑO_MiBlog.md` §2.7, DV-4 a DV-8 al diseño y `diagnostico.py` borrado | El repositorio queda entregable | **Cerrado 28/10** |
 
**4.3 va antes que 4.4 a propósito:** el tablón necesita saber a quién sigue el usuario, así que `RepositorioSeguimientos` tiene que existir antes.
 
**Lo que se adelantó del 4.6 al 4.4 (27/10):** las pruebas automáticas con `unittest` en `pruebas/` (83 al cerrar el 4.4, 183 al cerrar el 4.5 y 262 al cerrar el 4.6, D-27 y D-41), la herramienta `sembrar_datos.py` para llenar la base con datos de demostración (D-31) y un `README.md` completo (D-32). El 4.5 las amplió y el 4.6 las completó con las de la sesión, las relaciones y los errores.
 
**Los cuatro patrones aparecen en 4.4 y 4.5.** Strategy y Factory Method en el analizador y los extractores; el esqueleto del Template Method en `OperacionSobreMensaje`; el Decorator al armar el tablón. Son los dos chats donde más hay que respetar la estructura de `ANALISIS_MiBlog.md` §8.3 a §8.5.
 
## Cómo se transmite el estado de un bloque al siguiente
 
**El problema.** Cada chat empieza sin memoria. Lo único que el chat nuevo sabe del anterior es lo que está escrito en los documentos de este proyecto. Si el bloque 4.2 cambia un nombre o toma una decisión y nadie la anota, el 4.3 la desconoce y el código se bifurca.
 
**La solución, en tres piezas.**
 
1. **`CONTEXTO_IMPLEMENTACION_MiBlog.md`** es el documento de traspaso. Dice qué se construyó de verdad, qué se decidió al programar (D-xx), qué cambió respecto del diseño (DV-x), qué quedó abierto (P-x) y cómo comprobar que el bloque anterior sigue andando. Es chico a propósito: no repite el diseño, solo lo que se aparta de él.
2. **El prompt común** de abajo obliga a leerlo primero y a confirmar lo entendido antes de escribir código.
3. **El informe de cierre** termina con las líneas listas para ese documento. Abel las pega, sube la versión y lo vuelve a subir **antes** de abrir el chat siguiente.
Los tres documentos que un chat de Implementación tiene que haber leído, en este orden: `00_INDICE.md` → `CONTEXTO_IMPLEMENTACION_MiBlog.md` → `ESTADO_MI_PROYECTO.md`, y después del diseño solo lo que pide el bloque.
 
## El aspecto visual del frontend
 
El **prototipo de interfaces** (`Prototipo de Interfaces.pdf`, 14/09) es el artefacto de Requisitos: fija **qué elementos tiene cada vista y cómo se navega entre ellas**. Eso no se discute en la Implementación.
 
El **aspecto visual** —paleta, tipografía, espaciado, forma de los componentes— se trabaja aparte, con Claude Design, y entra al código como insumo del bloque 4.1, que es donde se escriben `estilos.css` y la plantilla base. **Hecho el 24/10**: el resultado y las clases que existen están descriptos en `CONTEXTO_IMPLEMENTACION_MiBlog.md` §4. El 28/10 se sumó la franja de marca de las dos pantallas sin sesión (D-43) y el prototipo de interfaces se actualizó al diseño implementado.
 
**Cómo entra, y cómo no.** De un diseño generado se toma la **decisión visual**, no el código:
 
- **Sí:** colores en hexadecimal, familia y tamaños tipográficos, escala de espaciado, radios de borde, sombras, y cómo se ve cada componente (tarjeta de mensaje, botón, campo de formulario, barra superior). **Las fuentes se incluyen como archivos del proyecto** (`presentacion/estaticos/fuentes/`), con su licencia, y se declaran con `@font-face`.
- **No:** Tailwind ni ninguna hoja de estilos o fuente por CDN, variables de un framework, JavaScript de ningún tipo, ni HTML pegado tal cual. El stack es **CSS propio escrito a mano** y `RNF31` limita el JavaScript al contador de caracteres. Una dependencia nueva sin declarar en `REQUISITOS_NO_FUNCIONALES_MiBlog.md` §8.0 es una incoherencia entre documento y código.
- Las clases de CSS que se definan en 4.1 tienen que **alcanzar a las siete vistas**, no solo a la primera, porque los bloques 4.2 a 4.5 reutilizan esa hoja.
**El riesgo a vigilar:** que el diseño visual traiga **pantallas, campos o acciones que el prototipo y las especificaciones no tienen** (un panel de tendencias, un botón de dejar de seguir, un perfil de usuario). Si eso pasa, no se programa de más: o se descarta el agregado, o se actualizan el prototipo y las especificaciones. Lo que no puede quedar es un código que ofrezca algo que ningún caso de uso especifica. Ver riesgo 7 de §7.
 
## Antes de abrir el chat 4.1
 
Tres cosas listas en la máquina: Python 3 instalado, el repositorio de Git creado, y saber abrir una terminal en la carpeta del proyecto.
 
## Reglas de los seis chats
 
- Estructura en capas, según `DISEÑO_MiBlog.md` §2.4. **El árbol del diseño está dentro de `4. Implementacion/codigo/`** (ver `CONTEXTO_IMPLEMENTACION_MiBlog.md` §2).
- **Los nombres de clases, métodos y rutas ya están decididos.** Si uno cambia, se cambia **en el diagrama el mismo día** (riesgo 5 de §7). Mientras el diagrama no se actualice, el cambio se anota en el documento de contexto.
- **Si un patrón no llega al código, se saca del diagrama el mismo día.** Template Method y Strategy son los que más fácil se degradan; las señales están en `ANALISIS_MiBlog.md` §8.8.
- Secretos en `.env`. El `.env`, `instance/` y la carpeta de fotos van en `.gitignore`. En el repositorio del compañero había credenciales reales de Gmail commiteadas; eso no se copia.
- Un commit por bloque terminado, con mensaje descriptivo en formato `Etapa: descripción`. El historial forma parte de la gestión de configuración. (En 4.2 a 4.6 el bloque se partió en varios commits, por capa; ver `CONTEXTO_IMPLEMENTACION_MiBlog.md` §2.)
- `requirements.txt` con **Flask y `python-dotenv`, y nada más**. Si hace falta otra dependencia, primero se agrega a `REQUISITOS_NO_FUNCIONALES_MiBlog.md` §8.0 con su motivo.
- **Cada bloque deja sus pruebas automáticas** en `4. Implementacion/codigo/pruebas/` (`unittest`, sin dependencia nueva; D-27), y **la suite completa tiene que pasar antes de cerrar el bloque**: `python -m unittest discover -s pruebas -t .` desde `codigo/`. Es la regla 12 de `CONTEXTO_IMPLEMENTACION_MiBlog.md` §1.
- **Cada bloque cierra con su informe** (§Informe de cierre), que se trae al chat general y se pega en el documento de contexto.
## Prompts
 
**Bloque común, al principio de los seis:**
 
```
Leé, en este orden: 00_INDICE.md, CONTEXTO_IMPLEMENTACION_MiBlog.md,
ESTADO_MI_PROYECTO.md, DISEÑO_MiBlog.md, ANALISIS_MiBlog.md y
ESPECIFICACIONES_CASOS_DE_USO_MiBlog.md.
 
Proyecto MiBlog: sistema de microblogging para empleados de una
empresa. Trabajo académico de Ingeniería de Software que se entrega con
defensa oral, donde me pueden pedir que explique el código y que muestre
su correspondencia con el diseño. Lo escribo yo, archivo por archivo, en
el chat: no uso Claude Code. Soy estudiante: explicame primero la idea
de lo que sea complicado y después el detalle.
 
Stack cerrado: Python 3, Flask, plantillas Jinja2, hojas de estilo
propias, SQLite por sqlite3, python-dotenv. Sin ORM, sin framework de
frontend. La única lógica en el navegador es el contador de caracteres.
 
CONTEXTO_IMPLEMENTACION_MiBlog.md te dice qué ya está construido, qué
decisiones se tomaron al programar y en qué se apartó el código del
diseño. Donde ese documento y el diseño se contradicen, manda el
documento de contexto (§5 y §6). Antes de escribir código, decime en
cinco líneas qué entendiste del estado: qué bloques están cerrados, qué
desvíos rigen y qué pendientes le tocan a este bloque. Después pedime
que corra la comprobación de la sección 7 de ese documento.
 
Reglas para todo lo que escribas:
- Respetá los nombres de clases, métodos y rutas de DISEÑO_MiBlog.md §2.5
  y §3. No los renombres por preferencia de estilo.
- Estructura de carpetas de DISEÑO_MiBlog.md §2.4, dentro de
  4. Implementacion/codigo/.
- SQL solo dentro de acceso_datos, siempre parametrizado.
- Dame los archivos de a uno, con la ruta completa arriba y el contenido
  entero, listo para copiar. No me des fragmentos sueltos.
- Después de cada archivo, explicame en dos o tres frases qué hace y por
  qué está así, con referencia a la sección del diseño de la que sale.
- Al terminar el bloque, decime exactamente qué comandos tengo que correr
  para probarlo y qué tendría que ver si funciona.
- Si algo del diseño no se puede programar tal como está, decímelo en vez
  de improvisar una solución distinta.
- Reutilizá las clases de estilos.css que ya existen; si hace falta una
  nueva, agregala a esa misma hoja y decímelo.
```
 
**4.1 Cimientos** — agregar al bloque común. *(Ya hecho el 24/10; se conserva como referencia.)*
 
```
Bloque 4.1: los cimientos. Todavía sin ningún caso de uso.
 
Construimos: la estructura de carpetas completa (§2.4), .gitignore,
.env de ejemplo, requirements.txt, acceso_datos/conexion.py con la
conexión por petición, transaccion(), normalizar() e inicializar_base();
acceso_datos/esquema.sql tal como está en §2.6; todas las clases de
logica/dominio (entidades, enumeraciones y las 14 excepciones de
negocio); miblog/__init__.py con un crear_app() mínimo; estilos.css y la
plantilla base.
 
Sobre el aspecto visual: te paso aparte el diseño que armé con Claude
Design. De ahí se toman solo las decisiones visuales (colores,
tipografía, espaciado, radios, sombras y cómo se ve cada componente) y
se escriben a mano en estilos.css, con variables CSS en :root. NO se
usa Tailwind, ni hojas por CDN, ni JavaScript, ni se pega el HTML
generado: el stack es CSS propio y el RNF31 limita el JavaScript al
contador de caracteres. Las clases que definas tienen que servir para
las siete vistas del prototipo, no solo para la primera, porque los
bloques siguientes reutilizan esta hoja. Si el diseño trae pantallas,
campos o acciones que el prototipo no tiene, avisame en vez de
programarlos.
 
Al terminar quiero poder: crear la base con el comando de Flask y
arrancar el servidor y ver una página, aunque esté casi vacía.
 
Empezá explicándome qué es un entorno virtual y cómo lo creo, porque es
la primera vez que armo un proyecto así.
```
 
**4.2 Sesión:**
 
```
Bloque 4.2: CU0001 Registrar Usuario, CU0002 Iniciar Sesión y CU0003
Cerrar Sesión. Las secuencias están en DISEÑO_MiBlog.md §6.1, §6.2 y §6.3.
 
Construimos: RepositorioUsuarios, RepositorioSesiones, AlmacenFotos,
ControlRegistro, ControlAutenticacion, GuardiaSesion, las vistas de
registro, inicio de sesión y confirmación de cierre, y sus plantillas.
Reemplazamos la ruta provisoria GET / y borramos inicio_provisorio.html.
 
Tené presente el hallazgo H1 del diseño: la sesión no es la cookie de
Flask sola. Se guarda una fila en la tabla sesiones con el hash SHA-256
del token, y se borra al cerrar sesión y cuando vence.
 
CU0003 sigue el diseño (decisión D-11 del documento de contexto):
GET /sesion/cerrar muestra una confirmación, sin barra, y el POST
invalida la sesión y redirige a /. No hay pantalla "Cerraste sesión".
 
Reutilizá las clases de estilos.css que ya existen; si hace falta una
nueva, agregala a esa misma hoja y decímelo. La barra superior aparece
solo con sesión iniciada (decisión D-08).
 
Al terminar quiero poder registrarme, entrar y salir.
```
 
**4.3 Relaciones:**
 
```
Bloque 4.3: CU0014 Buscar Usuarios y CU0011 Seguir Usuario. Las
secuencias están en DISEÑO_MiBlog.md §6.10 y §6.9.
 
Construimos: RepositorioSeguimientos, ControlBusquedaUsuarios,
ControlSeguimiento, VistaBusquedaUsuarios y busqueda.html.
 
Dos cosas del diseño: la búsqueda ignora mayúsculas y acentos con la
función normalizar() registrada en SQLite, y los resultados NO muestran
el correo. A quien ya sigo se lo marca con la etiqueta "Siguiendo", sin
botón, porque "Dejar de seguir" es CU0012 y está fuera de alcance.
 
Al terminar quiero poder buscar a un usuario y seguirlo.
```
 
**4.4 Mensajes y tablón:** *(Ya hecho el 27/10; se conserva como referencia.)*
 
```
Bloque 4.4: CU0004 Publicar Mensaje y CU0009 Visualizar Tablón. Las
secuencias están en DISEÑO_MiBlog.md §6.4 y §6.8. Es el bloque con más
patrones.
 
Construimos: AnalizadorDeTexto con los tres extractores (Strategy y
Factory Method), OperacionSobreMensaje y Publicacion (Template Method),
ControlPublicacion, ControlTablon, RepositorioMensajes,
RepositorioElementos, RepositorioRepublicaciones, VistaTablon,
tablon.html y contador.js.
 
Los patrones tienen que existir de verdad, no solo en el diagrama. La
estructura mínima que exige cada uno está en ANALISIS_MiBlog.md §8.3,
§8.4, §8.5 y §8.8, con sus señales de degradación. Dos en concreto:
- AnalizadorDeTexto recibe los extractores por constructor y no nombra
  ninguna clase concreta.
- El límite de 140 aparece una sola vez en todo el código, en
  OperacionSobreMensaje.LIMITE.
 
contador.js es el único JavaScript del proyecto (RNF31): que no se le
sume nada más.
 
Al terminar quiero poder publicar un mensaje con #etiquetas, @menciones
y un link, y verlo en el tablón junto con los de la gente que sigo.
```
 
**4.5 Edición y republicación:** *(Ya hecho el 27/10; se conserva como referencia.)*
 
```
Bloque 4.5: CU0005 Editar, CU0006 Borrar y CU0007 Republicar. Las
secuencias están en DISEÑO_MiBlog.md §6.5, §6.6 y §6.7.
 
Construimos: Edicion (la segunda clase concreta del Template Method),
los métodos de borrado de ControlPublicacion, ControlRepublicacion,
DialogoEdicionMensaje y DialogoConfirmacionBorrado con sus plantillas.
 
Cuatro cosas del diseño:
- Los diálogos son páginas propias con su ruta, no ventanas flotantes:
  no hay JavaScript para eso (hallazgo H9). El aspecto de recuadro
  centrado sobre fondo oscurecido se logra con CSS.
- Borrar elimina en cascada las republicaciones, y primero esas.
- Editar no propaga nada: la republicación muestra el texto nuevo porque
  lo delega en el original (Decorator). En el código no tiene que haber
  ningún isinstance ni ningún if por tipo, tampoco en la plantilla.
- El botón Republicar aparece en todo elemento cuyo autor original no
  sea yo, y decide el servidor (hallazgo H5).
 
Estado que heredás del 4.4: CONTEXTO_IMPLEMENTACION_MiBlog.md §4.6 dice
qué piezas quedaron a medias a propósito (ControlPublicacion solo
publica, a los repositorios de mensajes y de republicaciones les faltan
métodos, tablon.html todavía no tiene botones) y qué hace este bloque
con cada una. Las pruebas del 4.4 están en pruebas/ (83, §4.5 del
contexto): agregá las de este bloque (Edicion, el borrado en cascada,
ControlRepublicacion con ca 7.1 a 7.4, las rutas de los dos diálogos y
el caso directo del Decorator: editar un mensaje republicado y ver que
la republicación muestra el texto nuevo), dejá las 83 pasando y
actualizá el README.md (editar, borrar y republicar pasan de «En
desarrollo» a «Disponible»).
 
Al terminar quiero poder editar, borrar y republicar.
```
 
**4.6 Cierre del código:** *(Ya hecho el 28/10; se conserva como referencia.)*
 
```
Bloque 4.6: cerrar el código.
 
Las pruebas unitarias y un primer README.md ya se hicieron en el 4.4
(carpeta pruebas/ y README.md; decisiones D-27 y D-32) y el 4.5 las
amplió. Acá las revisamos y cerramos lo que falta:
- Correr la suite completa y decirme cuántas pruebas hay y si pasan.
- Revisar que el README.md final cuente lo que hace el programa con los
  diez casos de uso, y que no mande a otros archivos (D-32).
- Decidir conmigo los pendientes del documento de contexto que le
  tocan a este bloque: manejo de errores (P-8), formato del nombre de
  usuario (P-11) y cuáles limitaciones conocidas se arreglan y cuáles
  se declaran (P-13). También los comentarios «Bloque 4.x» que quedan
  en seis archivos (P-17): se sacan.
 
Después corremos las seis comprobaciones mecánicas de DISEÑO_MiBlog.md
§2.7 sobre el repositorio y me decís, una por una, si pasa o no. Si
alguna falla, hay que arreglar el código o sacar el patrón del diagrama;
no se deja un diagrama que muestre algo que el código no tiene.
 
Después pasamos al diseño los desvíos nuevos que el documento de
contexto tenga anotados en la sección 6.1 (DV-1 a DV-3 ya están en el
diseño 1.3; quedan DV-4, DV-5, DV-6 y DV-7), para que DISEÑO_MiBlog.md y el
código digan lo mismo.
 
Antes de entregar: borrar diagnostico.py y instance/diagnostico.log, y
comprobar que no hay ningún secreto commiteado (la única clave del
repositorio es demo-1234, la de las cuentas de demostración de
sembrar_datos.py, que es pública y de mentira).
 
Al final, dame la lista de en qué archivo vive cada uno de los diez casos
de uso: la necesito para la matriz de trazabilidad del cierre.
```
 
## Informe de cierre de cada bloque
 
Se pega al final de cada uno de los seis chats. Lo que devuelve se lleva al chat general, que es el que coordina y el que indica qué documentos hay que actualizar, y **se pega también en `CONTEXTO_IMPLEMENTACION_MiBlog.md`**.
 
```
Cerramos el bloque. Dame un informe de cierre con estos seis puntos, en
este orden y sin código:
 
1. ARCHIVOS. Lista de los archivos que escribimos, con su ruta completa.
   Marcá cuáles son nuevos y cuáles modificaste de un bloque anterior.
 
2. CASOS DE USO. Cuáles quedaron implementados y en qué archivos vive
   cada uno. Si alguno quedó a medias, decí qué falta.
 
3. DESVÍOS DEL DISEÑO. Cualquier cosa que no salió como decía
   DISEÑO_MiBlog.md: un nombre de clase, método o ruta que cambiamos,
   una decisión distinta, algo que el diseño no contemplaba o que no se
   podía programar tal cual. Si no hubo ninguno, decilo explícitamente.
 
4. PATRONES. De los cuatro (Strategy, Factory Method, Decorator,
   Template Method), cuáles toca este bloque y si quedaron con la
   estructura que pide ANALISIS_MiBlog.md §8.3 a §8.5, o si se
   degradaron. Si ya se puede correr alguna de las seis comprobaciones
   de DISEÑO_MiBlog.md §2.7, correla y decime el resultado.
 
5. DEPENDENCIAS. Si requirements.txt cambió, cuál se agregó y por qué.
 
6. ESTADO. Si el bloque arranca y funciona, qué probaste para
   confirmarlo, cuántas pruebas automáticas tiene ahora la suite y si
   pasan todas, si commiteaste, y qué quedó pendiente.
 
Después del informe, dame las líneas listas para actualizar
CONTEXTO_IMPLEMENTACION_MiBlog.md: la fila nueva de su sección 3, los
archivos nuevos de la 4.1, las decisiones nuevas con el siguiente
número D-xx, los desvíos nuevos DV-x, los pendientes resueltos o
nuevos, la tabla de comprobaciones de la sección 7 actualizada y este
mismo informe para la sección 9.
```
 
**Por qué estos seis.** El punto 3 es el que más fácil se omite y el que más caro sale: si en 4.4 se renombra un método porque quedaba más cómodo y nadie lo registra, el diagrama de clases y el código se separan en silencio, y eso aparece en la defensa cuando pidan mostrar la correspondencia. El punto 2 es la columna de código de la matriz de trazabilidad: juntándolo bloque por bloque, el cierre sale en una hora; dejándolo para el final, hay que reconstruirlo leyendo cuarenta archivos. El punto 4 decide si un patrón se queda en el diagrama o se saca, y esa decisión se toma en el día.
 
**Qué NO va al chat general:** el código completo de cada archivo, y los errores de ejecución. Los errores se resuelven en el chat del bloque, que tiene el código fresco; solo se llevan al general si revelan un problema del diseño y no del código. Un archivo suelto sí se puede traer, cuando hay dudas de si respeta el diseño.
 
---
 
# ETAPA 5 — PRUEBA
 
## Entregables
 
1. **Plan de pruebas**: alcance, qué se prueba, niveles, herramientas, criterios de éxito, ambiente.
2. **Casos de prueba** de los 10 casos de uso, en tabla: Id, Objetivo, Estado Inicial, Datos de Prueba, Resultado Esperado. Que cubran el curso normal **y** los cursos alternativos ya especificados.
3. **Procedimientos de prueba**: pasos numerados y ejecutables.
## Restricciones
 
- Herramientas y ambiente reales del stack. El proyecto de referencia puso JUnit en un proyecto Python y un ambiente "Windows 7 con Chrome 22".
- Los casos de prueba tienen que verificar los `rnf` que escribiste en las especificaciones. Si prometiste un tiempo de respuesta, tiene que haber un caso que lo mida.
- La frase de alcance de §2.3 va también en este documento. **Tal como está escrita y nada más:** el plan de pruebas **no** debe decir que la cátedra aceptó, autorizó o acordó el alcance reducido, porque no lo hizo. Si hace falta explicar de quién es la decisión, el texto es el de `DIA1_REQUISITOS_MiBlog.md` §7.0: decisión propia del alumno, con su fundamento. Esa afirmación falsa estuvo seis semanas en cuatro documentos y se corrigió el 28/10/2026; que no vuelva a entrar por un documento nuevo.
- Tres casos que el Diseño dejó anotados (`ESTADO_MI_PROYECTO.md` §9.1): el `ca 7.1` **por interfaz** con una republicación de un seguido, un **usuario con `activo = 0`** en los datos de prueba, y el `ca 7.4` de mensaje borrado antes de republicar.
- El **rnf 9.3** (tablón en menos de 3 segundos «con el juego de datos de prueba definido para el proyecto») ya tiene una prueba automática con el volumen del bloque 4.4: 100 usuarios, 5.000 mensajes, 500 republicaciones y 20 seguidos (D-30). El Plan de pruebas tiene que **declarar ese volumen** y definir el juego de datos; `sembrar_datos.py` puede servir de base (P-15, no decidido).
- Las **pruebas automáticas de `codigo/pruebas/`** (`unittest`, 262 al cerrar el 4.6) citan en sus nombres los `ca` y `rnf` que verifican. Se mapean a los casos de prueba y se declaran en el Plan como el nivel automatizado; **no reemplazan** al Plan, los Casos ni los Procedimientos, que son documentos.
- **El código está cerrado** (28/10/2026). Los **límites conocidos** del `README.md` (D-39) son comportamiento declarado: ningún caso de prueba debe esperar otro. Si una prueba encuentra un defecto, se corrige y se anota en `CONTEXTO_IMPLEMENTACION_MiBlog.md`.
- Lo que el 4.6 agregó y también hay que mapear: la forma del nombre de usuario (`rnf 1.1`, `{Ob 1.3}`, D-38) y las páginas de error con el archivo de registro (RNF16 y RNF24, D-37 y D-42).
## Teoría para la defensa
 
Flujo de Prueba: trabajadores, los tipos de casos de prueba, qué se especifica en un caso de prueba, prueba de caja negra y de caja blanca.
Dónde está: `Ingeniería_de_Software.pdf` págs. 53–61.
 
## Prompt
 
```
Leé 00_INDICE.md, CONTEXTO_IMPLEMENTACION_MiBlog.md,
PLAN_DEL_PROYECTO.md, ESPECIFICACIONES_CASOS_DE_USO_MiBlog.md y lo
producido en Diseño e Implementación.
 
Etapa 5: flujo de PRUEBA. Solo sobre los 10 casos de uso realizados.
 
Entregables:
1. Plan de pruebas: introducción y alcance, elementos incluidos,
   funcionalidades a probar con los IDs de casos de prueba, niveles y
   estrategia, herramientas, criterios de éxito, entregables, ambiente.
2. Casos de prueba en tabla Id / Objetivo / Estado Inicial / Datos de
   Prueba / Resultado Esperado, cubriendo el curso normal Y los cursos
   alternativos que ya están especificados en cada caso de uso.
   Encadenalos ("Estado inicial: se ejecutó con éxito el CP x.y") y usá
   datos concretos, no placeholders.
3. Procedimientos de prueba: pasos numerados y ejecutables.
 
Restricciones:
- Herramientas y ambiente reales de mi stack.
- Los casos tienen que verificar los rnf que escribí en las
  especificaciones. Si un rnf no se puede verificar, decímelo.
- Incluí la frase de alcance de la iteración
  (PLAN_DEL_PROYECTO.md §2.3), tal como está escrita. NO digas que la
  cátedra aceptó, autorizó o acordó el alcance reducido: no lo hizo. Si
  hace falta decir de quién es la decisión, es del alumno, y el texto
  está en DIA1_REQUISITOS_MiBlog.md §7.0.
- Ya existen pruebas automáticas en 4. Implementacion/codigo/pruebas/
  (unittest, 262 al cerrar el 4.6): mapealas a los casos de prueba en vez
  de ignorarlas, y declará en el Plan el volumen de datos del rnf 9.3
  (CONTEXTO D-30).
- El código está cerrado. Los límites conocidos del README.md (CONTEXTO
  D-39) son comportamiento declarado: no los trates como defectos.
 
Al final: los tipos de casos de prueba según el PU, qué se especifica
en un caso de prueba, y la diferencia entre caja negra y caja blanca.
```
 
---
 
# CIERRE — Trazabilidad, coherencia y defensa
 
No se saltea. Es lo que convierte un montón de documentos en un proyecto.
 
## Entregables
 
1. **Matriz de trazabilidad**: requisito del enunciado → caso de uso → clase de diseño → archivo de código → caso de prueba. Los requisitos que no llegaron a código quedan visibles como tales.
2. **Pasada de coherencia** sobre todo lo entregado.
3. **Preparación de la defensa.**
## Prompt
 
```
Leé 00_INDICE.md, CONTEXTO_IMPLEMENTACION_MiBlog.md,
PLAN_DEL_PROYECTO.md y todo lo producido en las cinco etapas.
 
Cierre del proyecto. Tres cosas:
 
1. MATRIZ DE TRAZABILIDAD en tabla: requisito del enunciado (R00-R17)
   → caso de uso → clase de análisis → clase de diseño → archivo de
   código → caso de prueba. Los requisitos que no llegaron a código
   deben quedar visibles como tales, no disimulados.
 
2. PASADA DE COHERENCIA. Reportame como lista de hallazgos:
   - Misma tecnología en arquitectura, despliegue, subsistemas, plan de
     pruebas y código.
   - La frase de alcance de la iteración presente en arquitectura y en
     el plan de pruebas.
   - Estados de los diagramas coherentes con el modelo de dominio.
   - Correspondencia real entre clases de análisis, de diseño,
     secuencias y código.
   - Ningún rnf con un número que ningún caso de prueba verifique.
   - Los 21 casos de uso presentes en el diagrama único.
   - Las 6 comprobaciones mecánicas de DISEÑO_MiBlog.md §2.7 sobre el
     repositorio.
   - Que los desvíos DV-x del documento de contexto estén pasados a
     DISEÑO_MiBlog.md.
   - El campo "Documentación anexa" de las 21 especificaciones.
   - El encabezado de versión de DIA1_REQUISITOS_MiBlog.md.
   - Que la interfaz no ofrezca ninguna acción que no esté especificada
     en algún caso de uso.
   Sé exigente. Prefiero diez problemas ahora que uno en la defensa.
 
3. PREPARACIÓN DE LA DEFENSA:
   a) Para cada artefacto: a qué flujo pertenece, qué trabajador lo
      produce, en qué actividad y qué decisión comunica.
   b) Respuestas a las preguntas incómodas de PLAN_DEL_PROYECTO.md §5.
   c) Preguntas teóricas probables sobre los temas que no aparecen en
      mi proyecto (modelos de proceso, calidad, métricas, gestión de
      configuración, las 4 P, fases vs flujos), con la respuesta breve
      y en qué resumen y página está.
 
No me tranquilices. Si algo está flojo o es indefendible, decímelo.
```
 
---
 
## 4. Qué se recorta si vas atrasado
 
Con la entrega el 24/11/2026 el tiempo dejó de ser el problema, así que esta lista pasó a ser un seguro y no un plan. **No se recorta nada mientras el cronograma alcance.** Si por algún motivo volviera a apretar, el orden es:
 
1. **Los tres agregados del 13/09**, en orden inverso: primero CU0005 Editar, después CU0006 Borrar, último CU0007 Republicar. Si se cae CU0007, el tablón vuelve a su forma simple y se ahorra también esa complicación.
2. Diagramas de estado: de dos a uno (queda Usuario).
3. Colaboraciones: de 10 casos de uso a 5 (quedan registro, login, buscar y seguir, publicar, tablón).
4. Prototipos: de siete vistas a cuatro.
5. Código: se cae CU0003 Cerrar Sesión.
6. Procedimientos de prueba: solo de los casos de uso implementados.
> Volver de 10 a menos no cuesta nada mientras la documentación siga diciendo lo que se realiza. Solo hay que actualizar la frase de §2.3 y las tablas de alcance. Eso es recortar; lo que no se puede es dejar la documentación prometiendo diez y entregar seis.
 
### Lo que no se recorta nunca
 
- La **frase de alcance** en arquitectura y plan de pruebas.
- El **diagrama de clases de diseño integral**.
- La **matriz de trazabilidad**.
- La **pasada de coherencia**.
---
 
## 5. Las preguntas incómodas de la defensa
 
**"¿Esto fue iterativo e incremental?"**
No. Fue **una sola iteración**, por restricción de tiempo y porque el trabajo estaba pensado para un grupo de ocho personas. El Proceso Unificado es iterativo por definición; en un desarrollo real la priorización de casos de uso decidiría qué entra en cada iteración. Acá la priorización existe y sirvió para decidir qué diez casos de uso se realizan.
 
**"¿Por qué implementaste 10 de 21?"**
Porque el Proceso Unificado es dirigido por casos de uso y cada caso de uso se propaga a todos los flujos. Con el tiempo disponible se eligió un subconjunto que, ejecutado en secuencia, demuestra el sistema de punta a punta: registrarse, entrar, buscar a alguien y seguirlo, publicar, editar, republicar, borrar y ver el tablón. El resto queda especificado, que es donde termina su recorrido en esta versión.
 
**"¿Por qué especificaste 21 si construís 10?"**
Porque el flujo de Requisitos describe el sistema, no la iteración. Recortarlo haría parecer que el relevamiento fue incompleto.
 
**"¿Dónde están los requisitos no funcionales y cómo se verifican?"**
En el documento global RNF01–RNF42, y en cada caso de uso como `rnf` locales que derivan de los globales y se referencian desde los pasos. Se verifican en los casos de prueba, salvo siete que se verifican por inspección del documento de arquitectura y están declarados como tales en la sección 10 de ese documento.
 
**"¿Cuál es la diferencia entre análisis y diseño en tu proyecto?"**
El ejemplo preparado es `AnalizadorDeTexto`: en análisis es una clase de control; en diseño son seis clases con Strategy y Factory Method, y además el diseño **corrigió** la firma del análisis (hallazgo H2). Está desarrollado en `DISEÑO_MiBlog.md` §8.3.
 
**"¿Cómo sabés que el código respeta el diseño?"**
Por tres cosas. Las seis comprobaciones mecánicas de `DISEÑO_MiBlog.md` §2.7, que se corren sobre el repositorio; esas mismas seis, que desde el bloque 4.4 corren solas como pruebas automáticas (`pruebas/test_reglas_de_arquitectura.py`) cada vez que se corre la suite; y la tabla de desvíos del documento de contexto, donde cada diferencia entre código y diseño quedó registrada, con su motivo, y se pasó al diseño (DV-1 a DV-8, todos en la versión 1.4). Un desvío que no está en esa tabla es un error, no una decisión.
 
**"¿Hay una clave en el repositorio?"**
Una sola, y es de mentira: `demo-1234`, la clave de las cuentas de demostración que crea `sembrar_datos.py`. Esas cuentas solo existen si alguien corre ese script, que pide confirmación escrita, y no dan acceso a nada real. Los secretos de verdad (`SECRET_KEY`) están en `.env`, que no se commitea: el repositorio solo trae `.env.example`, con valores de ejemplo. Las pruebas automáticas usan claves de juguete en bases temporales que se borran al terminar.
 
**"¿Por qué hay SQL fuera de `acceso_datos` en `sembrar_datos.py`?"**
Porque RNF25 y RNF40 rigen para la aplicación (`miblog/`) y `sembrar_datos.py` no forma parte de ella: es una herramienta de apoyo que vive afuera del paquete, no implementa ningún caso de uso y ninguna de las seis comprobaciones la mira. Los mensajes que carga sí pasan por las clases de la aplicación (`MensajePublico`, `RepositorioMensajes`, `AnalizadorDeTexto`); los usuarios, los seguimientos y las republicaciones los inserta con SQL propio.
 
**"¿Qué pasa si falla algo que no esperabas?"**
Hay dos clases de error. Los esperados son los cursos alternativos de cada caso de uso: la lógica lanza una excepción de negocio y la vista muestra el aviso. Los inesperados llegan a `errores_web.py`: la persona ve una página con un texto genérico, nunca el detalle técnico, y si es un 500 queda anotado en `instance/miblog.log` con fecha, hora, método, ruta y el recorrido del error, sin el formulario, porque podría traer una clave (RNF16 y RNF24, D-37 y D-42).
 
**"¿Qué cosas no hace la aplicación?"**
Están declaradas: 16 límites conocidos en la sección «Límites conocidos» del `README.md`, cada uno con su motivo (no hay paginación ni token contra CSRF, no se puede dejar de seguir, el doble clic en «Publicar» crea dos mensajes, entre otros). Ninguno es un error escondido: son decisiones de alcance (D-39).
 
**"El enunciado solo dice 15 caracteres para el nombre de usuario: ¿por qué tiene esa forma?"**
Porque sin una regla se podía registrar un nombre, con espacios o símbolos, que después nadie podría mencionar con `@`. La forma (letras, números y guion bajo; punto y guion solo en el medio) es un criterio propio: está en las especificaciones como `{Ob 1.3}` y no cambia el RNF02 (D-38).
 
---
 
## 6. Teoría que no sale de construir el proyecto
 
Estos temas están en los resúmenes y pueden salir en la defensa teórica, pero no se tocan en ninguna etapa. Repasar aparte:
 
- **Modelos de proceso**: cascada, prototipos, incremental, espiral → `ResumenPressman-IngdeSoftware.pdf` cap. 2.
- **Calidad y SQA**: costos de calidad, revisiones técnicas formales, fiabilidad → `ResumenPressman-IngdeSoftware.pdf` cap. 8.
- **Métricas**: directas e indirectas, puntos de función, GQM → `ResumenPressman-IngdeSoftware.pdf` cap. 4.
- **Gestión de configuración**: elementos de configuración, línea base → `Resumen_Final_Ing_de_Soft.pdf` pág. 22.
- **Las 4 P** y **fases vs flujos** → distinción clásica de examen.
---
 
## 7. Riesgos
 
1. **Que el alcance se vuelva a estirar.** Es el riesgo principal ahora que hay tiempo. El alcance ya se amplió dos veces (6 → 9 → 10) y **diez es el cierre definitivo**. El tiempo disponible va a que la Implementación y la Prueba salgan bien, y a la pasada de coherencia y la preparación de la defensa, no a agregar casos de uso. Cada CU nuevo arrastra análisis, diseño, código y pruebas, y obliga a tocar seis documentos.
2. **La decisión tecnológica ya está cerrada** (Python 3, Flask, Jinja2, SQLite, Linux, más `python-dotenv`). No se cambia a mitad de camino: tiene que aparecer igual en la arquitectura, el despliegue, los subsistemas, el plan de pruebas y el código.
3. **El recorte de alcance es una decisión propia y no está conversado con la cátedra.** Hay que decirlo así, porque es lo que ocurrió. El fundamento es: el proyecto está planteado para grupos de ocho personas y se cursó en solitario; según lo que comentaron compañeros de la materia, el mínimo esperado eran **cuatro** casos de uso realizados, y en esta entrega se realizaron **diez**, porque con cuatro la aplicación no tenía sentido de uso. **Pendiente:** conversarlo con la cátedra antes del 24/11/2026 y, si se obtiene una respuesta, registrarla. Si no se obtiene, el alcance se defiende como decisión propia con el fundamento de arriba. **Lo que no se hace es afirmar un acuerdo que no existió:** una afirmación falsa por escrito es peor que no decir nada, porque es verificable.
4. **Tres documentos propios no tienen encabezado de versión ni bloque de control:** `DIA1_REQUISITOS_MiBlog.md`, `REQUISITOS_CANDIDATOS_MiBlog.md` y `REQUISITOS_FUNCIONALES_MiBlog.md`. La §7 del índice dice que la regla aplica a todos. Los dos últimos, además, siguen con el estado `[PROPUESTA] — pendiente de confirmación`, aunque todo el proyecto se construyó sobre ellos. Corregir antes de la entrega.
5. **Que la documentación y el código se separen.** Durante la Implementación, cualquier nombre de clase o método que cambie se cambia **en el diagrama el mismo día**, y cualquier patrón que no llegue al código se saca del diagrama el mismo día. Mientras tanto, la tabla de desvíos del documento de contexto es la fuente.
6. **Programar en seis chats tiene su propio riesgo: que cada bloque arranque sin saber lo que hizo el anterior.** Se maneja con `CONTEXTO_IMPLEMENTACION_MiBlog.md`, que cada bloque lee al abrir y actualiza al cerrar, y con el informe de cierre. **Si se salta la actualización, el bloque siguiente arranca ciego.** La Etapa 4 se cerró con el documento al día (1.8); en la Etapa 5 vale lo mismo si se corrige el código.
7. **Que el diseño visual agregue funcionalidad.** Un diseño generado tiende a traer pantallas y controles que quedan bien pero que ningún caso de uso especifica. Si se programan, el código ofrece algo que la documentación no contempla; si se dejan dibujados y sin funcionar, la interfaz miente. La regla es: se descarta el agregado, o se actualizan el prototipo y las especificaciones. Entra en la pasada de coherencia del cierre.
8. **El modo típico de fracasar** no es escribir lento: es cambiar el conjunto de casos de uso o el stack a mitad de camino y tener que rehacer análisis y diseño.
---
 
## 8. Cómo se usa cada chat
 
**Al abrir:** pegar el prompt de la etapa. En la Etapa 4, el bloque común más el del bloque que toca.
 
**Al cerrar:** en la Etapa 4, el informe de cierre de §ETAPA 4, que incluye las líneas para `CONTEXTO_IMPLEMENTACION_MiBlog.md`. En las demás:
 
> Dame las líneas actualizadas de `ESTADO_MI_PROYECTO.md` con lo que quedó decidido y el estado de los entregables.
 
Y pegarlas al archivo, **subir la versión** y volver a subirlo al proyecto **antes** de abrir el chat siguiente. Si te salteás ese paso, la etapa siguiente arranca sin contexto.
 
---
 
## Control del documento
 
| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.12 | 27/10/2026 | Gestión del proyecto | **Bloque 4.4 cerrado; 7 de 10 casos de uso funcionando.** Estado de los bloques en §3 y en la tabla de la Etapa 4; lo que se adelantó del 4.6 al 4.4 (pruebas, `sembrar_datos.py`, README). Regla nueva: cada bloque deja sus pruebas y la suite pasa antes de cerrar. Prompt del 4.4 marcado como hecho; el del 4.5 hereda el estado y pide pruebas y README; el del 4.6 se reescribe. Informe de cierre con la cantidad de pruebas. Etapa 5: rnf 9.3, `sembrar_datos.py` y pruebas automáticas. Dos preguntas nuevas de defensa (clave `demo-1234`, SQL de `sembrar_datos.py`). CONTEXTO a 1.6. |
| 1.13 | 27/10/2026 | Gestión del proyecto | **Bloque 4.5 cerrado; los 10 casos de uso funcionando.** Estado de los bloques en §1, §3 y en la tabla de la Etapa 4; el 4.6 pasa a ser el siguiente y suma DV-7 y P-17. Prompt del 4.5 marcado como hecho; el del 4.6 suma DV-7 y P-17. Pruebas: 183 (Etapa 5). CONTEXTO a 1.7. |
| 1.14 | 28/10/2026 | Gestión del proyecto | **Bloque 4.6 cerrado; Etapa 4 (Implementación) cerrada.** Estado de los bloques en §1, §3 y en la tabla de la Etapa 4 (la Etapa 5 pasa a ser la siguiente); DISEÑO a 1.4, ESPECIFICACIONES a 1.3 y CONTEXTO a 1.8. Prompt del 4.6 marcado como hecho; la regla de commits abarca 4.2 a 4.6. Etapa 5: 262 pruebas, el código cerrado, los límites conocidos y lo que agregó el 4.6. Tres preguntas nuevas de defensa (errores inesperados, límites conocidos y forma del nombre de usuario). |
| 1.15 | 28/10/2026 | Gestión del proyecto | **Corrección de una afirmación falsa que venía desde la versión 1.0.** El encabezado decía que la cátedra aceptaba una entrega de alcance reducido, y el riesgo 3 daba por hecho un acuerdo verbal que había que poner por escrito. **No hubo ninguna conversación con la cátedra sobre el alcance.** El encabezado ahora dice que el recorte es una decisión propia del alumno, y el riesgo 3 queda reescrito con el fundamento real (proyecto para grupos de ocho cursado en solitario; cuatro casos de uso como mínimo comentado por compañeros; diez realizados) y con el pendiente de conversarlo antes del 24/11. El riesgo 4 pasa de uno a tres documentos sin encabezado de versión (`DIA1_REQUISITOS`, `REQUISITOS_CANDIDATOS` y `REQUISITOS_FUNCIONALES`) y suma el estado `[PROPUESTA]` de los dos últimos; los tres quedaron corregidos ese mismo día (1.1, 1.1 y 1.2). La §2.3 y el prompt de la Etapa 5 suman la restricción de **no** reintroducir la afirmación en el plan de pruebas, que es un documento nuevo y es la vía por la que podría volver a entrar. |
