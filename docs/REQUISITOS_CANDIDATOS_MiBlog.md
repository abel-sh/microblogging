# LISTA DE REQUISITOS CANDIDATOS — Sistema MiBlog

**Versión:** 1.1 · **Última modificación:** 28/10/2026 · **Etapa:** Requisitos

**Materia:** Ingeniería de Software · **Alumno:** Abel · **Modalidad:** proyecto planteado para grupos de ocho personas, cursado y entregado en solitario
**Flujo del Proceso Unificado:** Requisitos · **Actividad:** Enumerar los requisitos candidatos
**Trabajador responsable:** Analista de Sistemas
**Estado del documento:** `[DECIDIDO]` — cerrado el 13/09/2026, al cerrarse el flujo de Requisitos. Las características C01–C38 y sus estados no volvieron a cambiar: el análisis, el diseño, el código y las pruebas se construyeron sobre esta lista.

---

## 1. Qué es este documento

Es la **lista de características deseadas del sistema**. Es el primer artefacto del flujo de Requisitos: se arma antes de separar requisitos funcionales de no funcionales y antes de escribir un solo caso de uso.

Incluye tanto lo que se va a construir como lo que se evaluó y quedó afuera. Ese es su valor: deja por escrito que cada característica descartada fue **evaluada y descartada**, no olvidada.

De cada característica se registran los seis campos que pide el Proceso Unificado:

| Campo | Qué es |
|---|---|
| **Nombre corto** | Cómo se la nombra en todo el proyecto. |
| **Descripción** | Qué hace, en una frase. |
| **Estado** | Propuesto, aprobado, incluido o validado. |
| **Coste estimado** | Recursos necesarios y horas-hombre. |
| **Prioridad** | Crítico, importante o secundario. |
| **Nivel de riesgo** | Crítico, significativo u ordinario. |

---

## 2. Cómo leer los campos

### 2.1 Estado

Los cuatro estados son etapas sucesivas de la vida de una característica:

| Estado | Significado | Cuándo se alcanza |
|---|---|---|
| **Propuesto** | Se registró y se evaluó, pero todavía no se aprobó su inclusión. | Al enumerarla. |
| **Aprobado** | Se decidió que forma parte del sistema. | Al cerrar el alcance. |
| **Incluido** | Ya está implementada en una versión del sistema. | Al terminar la implementación. |
| **Validado** | Se verificó que cumple lo esperado. | Al ejecutar las pruebas. |

**En esta entrega:** las características que forman parte del sistema figuran como **aprobado**. Pasarán a *incluido* y *validado* a medida que avancen la implementación y las pruebas. Las que quedaron afuera se mantienen en **propuesto**, que es lo correcto: se registraron, se evaluaron y no se aprobaron. Cada una lleva el motivo en la sección 5.

### 2.2 Coste estimado

El único tipo de recurso del proyecto es **una persona** cumpliendo todos los roles, porque el trabajo es individual. Donde hace falta algo más, está indicado en la descripción.

Las horas-hombre estimadas cubren el ciclo completo de esa característica: análisis, diseño, implementación y prueba. **No son las horas de esta entrega**, son las que costaría el sistema terminado.

### 2.3 Prioridad

Mide la importancia de la característica **para el objetivo del sistema**, que es mejorar la comunicación entre los empleados de la empresa.

- **Crítico** — sin esto el sistema no cumple su objetivo.
- **Importante** — el sistema funciona sin esto, pero queda notoriamente incompleto.
- **Secundario** — mejora la experiencia, no cambia el objetivo.

### 2.4 Nivel de riesgo

Mide qué tan probable es que la implementación se complique.

- **Crítico** — depende de algo que todavía no sé resolver o que está fuera de mi control.
- **Significativo** — tiene una parte no trivial: un algoritmo, una integración, un efecto sobre otras características.
- **Ordinario** — alta, baja, modificación o consulta sin complicaciones.

### 2.5 Origen

