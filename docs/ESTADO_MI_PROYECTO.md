# ESTADO DE MI PROYECTO — Sistema MiBlog
 
**Materia:** Ingeniería de Software · **Alumno:** Abel
**Versión:** 1.13 · **Última modificación:** 28/10/2026 · **Etapa:** Gestión del proyecto
**Última actualización:** 28/10/2026 — **Etapa 4 (Implementación) CERRADA: los seis bloques (4.1 a 4.6) están cerrados y los 10 casos de uso funcionan.** Sigue la Etapa 5 (Prueba). Los flujos de Requisitos, Análisis y Diseño siguen cerrados (`ESPECIFICACIONES_CASOS_DE_USO_MiBlog.md` 1.3, `DISEÑO_MiBlog.md` 1.4). Lo que se construyó y se decidió al programar vive en `CONTEXTO_IMPLEMENTACION_MiBlog.md`.
**Cómo usar este archivo:** es el documento vivo del proyecto. Todo chat que vaya a producir un artefacto lo lee primero y, al cerrar, devuelve las líneas actualizadas para pegarlas acá. **En la Etapa 4 el traspaso entre bloques va en `CONTEXTO_IMPLEMENTACION_MiBlog.md`**, y acá solo se actualiza el estado de los entregables (§7) y la bitácora (§9).
 
---
 
## 0. Convención de estados y de origen
 
| Marca | Significado |
|---|---|
| `[ENUNCIADO]` | Está literalmente en `enunciado_microblogging.pdf`. No se discute. |
| `[DECIDIDO]` | Lo decidí yo. Vale como dato firme. |
| `[PROPUESTA]` | Sugerencia de un chat que **yo todavía no confirmé**. |
| `[PENDIENTE]` | Falta decidir. |
| `[CÁTEDRA]` | Indicación o corrección del profesor. Prioridad máxima. |
 
> Regla para los chats: **no convertir un `[PROPUESTA]` en `[DECIDIDO]` por su cuenta.**
 
### 0.1 Códigos usados en todos los documentos
 
Orden de construcción: enunciado → requisitos candidatos → requisitos funcionales y no funcionales → casos de uso.
 
| Código | Significa | Documento |
|---|---|---|
| R00–R17 | Requisito del enunciado | `enunciado_microblogging.pdf` |
| C01–C38 | Característica evaluada (requisito candidato) | `REQUISITOS_CANDIDATOS_MiBlog.md` |
| RF01–RF21 | Requisito funcional | `REQUISITOS_FUNCIONALES_MiBlog.md` |
| RA01–RA11 | Regla funcional automática | `REQUISITOS_FUNCIONALES_MiBlog.md` |
| RNF01–RNF42 | Requisito no funcional | `REQUISITOS_NO_FUNCIONALES_MiBlog.md` |
| CU0001–CU0021 | Caso de uso | `ESPECIFICACIONES_CASOS_DE_USO_MiBlog.md` |
| D-xx, DV-x, P-x | Decisión, desvío del diseño y pendiente de la Implementación | `CONTEXTO_IMPLEMENTACION_MiBlog.md` |
 
---
 
## 1. Datos del proyecto
 
- `[ENUNCIADO]` Dominio: red social **interna de una empresa** para mejorar la comunicación entre empleados.
- `[ENUNCIADO]` Tipo de sistema: **microblogging**.
- `[DECIDIDO]` Nombre del sistema: **MiBlog**.
- `[DECIDIDO]` Proyecto pensado para grupo, **cursado y entregado en solitario**. Sin reparto de CU, sin herramienta de backlog.
- `[DECIDIDO]` Qué se rinde: **Final** = entrega del proyecto + defensa oral práctica y teórica. La materia ya está regularizada.
- `[DECIDIDO]` Plazo: **entrega y defensa el 24/11/2026**. El plazo original de 4 días venció y se reemplazó por esta fecha.
- `[DECIDIDO]` **No se producen artefactos de SCRUM.** Eran exigencia de la cursada, no del final.
- `[DECIDIDO]` Alcance de la entrega, **decidido por el alumno y no conversado con la cátedra**: flujo de Requisitos completo; **10 de los 21 casos de uso** realizados en Análisis, Diseño, Implementación y Prueba.
- `[DECIDIDO]` Fundamento del recorte: el proyecto está planteado para grupos de ocho personas y se cursó en solitario. Según lo que comentaron compañeros de la materia, el mínimo esperado eran **cuatro** casos de uso realizados; en esta entrega se realizaron **diez**, porque con cuatro la aplicación no tenía sentido de uso.
- `[PENDIENTE]` Conversar el alcance con la cátedra antes del 24/11/2026 y registrar la respuesta si la hay. Si no la hay, el alcance se defiende como decisión propia con el fundamento de la línea anterior. **No se afirma en ningún documento un acuerdo que no existió.**
---
 
## 2. Requisitos del enunciado
 
Todos `[ENUNCIADO]`. Tomados de `enunciado_microblogging.pdf` (1 página).
 
- **R00** — Objetivo: mejorar la comunicación entre los empleados de la empresa.
- **R01** — Publicar mensajes de **hasta 140 caracteres**.
- **R02** — Los mensajes pueden ser leídos por los **seguidores** del autor.
- **R03** — Al registrarse: **nombre de usuario (≤15)**, correo, **foto**, clave, **nombre completo**, **breve descripción**.
- **R04** — **Tablón** con los mensajes de los seguidos y los propios.
- **R05** — Cada mensaje indica **autor**, **fecha** y **texto**.
- **R06** — El texto admite **links**, **menciones** (`@`) y **etiquetas** (`#`).
- **R07** — Las etiquetas **clasifican el contenido** para búsquedas y estadísticas.
- **R08** — Desde la página principal, consultar **seguidores** y **seguidos**.
- **R09** — **Temas del momento**: etiquetas más repetidas en los últimos `n` días.
- **R10** — `n` **configurable por el administrador**.
- **R11** — **Republicar** un mensaje del tablón creado por alguien a quien se sigue.
- **R12** — **Mensaje privado** a un usuario en particular.
- **R13** — Los mensajes propios pueden ser **borrados y editados**.
- **R14** — **Una vez a la semana**, email a los usuarios con los temas del momento.
- **R15** — Ese email contiene los **links** al listado de mensajes de cada etiqueta.
- **R16** — **Servicios web REST** para **publicar** y **leer el muro** de un usuario.
- **R17** — Acceso restringido a **aplicaciones registradas**.
### 2.1 Supuestos propios (lo que el enunciado no dice)
 
Todos `[DECIDIDO]`. Registrados como características en `REQUISITOS_CANDIDATOS_MiBlog.md`.
 
