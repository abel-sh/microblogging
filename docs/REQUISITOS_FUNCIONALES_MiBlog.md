# LISTA DE REQUISITOS FUNCIONALES — Sistema MiBlog

**Versión:** 1.1 · **Última modificación:** 28/10/2026 · **Etapa:** Requisitos

**Materia:** Ingeniería de Software · **Alumno:** Abel · **Modalidad:** proyecto planteado para grupos de ocho personas, cursado y entregado en solitario
**Flujo del Proceso Unificado:** Requisitos
**Trabajador responsable:** Analista de Sistemas
**Documento previo:** `REQUISITOS_CANDIDATOS_MiBlog.md`
**Estado del documento:** `[DECIDIDO]` — cerrado el 13/09/2026, al cerrarse el flujo de Requisitos. Los RF01–RF21 y las reglas RA01–RA11 no volvieron a cambiar: el análisis, el diseño, el código y las pruebas se construyeron sobre ellos.

---

## 1. Qué es este documento y de dónde sale

Un requisito funcional describe **qué tiene que hacer el sistema**.

Este documento toma las 25 características **aprobadas** de la lista de requisitos candidatos y las expresa como requisitos funcionales, separándolas de los requisitos no funcionales, que van en su propio documento.

### 1.1 Relación con los casos de uso

En el Proceso Unificado los requisitos funcionales **no se entregan como una lista suelta de frases**: se organizan en casos de uso. Ese es el sentido de decir que el PU está *dirigido por casos de uso*. El caso de uso es la unidad que se propaga después a análisis, diseño, código y pruebas; una frase suelta no se puede seguir a través de los flujos.

Por eso cada requisito funcional de este documento tiene un caso de uso asociado. **No son dos cosas distintas:** son el mismo requisito visto desde dos lugares. La lista sirve para verificar cobertura; el caso de uso sirve para trabajar.

### 1.2 Códigos usados

| Código | Significa |
|---|---|
| **R00–R17** | Requisito escrito literalmente en `enunciado_microblogging.pdf`. |
| **C01–C38** | Característica de la lista de requisitos candidatos. |
| **RF** | Requisito funcional de este documento. |
| **RA** | Regla funcional automática (sección 4). |
| **CU** | Caso de uso del modelo de casos de uso. |

---

## 2. Requisitos funcionales