- **Enunciado (R##)** — está escrito literalmente en `enunciado_microblogging.pdf`.
- **Supuesto propio** — no está en el enunciado. Se agregó porque sin esa característica el enunciado no cierra. Cada uno lleva su justificación.
- **Propuesta** — idea evaluada que no viene ni del enunciado ni de una necesidad estructural.

---

## 3. Características aprobadas — provenientes del enunciado

| ID | Nombre corto | Descripción | Origen | Estado | Coste | Prioridad | Riesgo |
|---|---|---|---|---|---|---|---|
| C01 | Registro de usuarios | Alta de cuenta con nombre de usuario, email, clave, nombre completo, descripción y foto. | R03 | Aprobado | 10 h | Crítico | Significativo |
| C02 | Publicación de mensajes | Publicar un texto de hasta 140 caracteres. | R01 | Aprobado | 12 h | Crítico | Ordinario |
| C03 | Datos del mensaje | Cada mensaje conserva y muestra autor, fecha de publicación y texto. | R05 | Aprobado | 2 h | Importante | Ordinario |
| C04 | Contenido enriquecido del mensaje | El texto admite links, menciones con `@` y etiquetas con `#`, que el sistema reconoce y registra por separado. | R06 | Aprobado | 10 h | Crítico | Significativo |
| C05 | Clasificación por etiquetas | Las etiquetas clasifican el contenido para permitir búsquedas y estadísticas posteriores. | R07 | Aprobado | 6 h | Importante | Ordinario |
| C06 | Tablón de anuncios | Listado donde aparecen los mensajes de los usuarios seguidos y los propios. | R04 | Aprobado | 14 h | Crítico | Significativo |
| C07 | Consulta de seguidores y seguidos | Desde la página principal, ver quiénes lo siguen y a quiénes sigue. | R08 | Aprobado | 4 h | Importante | Ordinario |
| C08 | Temas del momento | Listado de las etiquetas más repetidas en los últimos `n` días. | R09 | Aprobado | 12 h | Crítico | Significativo |
| C09 | Configuración de la ventana de días | El administrador modifica el valor de `n` sin intervención técnica. | R10 | Aprobado | 4 h | Importante | Ordinario |
| C10 | Republicación de mensajes | Reenviar a los propios seguidores un mensaje del tablón creado por alguien a quien se sigue. | R11 | Aprobado | 8 h | Importante | Significativo |
| C11 | Mensaje privado | Publicar un mensaje dirigido a un único destinatario. | R12 | Aprobado | 6 h | Importante | Ordinario |
| C12 | Edición y borrado de mensajes propios | Modificar o eliminar los mensajes que uno publicó. | R13 | Aprobado | 8 h | Importante | Significativo |
| C13 | Resumen semanal por email | Una vez por semana el sistema envía a los usuarios un email con los temas del momento. Requiere servidor de correo y planificador de tareas. | R14 | Aprobado | 16 h | Crítico | Crítico |
| C14 | Links del resumen semanal | El email incluye, por cada etiqueta, el link al listado de mensajes que la contienen. | R15 | Aprobado | 3 h | Importante | Ordinario |
| C15 | API REST de publicación y lectura | Servicios web para publicar un mensaje y leer el muro de un usuario desde otro sistema. | R16 | Aprobado | 14 h | Crítico | Significativo |
| C16 | Registro de aplicaciones autorizadas | Solo las aplicaciones registradas pueden usar la API. | R17 | Aprobado | 8 h | Importante | Significativo |

---

## 4. Características aprobadas — supuestos propios

Ninguna de estas está escrita en el enunciado. Se aprobaron porque sin ellas el sistema no funciona o el enunciado queda incompleto. La justificación de cada una es parte del documento.

| ID | Nombre corto | Descripción | Origen | Estado | Coste | Prioridad | Riesgo |
|---|---|---|---|---|---|---|---|
| C17 | Inicio y cierre de sesión | El usuario se autentica para operar y puede cerrar su sesión. **Justificación:** el enunciado habla de "mensajes propios" y "sus seguidores"; sin sesión el sistema no sabe quién es el usuario. La cátedra además exigió el login al grupo de referencia. | Supuesto propio | Aprobado | 10 h | Crítico | Significativo |
| C18 | Seguir y dejar de seguir usuarios | Acción de comenzar o terminar de seguir a otro usuario, sin necesidad de aprobación del seguido. **Justificación:** el enunciado da por existentes a los seguidores pero nunca describe la acción que los crea, y nunca menciona solicitudes ni aceptación. | Supuesto propio | Aprobado | 6 h | Crítico | Ordinario |
| C19 | Visibilidad pública dentro de la empresa | Los mensajes no privados pueden ser leídos por cualquier usuario del sistema; el seguimiento determina qué llega al tablón, no qué se puede leer. **Justificación:** la API expone el muro a aplicaciones que no siguen a nadie, y los temas del momento contarían etiquetas de mensajes inaccesibles si la visibilidad fuera estricta. | Supuesto propio | Aprobado | 2 h | Crítico | Ordinario |
| C20 | Muro público de usuario | Pantalla que muestra la foto, la descripción y los mensajes públicos de un usuario. **Justificación:** el enunciado expone "el muro de un usuario" por API; si la aplicación web no tiene ese concepto, la API expondría algo que en el sistema no existe. | Supuesto propio | Aprobado | 6 h | Importante | Ordinario |
| C21 | Búsqueda de usuarios | Buscar por nombre de usuario o nombre completo. **Justificación:** sin buscador no hay forma de encontrar a quién seguir. | Supuesto propio | Aprobado | 4 h | Secundario | Ordinario |
| C22 | Búsqueda de mensajes por etiqueta | Obtener el listado de mensajes que contienen una etiqueta. **Justificación:** el enunciado exige links "al listado de mensajes que contienen dicha etiqueta"; sin esta pantalla, esos links no tienen destino. | Supuesto propio | Aprobado | 5 h | Importante | Ordinario |
| C23 | Republicación por referencia | La republicación apunta al mensaje original en lugar de copiar su texto; al editarlo, las republicaciones reflejan el texto nuevo y el mensaje queda marcado como editado. **Justificación:** copiar el texto duplicaría el conteo de etiquetas y rompería el cálculo de los temas del momento. | Supuesto propio | Aprobado | 4 h | Importante | Significativo |
| C24 | Rol de administrador del sitio | Usuario con permisos adicionales, limitados a configurar `n` y a gestionar las aplicaciones externas. **Justificación:** el enunciado nombra al "administrador del sitio" y exige que las aplicaciones se registren, pero no define quién las registra. | Supuesto propio | Aprobado | 5 h | Importante | Ordinario |
| C25 | Autenticación de aplicaciones por credencial | Cada aplicación registrada recibe una credencial que debe presentar en cada llamada a la API. **Justificación:** el enunciado exige restringir el acceso pero no define el mecanismo. | Supuesto propio | Aprobado | 6 h | Crítico | Significativo |

---

## 5. Características no aprobadas

Se registraron y se evaluaron. Permanecen en estado **propuesto**: podrían aprobarse en una versión futura del sistema, pero no forman parte de esta.

| ID | Nombre corto | Descripción | Origen | Estado | Coste | Prioridad | Riesgo | Motivo de no aprobación |
|---|---|---|---|---|---|---|---|---|
| C26 | Recuperación de clave | Restablecer la clave olvidada mediante un link enviado por email. | Propuesta | Propuesto | 6 h | Secundario | Ordinario | No está en el enunciado. Sería barata porque la infraestructura de correo ya existe, pero no aporta a ningún requisito pedido. |
| C27 | Notificaciones dentro de la aplicación | Avisar al usuario cuando lo mencionan o cuando gana un seguidor. | Propuesta | Propuesto | 10 h | Secundario | Significativo | El enunciado define un único canal de notificación: el resumen semanal por email. Las menciones existen, pero el enunciado nunca dice que notifiquen. |
| C28 | Búsqueda de texto libre en mensajes | Buscar cualquier palabra dentro del texto de los mensajes. | Propuesta | Propuesto | 10 h | Secundario | Significativo | El enunciado solo pide clasificar y buscar por etiqueta. La búsqueda de texto completo es un problema distinto y más caro. |
| C29 | Estadísticas adicionales de etiquetas | Informes de uso de etiquetas más allá del ranking de temas del momento. | Propuesta | Propuesto | 10 h | Secundario | Significativo | El enunciado menciona "estadísticas" sin especificar cuáles. Se interpreta que el listado de temas del momento satisface esa mención. Cualquier otra queda sin definición suficiente para estimarla. |
| C30 | Edición del perfil | Modificar los datos de la cuenta después del registro. | Propuesta | Propuesto | 6 h | Secundario | Ordinario | No aparece en el enunciado en ninguna forma. |
| C31 | Moderación de contenido | El administrador oculta o elimina mensajes de otros usuarios. | Propuesta | Propuesto | 12 h | Secundario | Significativo | El enunciado limita al administrador a configurar la ventana de días. Agregaría un estado de mensaje que repercute en el resto del modelo. |
| C32 | Baja de usuarios | El administrador deshabilita cuentas. | Propuesta | Propuesto | 5 h | Secundario | Ordinario | Mismo motivo que la moderación. |
| C33 | Aprobación de solicitudes de seguimiento | El seguido debe aceptar antes de que el seguimiento tenga efecto. | Propuesta | Propuesto | 6 h | Secundario | Ordinario | Contradice el seguimiento unilateral aprobado en C18, que es lo que describe el enunciado. |
| C34 | Autenticación de aplicaciones por OAuth | Mecanismo de autenticación por token con servidor de autorización. | Propuesta | Propuesto | 16 h | Secundario | Crítico | Más robusto que la credencial de C25, pero exige un servidor de tokens que no se va a implementar. Documentar un mecanismo que el código no implementa sería una incoherencia entre artefactos. |
| C35 | Respuestas y conversaciones | Responder a un mensaje y ver el hilo resultante. | Propuesta | Propuesto | 14 h | Secundario | Significativo | El enunciado describe publicación, republicación y mensaje privado. No hay hilos. |
| C36 | Marcado de favoritos | Indicar que un mensaje gustó y consultarlos después. | Propuesta | Propuesto | 6 h | Secundario | Ordinario | No está en el enunciado. |
| C37 | Adjuntar imágenes a los mensajes | Incorporar archivos al contenido del mensaje. | Propuesta | Propuesto | 12 h | Secundario | Significativo | El enunciado define el contenido del mensaje como texto con links, menciones y etiquetas. La única imagen del sistema es la foto de perfil. |
| C38 | Aplicación móvil nativa | Cliente instalable para teléfonos. | Propuesta | Propuesto | 80 h | Secundario | Crítico | Fuera de alcance. El sistema es una aplicación web. |

---

## 6. Resumen

| Estado | Cantidad | Coste estimado |
|---|---|---|
| Aprobadas, provenientes del enunciado | 16 | 137 h |
| Aprobadas, supuestos propios | 9 | 48 h |
| **Total aprobado** | **25** | **185 h** |
| No aprobadas (estado propuesto) | 13 | 193 h |
| **Total evaluado** | **38** | **378 h** |

### 6.1 Lectura del coste

Las 185 horas-hombre corresponden al sistema **completo y terminado**: las 25 características aprobadas, con análisis, diseño, implementación y prueba de cada una.

El plazo disponible para esta entrega es sensiblemente menor. Por eso el alcance de implementación se define aparte: **todas las características aprobadas se documentan en su totalidad** (casos de uso, análisis, diseño y pruebas), pero **solo un subconjunto se implementa** en esta versión. El subconjunto se elige por prioridad crítica y riesgo, no por comodidad.

Que una característica esté en estado *aprobado* y no en *incluido* no es un incumplimiento: es exactamente lo que esos estados significan.

### 6.2 Concentración del riesgo

Una sola característica tiene riesgo **crítico** entre las aprobadas: **C13, el resumen semanal por email**. Es la única que depende de un planificador de tareas, de un servidor de correo externo y de un proceso que se ejecuta sin que ninguna persona lo dispare.

En el Proceso Unificado, el riesgo se ataca temprano. Por eso C13 debería estar entre las primeras características diseñadas, aunque su prioridad para el usuario no sea la más alta de la lista.

---

## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.0 | 13/09/2026 | Requisitos | Versión inicial: las 38 características candidatas C01–C38 con los seis campos del Proceso Unificado (nombre corto, descripción, estado, coste estimado, prioridad y nivel de riesgo), separadas en aprobadas del enunciado, aprobadas como supuesto propio y no aprobadas. |
| 1.1 | 28/10/2026 | Requisitos | **Encabezado de versión y bloque de control**, que faltaban (P-6). **Estado del documento de `[PROPUESTA]` a `[DECIDIDO]`**, con la fecha en que quedó cerrado: la marca anterior ya no describía su estado real, porque todo el proyecto se construyó sobre esta lista. Modalidad del encabezado alineada con el resto de los documentos. |