| Cód. | Decisión |
|---|---|
| C17 | Existen **login y cierre de sesión** (CU0002, CU0003). |
| C18 | **Seguir es unilateral**: no requiere aprobación del seguido. |
| C19 | Los mensajes no privados son **públicos dentro de la empresa**. El seguimiento determina qué llega al tablón, no qué se puede leer. |
| C20 | Existe el **muro de usuario** en la aplicación web (CU0010). |
| C21, C22 | Existen **búsqueda de usuarios** y **búsqueda de mensajes por etiqueta**. |
| C23 | La **republicación referencia** al mensaje original: al editarlo, todas reflejan el texto nuevo y el mensaje queda marcado como editado. |
| C24 | El **Administrador** configura `n` y gestiona las aplicaciones externas. **No** modera contenido ni da de baja usuarios. |
| C25 | Las **aplicaciones externas** se autentican con una credencial emitida al registrarse. |
| C27 | **No hay notificaciones in-app.** Único canal: el email semanal. |
| — | "Usuario registrado" y "usuario autenticado" se **unifican** en un solo actor. |
 
---
 
## 3. Actores
 
`[DECIDIDO]` — ver `DIA1_REQUISITOS_MiBlog.md` §2.
 
| Actor | Tipo | Requisitos |
|---|---|---|
| **Visitante** | Primario, humano | R03 |
| **Usuario** | Primario, humano | R01, R02, R04–R09, R11–R13 |
| **Administrador del Sitio** | Primario, humano. Especialización de Usuario | R10, R17 |
| **Tiempo** | Primario, no humano | R14 |
| **Aplicación Externa** | Primario, no humano | R16, R17 |
| **Servidor de Correo** | **Secundario**, no humano | R14, R15 |
 
> No existe un actor "Sistema": un sistema nunca es actor de sí mismo. Lo que dispara el envío semanal es el paso del tiempo.
 
---
 
## 4. Casos de uso
 
`[DECIDIDO]` — 21 casos de uso, todos especificados en `ESPECIFICACIONES_CASOS_DE_USO_MiBlog.md`.
 
| Cód. | Nombre | Actor | Paquete | Prioridad |
|---|---|---|---|---|
| CU0001 | Registrar Usuario | Visitante | Gestión de Usuarios | 10 |
| CU0002 | Iniciar Sesión | Visitante | Gestión de Usuarios | 10 |
| CU0003 | Cerrar Sesión | Usuario | Gestión de Usuarios | 3 |
| CU0004 | Publicar Mensaje | Usuario | Gestión de Mensajes | 10 |
| CU0005 | Editar Mensaje Propio | Usuario | Gestión de Mensajes | 7 |
| CU0006 | Borrar Mensaje Propio | Usuario | Gestión de Mensajes | 7 |
| CU0007 | Republicar Mensaje | Usuario | Gestión de Mensajes | 7 |
| CU0008 | Enviar Mensaje Privado | Usuario | Gestión de Mensajes | 6 |
| CU0009 | Visualizar Tablón | Usuario | Gestión de Mensajes | 10 |
| CU0010 | Consultar Muro de un Usuario | Usuario | Gestión de Mensajes | 6 |
| CU0011 | Seguir Usuario | Usuario | Gestión de Relaciones | 9 |
| CU0012 | Dejar de Seguir Usuario | Usuario | Gestión de Relaciones | 3 |
| CU0013 | Consultar Seguidores y Seguidos | Usuario | Gestión de Relaciones | 6 |
| CU0014 | Buscar Usuarios | Usuario | Gestión de Relaciones | 3 |
| CU0015 | Ver Temas del Momento | Usuario | Tendencias | 10 |
| CU0016 | Buscar Mensajes por Etiqueta | Usuario | Tendencias | 6 |
| CU0017 | Configurar Ventana de Días `n` | Administrador | Administración | 6 |
| CU0018 | Registrar Aplicación Externa | Administrador | Administración | 7 |
| CU0019 | Enviar Email Semanal de Temas del Momento | Tiempo | Notificaciones | 10 |
| CU0020 | Publicar Mensaje vía API REST | Aplicación Externa | Integración | 7 |
| CU0021 | Leer Muro de un Usuario vía API REST | Aplicación Externa | Integración | 7 |
 
### 4.1 Alcance de realización — los 10 que se construyen
 
`[DECIDIDO]` — **cerrado. No se vuelve a mover.**
 
**CU0001, CU0002, CU0003, CU0004, CU0005, CU0006, CU0007, CU0009, CU0011 y CU0014.**
 
Cubren **R01, R03, R04, R05, R06, R11, R13** y parcialmente **R02**, más la característica **C21**.
 
Los **11 restantes** —CU0008, CU0010, CU0012, CU0013, CU0015, CU0016, CU0017, CU0018, CU0019, CU0020 y CU0021— quedan especificados y **no se implementan**.
 
CU0014 entra porque es el punto de entrada de CU0011: sin búsqueda no hay forma de alcanzar a un usuario que todavía no se sigue.
 
**La regla: Requisitos, los 21. Análisis, Diseño, Implementación y Prueba, solo los 10.**
 
**Frase obligatoria** en el documento de arquitectura y en el plan de pruebas:
 
> Esta iteración realiza los casos de uso CU0001, CU0002, CU0003, CU0004, CU0005, CU0006, CU0007, CU0009, CU0011 y CU0014. Los restantes quedan especificados en el flujo de Requisitos y no forman parte del alcance de implementación de esta versión.
 
### 4.2 Consecuencias técnicas del alcance ampliado
 
Al incorporar CU0005, CU0006 y CU0007, dos cosas cambian y hay que reflejarlas en Análisis y Diseño:
 
1. **La consulta del tablón (CU0009) incluye republicaciones.** Reúne los mensajes públicos de los seguidos, los propios y **las republicaciones de unos y otro**, ordenando cada elemento por la fecha que corresponda: la de publicación para un mensaje, la de republicación para una republicación. Regla RA07.
2. **El borrado (CU0006) es en cascada.** Al eliminar un mensaje se eliminan todas sus republicaciones, en una única transacción. Reglas RA06 y `rnf 6.3`.
---
 
## 5. Decisiones técnicas
 
`[DECIDIDO]` 13/09/2026. Criterio: con una sola persona, no se incorpora ninguna herramienta que no se sepa usar.
 