| RF | Requisito funcional | Candidato | Enunciado | Caso de uso | Actor primario |
|---|---|---|---|---|---|
| RF01 | El sistema debe permitir a una persona sin cuenta registrarse indicando nombre de usuario, email, clave, nombre completo, descripción y foto. | C01 | R03 | CU0001 Registrar usuario | Visitante |
| RF02 | El sistema debe permitir a un usuario registrado autenticarse y abrir una sesión. | C17 | — | CU0002 Iniciar sesión | Visitante |
| RF03 | El sistema debe permitir a un usuario cerrar su sesión. | C17 | — | CU0003 Cerrar sesión | Usuario |
| RF04 | El sistema debe permitir a un usuario publicar un mensaje de texto de hasta 140 caracteres, registrando su autor y su fecha de publicación. | C02, C03 | R01, R05 | CU0004 Publicar mensaje | Usuario |
| RF05 | El sistema debe permitir a un usuario modificar el texto de un mensaje propio. | C12 | R13 | CU0005 Editar mensaje propio | Usuario |
| RF06 | El sistema debe permitir a un usuario eliminar un mensaje propio. | C12 | R13 | CU0006 Borrar mensaje propio | Usuario |
| RF07 | El sistema debe permitir a un usuario republicar hacia sus seguidores un mensaje de su tablón creado por alguien a quien sigue. | C10, C23 | R11 | CU0007 Republicar mensaje | Usuario |
| RF08 | El sistema debe permitir a un usuario enviar un mensaje dirigido a un único destinatario. | C11 | R12 | CU0008 Enviar mensaje privado | Usuario |
| RF09 | El sistema debe mostrar al usuario un tablón con los mensajes de los usuarios a los que sigue y los propios. | C06 | R04, R05 | CU0009 Visualizar tablón | Usuario |
| RF10 | El sistema debe permitir a un usuario consultar el muro de otro usuario: su foto, su descripción y sus mensajes públicos. | C20 | — | CU0010 Consultar muro de un usuario | Usuario |
| RF11 | El sistema debe permitir a un usuario seguir a otro usuario. | C18 | R02 | CU0011 Seguir usuario | Usuario |
| RF12 | El sistema debe permitir a un usuario dejar de seguir a otro usuario. | C18 | — | CU0012 Dejar de seguir usuario | Usuario |
| RF13 | El sistema debe permitir al usuario consultar, desde la página principal, quiénes son sus seguidores y a quiénes sigue. | C07 | R08 | CU0013 Consultar seguidores y seguidos | Usuario |
| RF14 | El sistema debe permitir buscar usuarios por nombre de usuario o nombre completo. | C21 | — | CU0014 Buscar usuarios | Usuario |
| RF15 | El sistema debe mostrar el listado de temas del momento: las etiquetas más repetidas en los últimos `n` días. | C08 | R09 | CU0015 Ver temas del momento | Usuario |
| RF16 | El sistema debe permitir obtener el listado de mensajes públicos que contienen una etiqueta determinada. | C05, C22 | R07, R15 | CU0016 Buscar mensajes por etiqueta | Usuario |
| RF17 | El sistema debe permitir al administrador modificar la cantidad de días `n` usada para calcular los temas del momento. | C09, C24 | R10 | CU0017 Configurar ventana de días `n` | Administrador |
| RF18 | El sistema debe permitir al administrador registrar una aplicación externa, emitirle su credencial y darla de baja. | C16, C24, C25 | R17 | CU0018 Registrar aplicación externa | Administrador |
| RF19 | El sistema debe enviar, una vez por semana, un email a cada usuario con el listado de temas del momento y los links al listado de mensajes de cada etiqueta. | C13, C14 | R14, R15 | CU0019 Enviar email semanal de temas del momento | Tiempo |
| RF20 | El sistema debe permitir a una aplicación registrada publicar un mensaje mediante la API REST. | C15, C25 | R16, R17 | CU0020 Publicar mensaje vía API REST | Aplicación Externa |
| RF21 | El sistema debe permitir a una aplicación registrada leer el muro de un usuario mediante la API REST. | C15, C25 | R16, R17 | CU0021 Leer muro de un usuario vía API REST | Aplicación Externa |

**Total: 21 requisitos funcionales, uno por caso de uso.**

---

## 3. Cobertura del enunciado

Ningún requisito del enunciado queda sin requisito funcional.

| Requisito del enunciado | Cubierto por |
|---|---|
| R00 — Mejorar la comunicación entre empleados (objetivo) | El sistema en su conjunto. Es el propósito, no una función. |
| R01 — Mensajes de hasta 140 caracteres | RF04 y el requisito no funcional de longitud |
| R02 — Los mensajes llegan a los seguidores | RF09, RF11 |
| R03 — Datos de registro | RF01 |
| R04 — Tablón con mensajes de seguidos y propios | RF09 |
| R05 — Autor, fecha y texto en cada mensaje | RF04, RF09 |
| R06 — Links, menciones y etiquetas en el texto | RF04, RF05 y la regla RA01 |
| R07 — Clasificación por etiquetas para búsquedas y estadísticas | RF15, RF16 |
| R08 — Consultar seguidores y seguidos | RF13 |
| R09 — Temas del momento | RF15 y la regla RA03 |
| R10 — `n` configurable por el administrador | RF17 |
| R11 — Republicar | RF07 |
| R12 — Mensaje privado | RF08 |
| R13 — Borrar y editar mensajes propios | RF05, RF06 |
| R14 — Email semanal | RF19 |
| R15 — Links a los mensajes de cada etiqueta en el email | RF16, RF19 |
| R16 — Servicios REST para publicar y leer el muro | RF20, RF21 |
| R17 — Acceso restringido a aplicaciones registradas | RF18, RF20, RF21 |