| Tema | Decisión |
|---|---|
| Lenguaje / backend | **Python 3 + Flask** |
| Frontend | **Plantillas Jinja2 renderizadas en el servidor.** Sin framework de frontend. Hoja de estilos propia. |
| Tipografía | **Space Grotesk y Martian Mono, como archivos del proyecto** (`presentacion/estaticos/fuentes/`), licencia SIL OFL 1.1, sin CDN. `[DECIDIDO]` 24/10/2026, D-09 del documento de contexto. |
| Base de datos | **SQLite**, mediante el módulo `sqlite3` de la biblioteca estándar. Archivo local, fuera del repositorio. |
| Acceso a datos | Módulo propio con **SQL parametrizado**. Sin ORM. |
| Autenticación | Mecanismos de sesión y cifrado de clave provistos por Flask (`werkzeug.security`). Para cerrar la sesión del lado del servidor, tabla técnica `sesiones` con el hash SHA-256 de un token aleatorio. Las filas vencidas se borran al validarlas y al iniciar sesión. `[DECIDIDO]` 15/09/2026, H1. |
| Errores y registro | Páginas de error con texto genérico (nunca el detalle técnico) y un archivo de registro, `instance/miblog.log`, donde quedan solo los errores inesperados, con fecha y hora y sin formularios (RNF16 y RNF24). `[DECIDIDO]` 28/10/2026, D-37 y D-42 del documento de contexto. |
| Dependencias | **Flask** y **python-dotenv**, ninguna otra. Declaradas en `REQUISITOS_NO_FUNCIONALES_MiBlog.md` §8.0, con el motivo de cada una. `[DECIDIDO]` 15/09/2026, H10. |
| Sistema operativo | **Linux** |
| Ejecución | Servidor de desarrollo de Flask, ambiente local. Sin servidor de producción declarado. |
| Envío de correo | SMTP externo. **Diseñado, no implementado** (CU0019 fuera de alcance). |
| Planificador | `cron`. **Diseñado, no implementado** (CU0019 fuera de alcance). |
| Repositorio | Git con historial. Secretos en `.env`, `.env` en `.gitignore`. **Un solo repositorio con las cinco etapas** (`microblogging/`), y el código en `4. Implementacion/codigo/`. Commits `Etapa: descripción`. `[DECIDIDO]` 24/10/2026, D-01. |
| Diagramado | Mermaid y PlantUML. |
 
**Regla de coherencia:** la misma tecnología en el texto de arquitectura, el diagrama de despliegue, el diagrama de subsistemas, el plan de pruebas y el código.
 
**Consecuencia:** el diagrama de despliegue tiene **un solo nodo**. Flask y el archivo SQLite conviven en la misma máquina.
 
### 5.1 Patrones de diseño
 
`[DECIDIDO]` 14/09/2026, en el flujo de Análisis. Fundamento completo en `ANALISIS_MiBlog.md` §8.
 
**Los cuatro patrones que estaban propuestos quedaron sin anclaje**, porque los cuatro se apoyaban en casos de uso que no se realizan:
 
| Patrón | Anclaje previsto | Motivo del descarte |
|---|---|---|
| Singleton | Acceso a la configuración del sitio (`n`) | `Configuracion` no está en el modelo de análisis: CU0015, CU0017 y CU0019 fuera de alcance |
| Observer | Notificación a seguidores | La característica C27 decidió que no hay notificaciones in-app |
| Factory Method | Tipos de mensaje (público / privado) | `MensajePrivado` nunca se instancia: CU0008 fuera de alcance |
| Strategy | Visibilidad del mensaje | Con un solo tipo de mensaje no hay dos estrategias entre las cuales elegir |
 
**Los cuatro que sí tienen anclaje real en los diez casos de uso realizados:**
 
| Patrón | Anclaje | CU que lo ejercitan |
|---|---|---|
| **Strategy** | Familia de extractores de `AnalizadorDeTexto` (etiquetas, menciones, enlaces), exigida por el `rnf 4.3` | CU0004, CU0005 |
| **Factory Method** | Cada extractor crea un tipo distinto de elemento extraído | CU0004, CU0005 |
| **Decorator** | `Republicacion` envuelve y delega en `MensajePublico`; es lo que sostiene la característica C23 | CU0007, CU0009 |
| **Template Method** | Esqueleto compartido de publicar y editar en `ControlPublicacion` | CU0004, CU0005 |
 
**Composite queda descartado** como alternativa para el tablón: resuelve jerarquías parte-todo en árbol, y el tablón es una lista plana donde la republicación referencia al mensaje en lugar de contenerlo.
 
**Clases de diseño nuevas que esto introduce**, ninguna de las cuales es entidad ni figura en el modelo de dominio: `Extractor` (abstracta) más sus tres concretas, `ElementoExtraido` (abstracta) y `ElementoDeTablon` (abstracta).
 
> **Regla para la Etapa 4.** Si algún patrón no llega al código, se saca de la documentación en la misma jornada. La coherencia entre diagrama y código vale más que la cantidad de patrones.
 
**Dónde quedaron en el Diseño** (`DISEÑO_MiBlog.md` §3.4). Los cuatro están dentro del **único** diagrama de clases de diseño, marcados con el papel que cumple cada clase en su patrón. Dos precisiones respecto del análisis: `ElementoDeTablon` quedó como **interfaz**, y `Republicacion` guarda una referencia de tipo `MensajePublico` (no a la interfaz), lo que impide republicar una republicación. La firma del analizador pasa a `analizar(texto)` (`[DECIDIDO]` H2).
 
**Criterio de verificación.** Cada patrón tiene escrita en `ANALISIS_MiBlog.md` §8.3 a §8.5 la estructura mínima de clases que el código debe tener para que sea real, y sus señales de degradación. La tabla que se aplica en la pasada de coherencia final está en **`ANALISIS_MiBlog.md` §8.8**, con tres comprobaciones que se corren sobre el repositorio:
 
| Comando | Resultado esperado |
|---|---|
| `grep -rn "140" <capa de lógica>` | una sola aparición |
| `grep -rn "isinstance\|es_republicacion" <lógica y plantillas>` | cero apariciones |
| `grep -rn "Extractor[A-Z]" analizador.py` | cero apariciones |
 
El Diseño agrega **tres comprobaciones más**, sobre las reglas de arquitectura (`DISEÑO_MiBlog.md` §2.7): que la presentación no llegue al acceso a datos, que no haya SQL fuera de `acceso_datos` y que el dominio no importe `acceso_datos`. **En total son seis.** El estado de cada una al cierre de cada bloque está en `CONTEXTO_IMPLEMENTACION_MiBlog.md` §7.
 
**Estado en el código (28/10/2026).** Desde el bloque 4.4 los cuatro patrones están en el código, y el 4.5 los completó, con la estructura que pide `ANALISIS_MiBlog.md` §8: Strategy y Factory Method completos (`Extractor` y sus tres concretos, `AnalizadorDeTexto`); Template Method con `OperacionSobreMensaje` y sus dos subclases, `Publicacion` y `Edicion` (`borrar` no lo usa, a propósito: DISEÑO §6.6); Decorator completo (el tablón trata igual al mensaje y a la republicación, `Republicacion` se crea sin copiar texto y editar el original se ve en sus republicaciones). Las seis comprobaciones dan el resultado esperado y además corren como pruebas automáticas (`pruebas/test_reglas_de_arquitectura.py`). El 4.6 no tocó ninguno de los cuatro y las seis se volvieron a correr sobre la copia final.
 
### 5.2 Hallazgos del Diseño
 
15/09/2026. Desarrollo completo en `DISEÑO_MiBlog.md` §1. **Los diez casos de uso se realizan.** Los doce hallazgos quedaron resueltos el mismo día.
 
| # | Hallazgo | Estado | Resultado |
|---|---|---|---|
| H1 | La sesión de Flask no se puede invalidar en el servidor (`rnf 3.1`) | `[DECIDIDO]` | Tabla `sesiones` con token aleatorio y hash SHA-256. Limpieza de vencidas al validar y al iniciar sesión |
| H2 | Las firmas de ANALISIS §8.3 y §8.5 no encajaban | `[DECIDIDO]` | `analizar(texto)`; la etiqueta repetida la resuelve la base con `INSERT OR IGNORE` |
| H3 | `ca 7.3` ofrecía deshacer la republicación | Aplicado | ESPECIFICACIONES 1.2 |
| H4 | `ca 11.3` ofrecía "Dejar de seguir" (CU0012) | Aplicado | Marcado fuera de alcance. ESPECIFICACIONES 1.2 y ANALISIS 2.2 |
| H5 | `ca 7.1` sí es alcanzable desde la interfaz | `[DECIDIDO]` | Botón en todo elemento cuyo autor original no es el usuario; decide el servidor. ESPECIFICACIONES 1.2 y ANALISIS 2.2 |
| H6 | CU0007 sin curso para mensaje inexistente | Aplicado | `ca 7.4`. ESPECIFICACIONES 1.2 |
| H7 | `Usuario.activo` nunca pasa a `False` | `[DECIDIDO]` | **Opción A**: se conserva. `Inactivo` es inalcanzable en esta versión. `DIA1_REQUISITOS_MiBlog.md` no cambia |
| H8 | Cuatro frases de la versión 1.0 en el análisis | Aplicado | ANALISIS 2.2 |
| H9 | Sin JavaScript no hay diálogos flotantes (RNF31) | `[DECIDIDO]` | Cada diálogo es una página propia |
| H10 | Leer el `.env` | `[DECIDIDO]` | `python-dotenv`, declarada también en `REQUISITOS_NO_FUNCIONALES_MiBlog.md` §8.0 |
| H11 | La presentación usa objetos del dominio | Aplicado | Dependencia `presentacion → dominio` declarada |
| H12 | Tres detalles en los documentos de requisitos | Aplicado | ESPECIFICACIONES 1.2 y REQUISITOS_NO_FUNCIONALES 1.1 |
 
**Respuestas para la defensa que quedaron escritas** (`DISEÑO_MiBlog.md` §1 y §8.4):
 
- **Limpieza de sesiones.** Una sesión vencida nunca se acepta, se haya borrado o no. La fila se borra cuando alguien intenta usarla vencida, y cada inicio de sesión borra las vencidas de todos.
- **`activo`.** No es una función de moderación (la descartó C24): es una marca de habilitación reservada, y las consultas filtran por ella de forma defensiva. Se prueba con un usuario inactivo cargado en los datos de prueba.
---
 
## 6. Modelo de dominio
 
`[DECIDIDO]` — 15 clases con atributos y multiplicidades en todas las asociaciones. Diagrama Mermaid completo en `DIA1_REQUISITOS_MiBlog.md` §4.
 
Núcleo: Usuario · Seguimiento · Mensaje (abstracta) · MensajePublico · MensajePrivado · Republicacion · Etiqueta · Mencion · Enlace · Aplicacion · Configuracion · EnvioSemanal
Derivadas: Muro · Tablon · Tendencia
 
`[DECIDIDO]` 15/09/2026 (hallazgo H7, opción A): `Usuario.activo` se conserva como marca de habilitación reservada. El modelo de dominio no cambia.
 
---
 
## 7. Estado de los entregables
 
### Requerimientos — **CERRADO**
 
`[DECIDIDO]` El flujo de Requisitos está terminado. Nada de esta sección vuelve a abrirse salvo corrección de la cátedra **o hallazgo de un flujo posterior**. El 15/09/2026 se aplicaron las correcciones del Diseño: `ESPECIFICACIONES_CASOS_DE_USO_MiBlog.md` pasó a 1.2 y `REQUISITOS_NO_FUNCIONALES_MiBlog.md` a 1.1. El 28/10/2026, por el cierre del 4.6, `ESPECIFICACIONES_CASOS_DE_USO_MiBlog.md` pasó a 1.3: documenta la forma del nombre de usuario (`{Ob 1.3}`) y apunta a las pantallas del prototipo; ningún caso de uso cambió de alcance.
| Artefacto | Estado |
|---|---|
| Listado de requerimientos candidatos | ✅ `REQUISITOS_CANDIDATOS_MiBlog.md` (C01–C38) |
| Modelo del Dominio | ✅ `DIA1_REQUISITOS_MiBlog.md` §4 |
| Listado de Actores y Casos de Uso | ✅ `DIA1_REQUISITOS_MiBlog.md` §2 y §3 |
| Priorización de Casos de Uso | ✅ `DIA1_REQUISITOS_MiBlog.md` §3.2 |
| **Diagrama de Casos de Uso — UNO SOLO** | ✅ `DIA1_REQUISITOS_MiBlog.md` §5 `[CÁTEDRA]` |
| Detalle de cada Caso de Uso | ✅ `ESPECIFICACIONES_CASOS_DE_USO_MiBlog.md` (21 CU) |
| Listado de requerimientos no funcionales | ✅ `REQUISITOS_NO_FUNCIONALES_MiBlog.md` (RNF01–RNF42) `[CÁTEDRA]` |
| Prototipos de interfaz | ✅ `Prototipo de Interfaces` (7 vistas en la entrega original), actualizado el 28/10/2026 al diseño visual implementado |
 
### Análisis — **CERRADO**
 
`[DECIDIDO]` 14/09/2026. Todo en `ANALISIS_MiBlog.md`, hoy en versión **2.2** por las correcciones del Diseño (H4, H5, H8).
 
| Artefacto | Estado |
|---|---|
| Clases de Análisis (interfaz / control / entidad) | ✅ 23 clases: 7 interfaz, 8 control, 8 entidad — `ANALISIS_MiBlog.md` §2 |
| Diagrama de Clases de Análisis | ✅ Mermaid — §3 |
| Diagrama de Paquetes | ✅ PlantUML, 5 paquetes acíclicos — §4 |
| Diagramas de Colaboración **con mensajes numerados** | ✅ los 10 CU — §5 |
| Patrones de diseño con anclaje real | ✅ §8 (artefacto de Diseño, decidido en Análisis) |
 
### Diseño — **CERRADO**
 
`[DECIDIDO]` 15/09/2026. Todo en `DISEÑO_MiBlog.md`, hoy en versión **1.4**. Los 17 diagramas están en PlantUML y compilados; la imagen del diagrama de clases hay que regenerarla (P-18).
 
| Artefacto | Estado |
|---|---|
| Arquitectura en capas y tabla de mecanismos | ✅ 4 capas, 15 rutas, esquema SQL, mecanismos de persistencia, transacciones, seguridad y errores — §2 |
| Patrones de diseño | ✅ los cuatro de §5.1, ubicados en el diagrama integral — §3.4 |
| **Diagrama de Clases de Diseño integral con patrones** | ✅ **uno solo**, 47 elementos, con atributos, métodos y visibilidad — §3 `[CÁTEDRA]` |
| Diagrama de Despliegue (un solo nodo) | ✅ §4 |
| Diagrama de Subsistemas | ✅ **dos vistas** — §5. Se entrega el de paquetes anidados por capa (§5.2.1), en el formato que usan los demás proyectos de la cátedra; el de las cuatro capas del PU queda como vista complementaria (§5.2.2). Los dos con traza a los cinco paquetes de análisis |
| Diagramas de Secuencia | ✅ los 10 CU, con fragmentos `alt` para cada curso alternativo especificado — §6 |
| Diagramas de Estados | ✅ `Mensaje` y `Usuario` — §7 |
 