---

## 4. Reglas funcionales automáticas

Son comportamientos obligatorios del sistema que **no constituyen un requisito funcional independiente ni un caso de uso**, porque ningún actor los inicia: ocurren dentro de otro caso de uso, sin que nadie los pida.

Se documentan acá para que no se pierdan entre el enunciado y el código, y se referencian desde la especificación de los casos de uso correspondientes.

| RA | Regla | Ocurre dentro de | Origen |
|---|---|---|---|
| RA01 | Al publicar o editar un mensaje, el sistema extrae del texto las etiquetas que comienzan con `#`, las menciones que comienzan con `@` y los links, y los registra como elementos propios del mensaje. | RF04, RF05 | R06, R07 |
| RA02 | Si una etiqueta extraída no existe todavía en el sistema, se crea en ese momento. | RF04, RF05 | R07 |
| RA03 | Los temas del momento se calculan contando las apariciones de cada etiqueta en los mensajes públicos publicados dentro de los últimos `n` días, tomando `n` de la configuración vigente al momento del cálculo. | RF15, RF19 | R09, R10 |
| RA04 | Los mensajes privados no se incluyen en el conteo de temas del momento, ni en los muros, ni en los tablones, ni en las respuestas de la API. | RF08, RF15, RF19, RF21 | R12, C19 |
| RA05 | Al editar un mensaje, el sistema registra la fecha de edición y lo marca como editado. Las republicaciones existentes muestran el texto actualizado, por ser referencias al mensaje original. | RF05 | C23 |
| RA06 | Al borrar un mensaje, se eliminan también todas sus republicaciones. | RF06 | R13, C23 |
| RA07 | El tablón de un usuario está formado por sus propios mensajes, los de los usuarios a los que sigue y las republicaciones hechas por esos usuarios, ordenados del más reciente al más antiguo. | RF09 | R04 |
| RA08 | Un usuario no puede seguirse a sí mismo ni seguir dos veces al mismo usuario. | RF11 | C18 |
| RA09 | Solo se pueden republicar mensajes públicos de usuarios a los que se sigue. | RF07 | R11 |
| RA10 | Un mensaje publicado mediante la API queda registrado con el usuario en cuyo nombre se publicó y con la aplicación que lo originó. | RF20 | R16, R17 |
| RA11 | El resumen semanal se envía a todos los usuarios activos. Si el envío a un destinatario falla, el sistema registra el error y continúa con los demás. | RF19 | R14 |

---

## 5. Resumen

- **21 requisitos funcionales**, derivados de las 25 características aprobadas y expresados como 21 casos de uso.
- **11 reglas funcionales automáticas**, referenciadas desde las especificaciones de los casos de uso.
- **Los 17 requisitos del enunciado quedan cubiertos en su totalidad**, más el objetivo general R00 que no se traduce a una función.

---

## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.0 | 13/09/2026 | Requisitos | Versión inicial: los 21 requisitos funcionales RF01–RF21, uno por caso de uso, con su traza a las características candidatas y al enunciado; la cobertura inversa de R00–R17; y las 11 reglas funcionales automáticas RA01–RA11. |
| 1.1 | 28/10/2026 | Requisitos | **Encabezado de versión y bloque de control**, que faltaban (P-6). **Estado del documento de `[PROPUESTA]` a `[DECIDIDO]`**, con la fecha en que quedó cerrado: la marca anterior ya no describía su estado real, porque todo el proyecto se construyó sobre estos requisitos. Modalidad del encabezado alineada con el resto de los documentos. |