**Corrección aplicada el 24/10/2026 (diseño 1.3)**, sin cambios en ningún diagrama: tres puntos de la §2.4 que el código cambió al programar (raíz del código dentro de `4. Implementacion/codigo/`, carpeta `fuentes/` y `.gitignore`), registrados como DV-1, DV-2 y DV-3 en `CONTEXTO_IMPLEMENTACION_MiBlog.md` §6.1.
 
**Corrección aplicada el 28/10/2026 (diseño 1.4)**, al cerrar el 4.6: los desvíos DV-4 a DV-8 del documento de contexto pasaron al diseño (árbol de §2.4, columna *Endpoint* de las 15 rutas en §2.5, fechas y manejo de errores y registro en §2.6, miembros de apoyo y nota N4 en el diagrama de clases de §3.2, forma del nombre de usuario en §6.1, cuatro reglas en §6.4 y el aviso de `ca 11.2` en §6.9). Ningún nombre de clase, método ni ruta cambió; el diagrama de §3.2 se recompiló con PlantUML sin errores y sigue teniendo 47 elementos. **No queda ningún desvío sin pasar al diseño.**
 
### Implementación — **CERRADA** (del 23/10/2026 al 28/10/2026)
 
Se hizo en chats de este proyecto, en seis bloques. El detalle de cada uno, con su estado, está en `PLAN_DEL_PROYECTO.md` (Etapa 4) y lo construido en `CONTEXTO_IMPLEMENTACION_MiBlog.md`.
 
| Artefacto | Estado |
|---|---|
| **4.1 Cimientos** (carpetas, conexión, esquema, dominio, errores, `crear_app()`, estilos y plantilla base) | ✅ cerrado el 24/10/2026. La base se crea con `iniciar-bd` y el servidor muestra la página provisoria |
| **4.2 Sesión** (CU0001, CU0002, CU0003) | ✅ cerrado el 24/10/2026. Se puede registrar una cuenta, iniciar sesión y cerrarla |
| **4.3 Relaciones** (CU0014, CU0011) | ✅ cerrado el 26/10/2026. Se puede buscar a un usuario y seguirlo. Primeras rutas protegidas por `GuardiaSesion` |
| **4.4 Mensajes y tablón** (CU0004, CU0009) | ✅ cerrado el 27/10/2026. Se puede publicar un mensaje con `#etiquetas`, `@menciones` y enlaces, y verlo en el tablón junto con los de las personas que sigo. Los cuatro patrones están en el código. 83 pruebas automáticas, datos de demostración (`sembrar_datos.py`) y `README.md` completo |
| **4.5 Edición y republicación** (CU0005, CU0006, CU0007) | ✅ cerrado el 27/10/2026. Se puede editar, borrar (en cascada) y republicar. `Edicion` es la segunda clase del Template Method y el Decorator quedó completo. 183 pruebas automáticas. Commiteado en seis commits por capa |
| **4.6 Cierre del código** (errores y registro, forma del nombre de usuario, franja de marca, pruebas de la sesión y de las relaciones, README final, desvíos al diseño, `diagnostico.py` borrado) | ✅ cerrado el 28/10/2026. Páginas de error y archivo de registro (RNF24), el nombre de usuario con su forma admitida (D-38), la franja de marca en el inicio de sesión y en el registro (D-43), 79 pruebas nuevas, `README.md` final con los límites conocidos (D-39) y DV-4 a DV-8 en el diseño 1.4. Once commits. **Con este bloque se cierra la Etapa 4** |
| Los 10 casos de uso funcionando | ✅ **10 de 10** (CU0001 a CU0007, CU0009, CU0011 y CU0014), completos desde el 27/10/2026 con el bloque 4.5 y con el código cerrado desde el 28/10/2026 (4.6). Sigue la Etapa 5 |
| Pruebas automáticas (`codigo/pruebas/`) | ✅ **262 pruebas** con `unittest` (83 desde el 4.4, 100 del 4.5 y 79 del 4.6; D-27 y D-41): extractores y analizador, repositorios, registro, sesión, búsqueda y seguimiento, publicación, edición, borrado en cascada, republicación, tablón, rutas web, errores y registro, rendimiento (rnf 9.3) y las seis reglas de arquitectura. Se rompió el código a propósito 39 veces para comprobar que sirven y las detectaron todas. No reemplazan al Plan, los Casos y los Procedimientos de prueba de la Etapa 5 |
| Repositorio Git con historial | ✅ Un commit por cosa terminada (de 4.2 a 4.6, por capa), formato `Etapa: descripción`. Todos los hashes están anotados (P-16). Quedan por commitear los documentos actualizados al cerrar el 4.6 (P-19) |
 
### Prueba
| Artefacto | Estado |
|---|---|
| Plan de Pruebas | `[PENDIENTE]` |
| Casos de Prueba | `[PENDIENTE]` — los 10 CU, curso normal y alternativos |
| Procedimientos de Prueba | `[PENDIENTE]` |
 
### Cierre
| Artefacto | Estado |
|---|---|
| Matriz de trazabilidad | `[PENDIENTE]` |
| Pasada de coherencia | `[PENDIENTE]` |
 
**Correcciones del Diseño, aplicadas el 15/09/2026:**
 
| Documento | Versión | Por | Estado |
|---|---|---|---|
| `ESPECIFICACIONES_CASOS_DE_USO_MiBlog.md` | 1.2 | H3, H4, H5, H6, H12.1, H12.2 | ✅ |
| `ANALISIS_MiBlog.md` | 2.2 | H4, H5, H8 | ✅ |
| `REQUISITOS_NO_FUNCIONALES_MiBlog.md` | 1.1 | H10, H12.3 | ✅ |
| `DIA1_REQUISITOS_MiBlog.md` | 1.0, sin cambios | H7 opción A | ✅ |
 
**Pendiente menor para la pasada de coherencia final:** el campo **Documentación anexa** de las 21 especificaciones dice "Pendiente" en las filas de prototipo de interfaz y de documentación de la API. Las que refieren a pantallas deben apuntar al archivo del prototipo; las de la API quedan como no aplicables por estar fuera del alcance de realización. **Avance (28/10/2026, ESPECIFICACIONES 1.3):** las cuatro filas de prototipo de interfaz (CU0001, CU0002, CU0004 y CU0009) ya apuntan a las pantallas del `Prototipo de Interfaces`. Quedan las de API y plantilla de correo de los casos de uso fuera del alcance de realización, y `DIA1_REQUISITOS_MiBlog.md` sin encabezado de versión (P-6).
 
> **Gestión (SCRUM): no aplica.** Era exigencia de la cursada, no del final.
 
---
 
## 8. Correcciones y devoluciones de la cátedra
 
- (sin devoluciones registradas todavía)
---
 
## 9. Bitácora de chats
 
- **12/09/2026** — Análisis de los archivos de la raíz y de los repositorios de referencia. Se generó `INFORME_CONTEXTO_PROYECTO.md`, `00_INDICE.md` y este documento.
- **13/09/2026** — **FLUJO DE REQUISITOS CERRADO.** Cerradas las decisiones bloqueantes y los supuestos C17–C27. Producidos y terminados: los tres listados de requisitos (candidatos, funcionales y no funcionales), 6 actores, catálogo de 21 CU priorizado, modelo de dominio de 15 clases, diagrama único de casos de uso, las 21 especificaciones y el prototipo de interfaces de 7 vistas. Decidido el stack completo. Alcance cerrado en **10 casos de uso realizados**.
  **Próxima etapa: Análisis, sobre los 10.**
- **14/09/2026** — **FLUJO DE ANÁLISIS CERRADO.** Producidos los cuatro entregables sobre los 10 casos de uso realizados. Tomadas cinco decisiones de modelado (`ANALISIS_MiBlog.md` §1): la sesión no es entidad sino mecanismo de diseño; CU0009 paso 6, CU0014 paso 4 y CU0007 `ca 7.1` marcados fuera de alcance en las especificaciones; se conserva la jerarquía de `Mensaje`; `Tablon`, `Muro` y `Tendencia` no son entidades de análisis. Reemplazados los cuatro patrones de diseño por otros cuatro con anclaje real (§5.1). Separada la capa de presentación en el diagrama de paquetes para eliminar un ciclo. Agregado el control de versiones a los documentos del proyecto.
  **Próxima etapa: Diseño.**
- **15/09/2026** — **FLUJO DE DISEÑO PRODUCIDO.** Generado `DISEÑO_MiBlog.md` 1.0 con los seis artefactos sobre los 10 casos de uso: arquitectura en cuatro capas con tabla de mecanismos, un único diagrama de clases de diseño con los cuatro patrones adentro, despliegue de un nodo, subsistemas en capas, diez secuencias con fragmentos `alt` y los estados de `Mensaje` y `Usuario`. Verificado que los diez casos de uso se realizan. Registrados doce hallazgos (§5.2): seis esperan mi confirmación y los demás son correcciones a documentos anteriores. Corregida en el índice la versión de `ANALISIS_MiBlog.md` (figuraba 2.0, está en 2.1).
  **Próxima etapa: confirmar los hallazgos y pasar a Implementación.**
- **15/09/2026** — **FLUJO DE DISEÑO CERRADO.** Confirmadas las seis decisiones: H1 con la limpieza de sesiones vencidas agregada, H2, H5, H7 (opción A, con la respuesta para la defensa escrita), H9 y H10 (con la dependencia declarada también en los requisitos no funcionales). Aplicadas las correcciones: `ESPECIFICACIONES_CASOS_DE_USO_MiBlog.md` 1.2, `ANALISIS_MiBlog.md` 2.2 y `REQUISITOS_NO_FUNCIONALES_MiBlog.md` 1.1, que ahora cumple la regla de control de versiones. `DISEÑO_MiBlog.md` a 1.1, con el `ca 7.4` como rama `alt` en la secuencia de CU0007.
  **Próxima etapa: Implementación** (originalmente prevista en Claude Code; ver la entrada del 22/10).
- **22/10/2026** — **Nuevo plazo y nuevo método de implementación.** La entrega y defensa pasan al 24/11/2026. La Implementación se hace en chats de este proyecto y no en Claude Code, para poder explicar el código en la defensa, en seis bloques que terminan cada uno en algo que se puede correr (`PLAN_DEL_PROYECTO.md` 1.6).
- **23/10/2026** — **ETAPA 4 ABIERTA.** Se agregó el informe de cierre de bloque y se fijó cómo entra el diseño visual (solo decisiones visuales, escritas a mano; sin Tailwind, CDN ni JavaScript). `PLAN_DEL_PROYECTO.md` 1.7.
- **24/10/2026** — **BLOQUE 4.1 CERRADO.** Construidos los cimientos: estructura de carpetas, `.gitignore`, `.env.example`, `requirements.txt`, `conexion.py`, `esquema.sql`, las clases del dominio con las 14 excepciones, `crear_app()` mínimo con el comando `iniciar-bd`, la hoja de estilos completa y la plantilla base. Probado y commiteado. Decididos el repositorio único con las cinco etapas, las fuentes propias del diseño y la regla de la barra superior (solo con sesión iniciada). Tres puntos de la §2.4 del diseño se corrigieron después (DV-1 a DV-3). Creado `CONTEXTO_IMPLEMENTACION_MiBlog.md`, el documento de traspaso entre bloques.
  **Próxima etapa: bloque 4.2, sesión (CU0001, CU0002, CU0003).** Antes de abrirlo: aplicar las fuentes propias (P-1).
- **24/10/2026 (más tarde)** — Pasadas al diseño las correcciones de la §2.4 (`DISEÑO_MiBlog.md` 1.3). Decidido que **el cierre de sesión sigue el diseño**: una pantalla de confirmación sin barra y no la pantalla "Cerraste sesión" del prototipo (D-11). `CONTEXTO_IMPLEMENTACION_MiBlog.md` 1.1.
- **24/10/2026 (cierre del 4.2)** — **BLOQUE 4.2 CERRADO.** Construidos CU0001, CU0002 y CU0003: repositorios de usuarios y de sesiones, almacén de fotos, controles de registro y de autenticación, `GuardiaSesion`, las vistas de sesión y cuatro plantillas. Probado por mí en mi máquina. Decididos "clave" en lugar de "contraseña", el registro exitoso respondido desde el mismo `POST`, el tamaño máximo de foto configurable, `GuardiaSesion` lista para rutas protegidas y `diagnostico.py` como herramienta local (D-12 a D-16); registrado el desvío DV-4. `CONTEXTO_IMPLEMENTACION_MiBlog.md` 1.3.
- **26/10/2026** — **BLOQUE 4.3 CERRADO.** Construidos CU0014 y CU0011: `RepositorioSeguimientos`, `ControlBusquedaUsuarios`, `ControlSeguimiento`, `VistaBusquedaUsuarios` y `busqueda.html`, más dos métodos nuevos en `RepositorioUsuarios`. La búsqueda ignora mayúsculas y acentos y no muestra el correo; a quien ya sigo lo marca «Siguiendo», sin botón. Son las primeras rutas protegidas por `GuardiaSesion`. Probado por mí con dos cuentas y commiteado en cinco commits, uno por capa. Decididos D-17 a D-21 (resultados sin descripción, la propia cuenta sin botón, orden por nombre completo, Post/Redirect/Get con el criterio, campo `type="text"`); registrados el desvío DV-5 y el pendiente P-10 (texto de ayuda de la búsqueda). `CONTEXTO_IMPLEMENTACION_MiBlog.md` 1.4, `PLAN_DEL_PROYECTO.md` 1.10 y este documento (que ya no reflejaba el 4.2).
  **Próxima etapa: bloque 4.4, mensajes y tablón (CU0004, CU0009).** Es el bloque con más patrones; P-10 ya está resuelto (D-22).
- **26/10/2026 (más tarde)** — Decididos los textos de ayuda de los campos (D-22): inicio de sesión sin el «tu.usuario» del diseño visual, registro con una pista por campo (límites y formato) y búsqueda con la línea de ayuda acortada. Resuelto P-10. Abel lo commiteó y lo subió al repositorio; queda libre el camino al bloque 4.4. `CONTEXTO_IMPLEMENTACION_MiBlog.md` 1.5.
- **27/10/2026** — **BLOQUE 4.4 CERRADO.** Construidos CU0004 y CU0009: los repositorios de mensajes, de republicaciones y de elementos; los cuatro patrones (Strategy y Factory Method en `Extractor` y sus tres concretos, Template Method en `OperacionSobreMensaje` y `Publicacion`, Decorator de lectura en el tablón); `ControlPublicacion`, `ControlTablon`, `VistaTablon`, `tablon.html` y `contador.js` (el único JavaScript del proyecto). Corrí las 83 pruebas automáticas (todas pasan), probé la aplicación con datos de demostración y pedí cerrar el bloque. Decididos D-23 a D-32: etiquetas en minúsculas, cómo se reconocen etiquetas, menciones y enlaces, normalización del texto, formato de las fechas, pruebas con `unittest`, contador pasado del límite, saltos de línea, rnf 9.3 medido, `sembrar_datos.py` dentro del repositorio y `README.md` autocontenido. Registrados el desvío DV-6 y los pendientes P-11 a P-16. Las seis comprobaciones de §2.7 dan el resultado esperado. `CONTEXTO_IMPLEMENTACION_MiBlog.md` 1.6, `PLAN_DEL_PROYECTO.md` 1.12, `00_INDICE.md` 1.12 y este documento.
  **Próxima etapa: bloque 4.5, edición, borrado y republicación (CU0005, CU0006, CU0007).** Antes de abrirlo anoto los hashes de los commits del 4.4 (P-16).
- **27/10/2026 (más tarde)** — **BLOQUE 4.5 CERRADO.** Construidos CU0005, CU0006 y CU0007: `Edicion` (segunda subclase del Template Method), `ControlRepublicacion`, los métodos de edición y borrado de `ControlPublicacion`, los métodos nuevos de los repositorios de mensajes y de republicaciones, los diálogos de edición y de borrado, los botones del tablón y las cinco rutas nuevas (15 en total). Con eso el Decorator quedó completo: editar el mensaje original se ve en sus republicaciones sin copiar texto. Corrí las 183 pruebas (todas pasan), probé con dos cuentas editar, borrar en cascada y republicar, y commiteé en seis commits por capa. Decididos D-33 a D-36 (la marca «(editado el …)» con fecha, los avisos de cada curso alternativo, el diálogo de borrado que muestra el texto del mensaje, y los comentarios sin números de bloque); registrados el desvío DV-7 y el pendiente P-17. Las seis comprobaciones de §2.7 dan el resultado esperado. `CONTEXTO_IMPLEMENTACION_MiBlog.md` 1.7, `PLAN_DEL_PROYECTO.md` 1.13, `00_INDICE.md` 1.13 y este documento.
  **Próxima etapa: bloque 4.6, cierre del código.** Antes de abrirlo anoto los hashes del 4.4 que faltan (P-16).
- **28/10/2026** — **BLOQUE 4.6 CERRADO. ETAPA 4 (IMPLEMENTACIÓN) CERRADA.** Cerrado el código de los diez casos de uso. Se programaron las páginas de error y el archivo de registro de eventos (`errores_web.py`, `error.html` e `instance/miblog.log`; D-37 y D-42), el nombre de usuario con su forma admitida (solo letras, números y guion bajo; punto y guion únicamente en el medio; D-38) y la franja de marca en el inicio de sesión y en el registro (D-43, un detalle del diseño visual que pedí conservar). Se agregaron 79 pruebas (CU0001, CU0002, CU0003, CU0011, CU0014 y errores): son 262 en total y pasan, también tratando los `ResourceWarning` como error; el chat rompió el código a propósito 39 veces y la suite las detectó todas. Decidí programar el manejo de errores, restringir el formato del nombre de usuario, declarar todos los límites conocidos (16, en el `README.md`) y agregar las pruebas que faltaban (D-37 a D-41). Dejé la carpeta limpia (borrados `diagnostico.py` e `instance/diagnostico.log`, sin comentarios «Bloque 4.x»), actualicé el prototipo de interfaces al diseño implementado y commiteé en once commits (`eeeb3a7` a `b105686`). Los desvíos DV-4 a DV-8 pasaron al diseño (`DISEÑO_MiBlog.md` 1.4) y la forma del nombre de usuario a las especificaciones (`ESPECIFICACIONES_CASOS_DE_USO_MiBlog.md` 1.3). Las seis comprobaciones de §2.7 dan el resultado esperado. `CONTEXTO_IMPLEMENTACION_MiBlog.md` 1.8, `PLAN_DEL_PROYECTO.md` 1.14, `00_INDICE.md` 1.14 y este documento.
  **Próxima etapa: Etapa 5, Prueba** (Plan, Casos y Procedimientos de prueba, solo sobre los 10 casos de uso realizados). Antes: commitear los documentos actualizados (P-19) y regenerar `clases.png` (P-18).
---
 
## 9.1 Dónde estoy y qué sigue
 
**Etapas cerradas:** Requisitos, Análisis, Diseño e Implementación (esta última en chats de este proyecto, no en Claude Code, en seis bloques; cerrada el 28/10/2026).
**Sigue:** **Prueba** (Etapa 5), sobre los 10 casos de uso realizados, y después el Cierre (trazabilidad, coherencia y defensa).
 
**Lo que Implementación heredó de Diseño** (y que la pasada de coherencia vuelve a comprobar):
 
1. La **estructura de carpetas y los nombres de archivo** de `DISEÑO_MiBlog.md` §2.4, dentro de `4. Implementacion/codigo/` (DV-1 a DV-3, ya aplicados en el diseño 1.3).
2. Las **15 rutas** con su método HTTP, su clase y su método (§2.5), y la regla Post/Redirect/Get.
3. El **esquema SQL** (§2.6), con `PRAGMA foreign_keys = ON` en cada conexión y el borrado en cascada hecho por el código, no por la base.
4. Los **nombres de clases, atributos y métodos** del diagrama integral (§3). Si uno cambia al programar, se cambia en el diagrama el mismo día; mientras tanto se anota en el documento de contexto.
5. Las **14 excepciones de negocio**, una por curso alternativo que rechaza una operación (§2.6).
6. El **orden de los mensajes** de cada caso de uso (§6), en particular las dos verificaciones de autoría de CU0005 y CU0006.
7. Las **seis comprobaciones mecánicas** de §2.7, que se corren sobre el repositorio en la pasada de coherencia.
8. **`requirements.txt` con Flask y `python-dotenv`, y nada más** (`REQUISITOS_NO_FUNCIONALES_MiBlog.md` §8.0).
9. **La limpieza de sesiones** en los dos momentos de H1, y el filtro `activo = 1` en las cinco consultas de `DISEÑO_MiBlog.md` §7.2.
10. **Cada chat nuevo lee los documentos de este proyecto y nada más**: por eso lo decidido al programar se anota en `CONTEXTO_IMPLEMENTACION_MiBlog.md` al cerrar cada bloque.
**Lo que Prueba ya tiene anotado para no olvidarlo:**
 
- El `ca 7.1` se prueba **por interfaz**: A sigue a B y no sigue a C; B, que sí sigue a C, republica un mensaje de C; A intenta republicarlo desde su tablón (H5).
- Los datos de prueba incluyen **un usuario con `activo = 0`**, para `ca 2.1`, `ca 11.1` y `{Ob 14.2}` (H7).
- El `ca 7.4` (mensaje borrado antes de republicar) tiene su caso, igual que `ca 5.1` y `ca 6.1` (H6).
- Un caso directo del Decorator: editar un mensaje republicado y verificar que la republicación muestra el texto nuevo (ANALISIS §8.7). Ya tiene prueba automática desde el 4.5 (`test_edicion_y_borrado.py` y `test_web_edicion_republicacion.py`), igual que `ca 7.1` (con el caso de H5), `ca 7.4`, `ca 5.1` y `ca 6.1`: la Etapa 5 los mapea a casos de prueba.
- El **rnf 9.3** («menos de 3 segundos con el juego de datos de prueba definido para el proyecto») ya tiene una prueba automática con un volumen que elegí durante la Implementación: 100 usuarios, 5.000 mensajes, 500 republicaciones y 20 seguidos (D-30). El Plan de pruebas tiene que declarar ese volumen y definir el juego de datos (P-15).
- `sembrar_datos.py` (en el repositorio, D-31) ya trae un usuario con `activo = 0`, un tablón vacío (`ca 9.1`) y una republicación de alguien a quien no se sigue (H5): puede servir de base para el juego de datos. **No decidido** (P-15).
- Las 262 pruebas automáticas de `codigo/pruebas/` citan los `ca` y `rnf` que verifican, así que se pueden mapear en la matriz de trazabilidad.
- La forma del nombre de usuario (`rnf 1.1`, `{Ob 1.3}`) ya tiene prueba automática en `test_registro.py`; el inicio de sesión no la aplica, a propósito (D-38).
- Las páginas de error y el archivo de registro (RNF16 y RNF24) tienen pruebas en `test_errores_web.py`. El RNF24 también habla del proceso semanal de resumen por correo, que no está en esta versión: no hay nada que probar de él.
- Los 16 límites conocidos del `README.md` (D-39) son comportamiento declarado: ningún caso de prueba debe esperar otro.
---
 
## 10. Recordatorios permanentes
 
1. UMBook es **referencia de formato, no de contenido**.
2. Un **solo** diagrama de casos de uso para toda la aplicación.
3. Coherencia tecnológica entre texto, despliegue, subsistemas, pruebas y código.
4. La **frase de alcance** va en arquitectura y en el plan de pruebas. Sin ella, 10 CU no son una decisión: son 11 que faltan.
5. No prometer números en los RNF que ninguna prueba verifique.
6. Secretos en `.env`; `.env`, base de datos y cachés **fuera** del repositorio.
7. Revisar antes de entregar: códigos de CU únicos, encabezados actualizados, sin restos de plantilla ni de otro proyecto.
8. **El modo típico de fracasar** no es escribir lento: es volver a cambiar el conjunto de casos de uso o el stack a mitad de camino. Ambos están cerrados. No se tocan.
9. **Cada bloque de Implementación termina actualizando `CONTEXTO_IMPLEMENTACION_MiBlog.md` y subiéndolo al proyecto antes de abrir el siguiente.** Sin eso, el chat que sigue no sabe qué se hizo.
10. **El código quedó cerrado el 28/10/2026.** Si la Etapa 5 encuentra un defecto y se corrige, el cambio se anota en `CONTEXTO_IMPLEMENTACION_MiBlog.md` (decisión o desvío nuevo) y se sube su versión.
---
 
## Control del documento
 
| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.10 | 27/10/2026 | Gestión del proyecto | **Bloque 4.4 cerrado; 7 de 10 casos de uso funcionando.** Encabezado, §5.1 (estado de los patrones en el código), §7 (Implementación: 4.4 cerrado, 4.5 siguiente, 4.6 ajustado, fila de pruebas automáticas, DV-6 sin pasar), §9 (bitácora del 27/10) y §9.1 (dónde estoy; notas para Prueba: rnf 9.3, `sembrar_datos.py`, pruebas mapeables). CONTEXTO a 1.6 y PLAN a 1.12. |
| 1.11 | 27/10/2026 | Gestión del proyecto | **Bloque 4.5 cerrado; los 10 casos de uso funcionando.** Encabezado, §5.1 (Template Method y Decorator completos), §7 (Implementación: 4.5 cerrado, 4.6 siguiente, 10 de 10, 183 pruebas, DV-7 sin pasar al diseño), §9 (bitácora del cierre del 4.5) y §9.1 (dónde estoy; el caso del Decorator y los `ca` 5.1, 6.1, 7.1 y 7.4 ya tienen prueba automática). CONTEXTO a 1.7 y PLAN a 1.13. |
| 1.12 | 28/10/2026 | Gestión del proyecto | **Bloque 4.6 cerrado; Etapa 4 (Implementación) cerrada.** Encabezado, §5 (fila de errores y registro), §5.1 (estado de los patrones), §7 (Requerimientos: ESPECIFICACIONES 1.3 y prototipo actualizado; Diseño: 1.4 y desvíos pasados; Implementación: cerrada, 262 pruebas, once commits; avance de «Documentación anexa»), §9 (bitácora del cierre del 4.6), §9.1 (dónde estoy; notas para Prueba) y §10 (recordatorio 10). CONTEXTO a 1.8 y PLAN a 1.14. |
| 1.13 | 28/10/2026 | Gestión del proyecto | **Corrección de una afirmación falsa que venía desde la versión 1.0.** La §1 decía «Alcance acordado con la cátedra» y dejaba como pendiente «tener la autorización por escrito», dando por hecho un acuerdo verbal. **No hubo ninguna conversación con la cátedra sobre el alcance.** Las tres líneas de la §1 ahora dicen que el recorte es una decisión propia del alumno, con su fundamento real (proyecto para grupos de ocho cursado en solitario; cuatro casos de uso como mínimo comentado por compañeros; diez realizados) y con el pendiente de conversarlo antes del 24/11. PLAN a 1.15 e índice a 1.15. |
