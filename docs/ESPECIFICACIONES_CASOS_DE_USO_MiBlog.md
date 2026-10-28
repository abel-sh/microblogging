# ESPECIFICACIÓN DE CASOS DE USO — Sistema MiBlog
 
**Materia:** Ingeniería de Software · **Alumno:** Abel · **Modalidad:** proyecto grupal, cursado en solitario
**Flujo del Proceso Unificado:** Requisitos · **Actividad:** Detallar un caso de uso
**Trabajador responsable:** Especificador de Casos de Uso
**Documentos previos:** `REQUISITOS_CANDIDATOS_MiBlog.md` · `REQUISITOS_FUNCIONALES_MiBlog.md` · `REQUISITOS_NO_FUNCIONALES_MiBlog.md` · `DIA1_REQUISITOS_MiBlog.md`
**Versión:** 1.3 · **Última modificación:** 28/10/2026 · **Etapa:** Requisitos
 
> **Alcance de realización.** Esta versión realiza (diseña, implementa y prueba) los casos de uso **CU0001, CU0002, CU0003, CU0004, CU0005, CU0006, CU0007, CU0009, CU0011 y CU0014**. Los restantes quedan especificados en este documento y no forman parte del alcance de implementación, conforme a lo acordado con la cátedra.
 
**Estado del documento:** `[DECIDIDO]` — confirmado el 14/09/2026. Correcciones de la versión 1.2 confirmadas el 15/09/2026, a partir de los hallazgos del flujo de Diseño (`DISEÑO_MiBlog.md` §1).
 
---
 
## Convenciones adoptadas
 
Siete decisiones que la plantilla de la cátedra obliga a tomar, tomadas una sola vez y sostenidas en los 21 casos de uso.
 
**1. Formato del código.** `CU00NN`, cuatro dígitos, igual en el encabezado, en el resumen ejecutivo y en el título.
 
**2. Prioridad numérica.** La plantilla pide un número. Se usa una escala de 1 a 10 que combina la prioridad del requisito candidato con su nivel de riesgo:
 
| Prioridad del candidato | Riesgo | Valor |
|---|---|---|
| Crítico | Crítico o significativo | 10 |
| Crítico | Ordinario | 9 |
| Importante | Significativo | 7 |
| Importante | Ordinario | 6 |
| Secundario | Cualquiera | 3 |
 
**3. Requerimientos no funcionales locales.** Cada caso de uso declara sus `rnf` propios con la numeración `rnf <número de CU>.<correlativo>`. En la descripción de cada uno se indica **de qué requisito no funcional global deriva** (`RNF01` a `RNF42`). El `rnf` local es el detalle concreto de esa pantalla u operación; el global es la regla que se cumple en todo el sistema.
 
**4. Cursos alternativos.** Se numeran `ca <número de CU>.<correlativo>`, y sus pasos `<número de CU>.<correlativo>.<paso>`.
 
**5. Postcondición.** La plantilla no tiene ese campo. El estado final del sistema se expresa como último paso del curso normal, antes de FIN CASO DE USO.
 
**6. rnf transversales.** Algunos requerimientos no funcionales aplican al caso de uso completo y no a un paso en particular. Esos se declaran en la tabla y no se referencian desde el flujo de sucesos. Un `rnf` sin referencia en el curso normal no es una omisión: es un requisito de alcance transversal.
 
**7. Requerimientos no funcionales de sistema.** Doce requisitos no funcionales globales no derivan en ningún `rnf` local, y no deben hacerlo: no dependen de ningún caso de uso en particular porque rigen sobre el sistema completo.
 
| RNF global | Categoría | Por qué no deriva en un rnf local |
|---|---|---|
| RNF18 | Usabilidad | Define el medio de acceso al sistema (navegador de escritorio) y excluye el diseño adaptable a móvil. Aplica a todas las pantallas por igual. |
| RNF25 | Mantenibilidad | Separación en capas de presentación, lógica y persistencia. Es una propiedad de la arquitectura, no de una operación. |
| RNF27 | Mantenibilidad | Versionado del código en Git. Corresponde a la gestión de configuración del proyecto. |
| RNF29 | Restricción técnica | Tipo de almacenamiento (base de datos relacional). |
| RNF30 | Restricción técnica | Lenguaje y framework del backend. |
| RNF31 | Restricción técnica | Tecnología del frontend. |
| RNF32 | Restricción técnica | El envío de correo se delega en un servidor SMTP externo; el sistema no implementa entrega propia. |
| RNF33 | Restricción técnica | Mecanismo de ejecución periódica (planificador de tareas). |
| RNF34 | Restricción técnica | Sistema operativo de despliegue. |
| RNF40 | Restricción técnica | Todo acceso a la base se encapsula en un módulo de acceso a datos con SQL parametrizado. Es una regla sobre la estructura del código, no sobre una operación: ningún paso de ningún caso de uso puede referenciarla porque todos la cumplen por igual. |
| RNF41 | Restricción técnica | La gestión de sesiones y el cifrado de claves se resuelven con los mecanismos de Flask, sin dependencias adicionales de autenticación. Define con qué herramienta se construye, no qué debe ocurrir: el comportamiento esperado ya está en RNF08 y RNF09, que sí derivan en `rnf` locales en CU0001, CU0002 y CU0003. |
| RNF42 | Restricción técnica | Ambiente de ejecución para la demostración (servidor de desarrollo de Flask en entorno local). Corresponde al ambiente declarado en el plan de pruebas. |
 
Estos doce se verifican por inspección de la arquitectura, del repositorio y del entorno de despliegue, no mediante casos de prueba de casos de uso. Su trazabilidad corresponde al documento de arquitectura y al plan de pruebas, no a este documento.
 
En todos los casos de uso: **Elaboró** Abel · **Fecha** 13/09/2026 · **Aprobó** y **Revisó** pendientes de la cátedra · **Versión** 1.0.
 
---
---
 
# PAQUETE: GESTIÓN DE USUARIOS
 
---
 
## CU0001 — Registrar Usuario
 
### Resumen ejecutivo
 
| Campo | Contenido |
|---|---|
| Código | CU0001 |
| Paquete | Gestión de Usuarios |
| Nombre | Registrar Usuario |
| Versión | 1.0 |
| Prioridad | 10 |
| Confeccionó | Abel |
| Relevó | Abel |
| Revisó | — |
| Descripción | Permite que una persona de la empresa que todavía no tiene cuenta cree la suya en el sistema. |
| Actores | **Visitante**: persona de la empresa que no tiene cuenta o no ha iniciado sesión. |
| Frecuencia | Alta durante la puesta en marcha del sistema; baja y esporádica una vez estabilizada la base de usuarios. |
| Comentarios | Es el caso de uso que crea la entidad central del sistema. Ningún otro caso de uso puede ejecutarse sin que este se haya completado al menos una vez. |
| Observaciones | Ver {Ob 1.1} |
 
### Curso normal
 
| Precondición |
|---|
| Ninguna. |
 
| N° | Paso (Flujo de Sucesos) |
|---|---|
| 1 | El Visitante selecciona la opción "Registrarse". |
| 2 | El sistema muestra el formulario de registro. {rnf 1.1} |
| 3 | El Visitante completa los datos solicitados y selecciona "Registrarse". {ca 1.1} {ca 1.2} {ca 1.3} {ca 1.4} |
| 4 | El sistema valida que todos los campos obligatorios estén completos y con el formato correcto. |
| 5 | El sistema verifica que el nombre de usuario y la dirección de correo no estén en uso. |
| 6 | El sistema almacena la foto de perfil y cifra la clave. {rnf 1.2} |
| 7 | El sistema crea la cuenta con rol Empleado, la deja en estado activo y registra su fecha de alta. {rnf 1.3} |
| 8 | El sistema informa que el registro se completó y ofrece iniciar sesión. |
| 9 | FIN CASO DE USO |
 
### Cursos alternativos
 
**ca 1.1 — Datos obligatorios incompletos o con formato inválido**
 
| N° | Paso |
|---|---|
| 1.1.1 | El sistema detecta campos vacíos, un nombre de usuario de más de 15 caracteres o que no respeta la forma admitida (`rnf 1.1`, {Ob 1.3}), o una dirección de correo mal formada. |
| 1.1.2 | El sistema muestra el formulario indicando, campo por campo, cuál es el problema, y conserva los datos ya ingresados salvo la clave. |
| 1.1.3 | El caso de uso continúa en el paso 3 del curso normal. |
 
**ca 1.2 — Nombre de usuario o correo ya existente**
 
| N° | Paso |
|---|---|
| 1.2.1 | El sistema detecta que el nombre de usuario o el correo ya pertenecen a otra cuenta. |
| 1.2.2 | El sistema informa cuál de los dos está en uso y solicita otro valor. |
| 1.2.3 | El caso de uso continúa en el paso 3 del curso normal. |
 
**ca 1.3 — Foto de perfil inválida**
 
| N° | Paso |
|---|---|
| 1.3.1 | El sistema detecta que el archivo no es una imagen de formato admitido o supera el tamaño máximo. |
| 1.3.2 | El sistema informa el formato y el tamaño admitidos, y descarta el archivo. |
| 1.3.3 | El caso de uso continúa en el paso 3 del curso normal. |
 
**ca 1.4 — El Visitante cancela el registro**
 
| N° | Paso |
|---|---|
| 1.4.1 | El Visitante selecciona "Cancelar". |
| 1.4.2 | El sistema descarta los datos ingresados y vuelve a la pantalla inicial. |
| 1.4.3 | FIN CASO DE USO |
 
### Requerimientos no funcionales
 
| Cod | Nombre | Descripción |
|---|---|---|
| rnf 1.1 | Formulario de registro | Campos solicitados: nombre de usuario (obligatorio, máximo 15 caracteres, único, solo letras, números y guion bajo, con puntos o guiones únicamente en el medio), correo electrónico (obligatorio, formato válido, único), clave (obligatoria, mínimo 8 caracteres), confirmación de clave (obligatoria, debe coincidir), nombre completo (obligatorio), descripción breve (opcional), foto de perfil (opcional). Deriva de RNF02, RNF03 y RNF04. |
| rnf 1.2 | Almacenamiento de la clave | La clave se guarda mediante función de hash con salt. En ningún momento se almacena ni se registra en texto plano. Deriva de RNF08. |
| rnf 1.3 | Atomicidad del alta | La creación de la cuenta y el almacenamiento de la foto conforman una única transacción: si alguna de las dos falla, no queda registro parcial del usuario. Deriva de RNF23. |
 
### Observaciones
 
| Cod | Descripción |
|---|---|
| {Ob 1.1} | El enunciado no define reglas de complejidad para la clave. Se adopta una longitud mínima de 8 caracteres como criterio propio, documentado en el `rnf 1.1` de este caso de uso. RNF08 no fija longitudes: regula cómo se **almacena** la clave, no cómo se elige. |
| {Ob 1.2} | El sistema no envía correo de confirmación de cuenta: el enunciado no lo pide y no forma parte del alcance. |
| {Ob 1.3} | El enunciado solo fija que el nombre de usuario tenga **no más de 15 caracteres** (RNF02); no dice qué caracteres admite. Se adopta como criterio propio que sean letras (con tilde o `ñ`), números y guion bajo, y que el punto y el guion se admitan **solo en el medio** (`juan.perez`, `ana-lopez`; no `.juan`, `juan.`, `a..b` ni `ana lopez`). El motivo es que el texto de un mensaje reconoce las menciones con `@` (CU0004) con exactamente esa forma: sin esta regla se podría registrar un nombre que después nadie puede mencionar. La regla solo se aplica al **registrarse**: el inicio de sesión (CU0002) no la revisa, para que una cuenta ya existente pueda entrar siempre. No cambia el máximo de 15 caracteres ni el RNF02. |
 
### Documentación anexa
 
| Nombre | Tipo | Nombre/Lugar |
|---|---|---|
| Prototipo de la pantalla de registro | Diseño de interfaz | `Prototipo de Interfaces` (carpeta `1. Requerimientos`), pantalla 2, «Registro» |
 
---
 
## CU0002 — Iniciar Sesión
 
### Resumen ejecutivo
 
| Campo | Contenido |
|---|---|
| Código | CU0002 |
| Paquete | Gestión de Usuarios |
| Nombre | Iniciar Sesión |
| Versión | 1.0 |
| Prioridad | 10 |
| Confeccionó | Abel |
| Relevó | Abel |
| Revisó | — |
| Descripción | Permite que un usuario registrado se autentique y abra una sesión de trabajo en el sistema. |
| Actores | **Visitante**: persona de la empresa que tiene cuenta pero no ha iniciado sesión. |
| Frecuencia | Muy alta. Varias veces por día por usuario. |
| Comentarios | Este caso de uso no está en el enunciado. Proviene de la característica C17, aprobada como supuesto propio. |
| Observaciones | Ver {Ob 2.1} |
 
### Curso normal
 
| Precondición |
|---|
| El usuario debe tener una cuenta creada mediante CU0001. |
 
| N° | Paso (Flujo de Sucesos) |
|---|---|
| 1 | El Visitante selecciona la opción "Iniciar sesión". |
| 2 | El sistema muestra el formulario de autenticación. {rnf 2.1} |
| 3 | El Visitante ingresa su nombre de usuario y su clave, y confirma. {ca 2.1} {ca 2.2} |
| 4 | El sistema verifica que exista una cuenta activa con ese nombre de usuario y que la clave coincida. {rnf 2.2} |
| 5 | El sistema abre la sesión, registra al Visitante como Usuario autenticado y lo redirige a su tablón (CU0009). |
| 6 | FIN CASO DE USO |
 
### Cursos alternativos
 
**ca 2.1 — Credenciales inválidas**
 
| N° | Paso |
|---|---|
| 2.1.1 | El nombre de usuario no existe, la clave no coincide o la cuenta no está activa. |
| 2.1.2 | El sistema informa que las credenciales son incorrectas, sin precisar cuál de los dos datos falló. {rnf 2.3} |
| 2.1.3 | El caso de uso continúa en el paso 3 del curso normal. |
 
**ca 2.2 — Campos vacíos**
 
| N° | Paso |
|---|---|
| 2.2.1 | El Visitante confirma sin completar alguno de los dos campos. |
| 2.2.2 | El sistema indica qué campo falta completar. |
| 2.2.3 | El caso de uso continúa en el paso 3 del curso normal. |
 
### Requerimientos no funcionales
 
| Cod | Nombre | Descripción |
|---|---|---|
| rnf 2.1 | Formulario de autenticación | Campos solicitados: nombre de usuario y clave, ambos obligatorios. La clave se ingresa enmascarada. |
| rnf 2.2 | Verificación de la clave | La comparación se realiza contra el hash almacenado. La clave en texto plano no se guarda ni se registra en ningún log. Deriva de RNF08. |
| rnf 2.3 | Mensaje de error genérico | El mensaje de credenciales inválidas no revela si el error estuvo en el usuario o en la clave, para no permitir descubrir qué nombres de usuario existen. Es una excepción deliberada a RNF16, que exige mensajes de error descriptivos; aplica únicamente a la autenticación. |
 
### Observaciones
 
| Cod | Descripción |
|---|---|
| {Ob 2.1} | El bloqueo de la cuenta tras varios intentos fallidos no forma parte del alcance: no está en el enunciado y no se va a implementar ni probar. |
| {Ob 2.2} | La recuperación de clave olvidada corresponde a la característica C26, registrada y no aprobada para esta versión. |
 
### Documentación anexa
 
| Nombre | Tipo | Nombre/Lugar |
|---|---|---|
| Prototipo de la pantalla de inicio de sesión | Diseño de interfaz | `Prototipo de Interfaces` (carpeta `1. Requerimientos`), pantalla 1, «Iniciar sesión» |
 
---
 
## CU0003 — Cerrar Sesión
 
### Resumen ejecutivo
 
| Campo | Contenido |
|---|---|
| Código | CU0003 |
| Paquete | Gestión de Usuarios |
| Nombre | Cerrar Sesión |
| Versión | 1.0 |
| Prioridad | 3 |
| Confeccionó | Abel |
| Relevó | Abel |
| Revisó | — |
| Descripción | Permite que un usuario autenticado finalice su sesión de trabajo. |
| Actores | **Usuario**: empleado registrado con sesión activa. |
| Frecuencia | Alta. Una vez por sesión de trabajo. |
| Comentarios | Complementa a CU0002. Proviene de la característica C17. |
| Observaciones | — |
 
### Curso normal
 
| Precondición |
|---|
| El Usuario debe tener una sesión activa. |
 
| N° | Paso (Flujo de Sucesos) |
|---|---|
| 1 | El Usuario selecciona la opción "Cerrar sesión". |
| 2 | El sistema invalida la sesión activa. {rnf 3.1} {ca 3.1} |
| 3 | El sistema redirige a la pantalla inicial y el Usuario pasa a ser Visitante. |
| 4 | FIN CASO DE USO |
 
### Cursos alternativos
 
**ca 3.1 — La sesión ya había expirado**
 
| N° | Paso |
|---|---|
| 3.1.1 | El sistema detecta que la sesión no está vigente. |
| 3.1.2 | El sistema redirige a la pantalla inicial sin informar error. |
| 3.1.3 | FIN CASO DE USO |
 
### Requerimientos no funcionales
 
| Cod | Nombre | Descripción |
|---|---|---|
| rnf 3.1 | Invalidación completa | Al cerrar la sesión, el identificador de sesión deja de ser válido del lado del servidor. No alcanza con borrarlo del navegador. Deriva de RNF09. |
 
### Observaciones
 
| Cod | Descripción |
|---|---|
| {Ob 3.1} | El cierre automático de sesión por inactividad se considera una configuración de infraestructura, no un caso de uso. Queda cubierto por RNF09. |
 
### Documentación anexa
 
| Nombre | Tipo | Nombre/Lugar |
|---|---|---|
| — | — | — |
 
---
---
 
# PAQUETE: GESTIÓN DE MENSAJES
 
---
 
## CU0004 — Publicar Mensaje
 
### Resumen ejecutivo
 
| Campo | Contenido |
|---|---|
| Código | CU0004 |
| Paquete | Gestión de Mensajes |
| Nombre | Publicar Mensaje |
| Versión | 1.0 |
| Prioridad | 10 |
| Confeccionó | Abel |
| Relevó | Abel |
| Revisó | — |
| Descripción | Permite que un usuario publique un mensaje de hasta 140 caracteres, visible en su muro y en el tablón de sus seguidores. |
| Actores | **Usuario**: empleado registrado con sesión activa. |
| Frecuencia | Muy alta. Es la operación principal del sistema. |
| Comentarios | Es el caso de uso central del dominio. Cubre R01, R05 y R06. |
| Observaciones | Ver {Ob 4.1} |
 
### Curso normal
 
| Precondición |
|---|
| El Usuario debe tener una sesión activa (CU0002). |
 
| N° | Paso (Flujo de Sucesos) |
|---|---|
| 1 | El Usuario selecciona la opción de publicar un mensaje. |
| 2 | El sistema muestra el campo de redacción con el contador de caracteres restantes. {rnf 4.1} |
| 3 | El Usuario escribe el texto del mensaje y selecciona "Publicar". {ca 4.1} {ca 4.2} {ca 4.3} |
| 4 | El sistema valida que el texto no esté vacío y no supere los 140 caracteres. {rnf 4.2} |
| 5 | El sistema analiza el texto y extrae las etiquetas que comienzan con `#`, las menciones que comienzan con `@` y los links. {rnf 4.3} |
| 6 | El sistema registra las etiquetas que todavía no existen en el sistema. |
| 7 | El sistema descarta las menciones que no corresponden a un nombre de usuario existente. |
| 8 | El sistema almacena el mensaje con su autor, su fecha de publicación, su origen web y los elementos extraídos. {rnf 4.4} {rnf 4.5} |
| 9 | El sistema muestra el mensaje publicado en el tablón del Usuario. A partir de ese momento el mensaje queda disponible en su muro y en el tablón de sus seguidores. |
| 10 | FIN CASO DE USO |
 
### Cursos alternativos
 
**ca 4.1 — Mensaje vacío**
 
| N° | Paso |
|---|---|
| 4.1.1 | El Usuario confirma sin haber escrito texto, o habiendo escrito solo espacios. |
| 4.1.2 | El sistema informa que el mensaje no puede estar vacío y no publica nada. |
| 4.1.3 | El caso de uso continúa en el paso 3 del curso normal. |
 
**ca 4.2 — Texto que supera los 140 caracteres**
 
| N° | Paso |
|---|---|
| 4.2.1 | El texto recibido supera los 140 caracteres. |
| 4.2.2 | El sistema rechaza la publicación e informa el límite y la cantidad de caracteres excedentes. El texto no se recorta automáticamente. |
| 4.2.3 | El caso de uso continúa en el paso 3 del curso normal. |
 
**ca 4.3 — La sesión expiró durante la redacción**
 
| N° | Paso |
|---|---|
| 4.3.1 | El sistema detecta que la sesión ya no está vigente al recibir la publicación. |
| 4.3.2 | El sistema conserva el texto redactado y solicita al Usuario que vuelva a iniciar sesión (CU0002). |
| 4.3.3 | El caso de uso continúa en el paso 3 del curso normal. |
 
### Requerimientos no funcionales
 
| Cod | Nombre | Descripción |
|---|---|---|
| rnf 4.1 | Contador de caracteres | El campo de redacción muestra permanentemente cuántos caracteres quedan disponibles y bloquea la escritura al alcanzar los 140. Deriva de RNF15. |
| rnf 4.2 | Validación en el servidor | El límite de 140 caracteres se valida del lado del servidor, no solo en la interfaz, porque el mismo límite rige para las publicaciones que llegan por la API (CU0020). Deriva de RNF01. |
| rnf 4.3 | Componente único de extracción | El análisis del texto para extraer etiquetas, menciones y links se resuelve con un único componente, reutilizado por la aplicación web y por la API. Deriva de RNF26. |
| rnf 4.4 | Atomicidad de la publicación | El mensaje, sus etiquetas, sus menciones y sus links se registran en una única transacción. Deriva de RNF23. |
| rnf 4.5 | Datos obligatorios del mensaje | Todo mensaje se almacena con su autor y su fecha de publicación, sin excepción y cualquiera sea su origen. Deriva de RNF05. |
 
### Observaciones
 
| Cod | Descripción |
|---|---|
| {Ob 4.1} | Este caso de uso realiza las reglas automáticas RA01 y RA02 del documento de requisitos funcionales. |
| {Ob 4.2} | Las menciones no generan ninguna notificación. Esa característica es C27, registrada y no aprobada para esta versión. |
| {Ob 4.3} | El enunciado no impone un máximo de etiquetas por mensaje. El límite efectivo es el de 140 caracteres. |
 
### Documentación anexa
 
| Nombre | Tipo | Nombre/Lugar |
|---|---|---|
| Prototipo del campo de publicación | Diseño de interfaz | `Prototipo de Interfaces` (carpeta `1. Requerimientos`), pantalla 3, «Tablón» |
 
---
 
## CU0005 — Editar Mensaje Propio
 
### Resumen ejecutivo
 
| Campo | Contenido |
|---|---|
| Código | CU0005 |
| Paquete | Gestión de Mensajes |
| Nombre | Editar Mensaje Propio |
| Versión | 1.0 |
| Prioridad | 7 |
| Confeccionó | Abel |
| Relevó | Abel |
| Revisó | — |
| Descripción | Permite que un usuario modifique el texto de un mensaje que él mismo publicó. |
| Actores | **Usuario**: empleado registrado con sesión activa, autor del mensaje. |
| Frecuencia | Media. Habitualmente para corregir errores poco después de publicar. |
| Comentarios | Es el caso de uso donde se materializa la decisión de que la republicación referencia al mensaje original (característica C23). |
| Observaciones | Ver {Ob 5.1} |
 
### Curso normal
 
| Precondición |
|---|
| El Usuario debe tener sesión activa y ser el autor del mensaje a editar. |
 
| N° | Paso (Flujo de Sucesos) |
|---|---|
| 1 | El Usuario selecciona la opción de editar sobre uno de sus mensajes. {ca 5.1} |
| 2 | El sistema verifica que el Usuario sea el autor del mensaje. {rnf 5.1} {ca 5.2} |
| 3 | El sistema muestra el texto actual en el campo de redacción, con el contador de caracteres. |
| 4 | El Usuario modifica el texto y confirma. {ca 5.3} {ca 5.4} |
| 5 | El sistema valida que el texto no esté vacío y no supere los 140 caracteres. |
| 6 | El sistema vuelve a analizar el texto y recalcula las etiquetas, menciones y links del mensaje, descartando los que ya no están y registrando los nuevos. |
| 7 | El sistema guarda el nuevo texto, registra la fecha de edición y marca el mensaje como editado. |
| 8 | El sistema muestra el mensaje actualizado. Todas las republicaciones existentes de ese mensaje pasan a mostrar el texto nuevo, por ser referencias al original. |
| 9 | FIN CASO DE USO |
 
### Cursos alternativos
 
**ca 5.1 — El mensaje ya no existe**
 
| N° | Paso |
|---|---|
| 5.1.1 | El mensaje fue borrado mientras el Usuario tenía la pantalla abierta. |
| 5.1.2 | El sistema informa que el mensaje ya no está disponible y actualiza la vista. |
| 5.1.3 | FIN CASO DE USO |
 
**ca 5.2 — El Usuario no es el autor**
 
| N° | Paso |
|---|---|
| 5.2.1 | El sistema determina que el mensaje pertenece a otro usuario. |
| 5.2.2 | El sistema rechaza la operación e informa que solo el autor puede editar un mensaje. |
| 5.2.3 | FIN CASO DE USO |
 
**ca 5.3 — Texto inválido**
 
| N° | Paso |
|---|---|
| 5.3.1 | El texto queda vacío o supera los 140 caracteres. |
| 5.3.2 | El sistema informa el problema y conserva el texto original sin modificar. |
| 5.3.3 | El caso de uso continúa en el paso 4 del curso normal. |
 
**ca 5.4 — El Usuario cancela la edición**
 
| N° | Paso |
|---|---|
| 5.4.1 | El Usuario selecciona "Cancelar". |
| 5.4.2 | El sistema descarta los cambios y mantiene el mensaje como estaba. |
| 5.4.3 | FIN CASO DE USO |
 
### Requerimientos no funcionales
 
| Cod | Nombre | Descripción |
|---|---|---|
| rnf 5.1 | Verificación de autoría en el servidor | La comprobación de que el Usuario es el autor se realiza del lado del servidor en cada solicitud. Ocultar el botón de editar en la interfaz no se considera control suficiente. Deriva de RNF10. |
| rnf 5.2 | Indicación de edición | Todo mensaje editado se muestra con una marca visible de "editado" y la fecha de la última modificación, tanto en el muro como en el tablón. Deriva de RNF14. |
 
### Observaciones
 
| Cod | Descripción |
|---|---|
| {Ob 5.1} | Este caso de uso realiza las reglas automáticas RA01, RA02 y RA05. |
| {Ob 5.2} | El sistema no conserva el historial de versiones anteriores del texto. El enunciado no lo pide. |
 
### Documentación anexa
 
| Nombre | Tipo | Nombre/Lugar |
|---|---|---|
| — | — | — |
 
---
 
## CU0006 — Borrar Mensaje Propio
 
### Resumen ejecutivo
 
| Campo | Contenido |
|---|---|
| Código | CU0006 |
| Paquete | Gestión de Mensajes |
| Nombre | Borrar Mensaje Propio |
| Versión | 1.0 |
| Prioridad | 7 |
| Confeccionó | Abel |
| Relevó | Abel |
| Revisó | — |
| Descripción | Permite que un usuario elimine definitivamente un mensaje que él mismo publicó. |
| Actores | **Usuario**: empleado registrado con sesión activa, autor del mensaje. |
| Frecuencia | Baja. |
| Comentarios | La eliminación arrastra las republicaciones del mensaje, por ser referencias al original. |
| Observaciones | Ver {Ob 6.1} |
 
### Curso normal
 
| Precondición |
|---|
| El Usuario debe tener sesión activa y ser el autor del mensaje a borrar. |
 
| N° | Paso (Flujo de Sucesos) |
|---|---|
| 1 | El Usuario selecciona la opción de borrar sobre uno de sus mensajes. {ca 6.1} |
| 2 | El sistema verifica que el Usuario sea el autor del mensaje. {rnf 6.1} {ca 6.2} |
| 3 | El sistema solicita confirmación e informa que la acción no puede deshacerse y que el mensaje desaparecerá también de los tablones donde fue republicado. {rnf 6.2} |
| 4 | El Usuario confirma. {ca 6.3} |
| 5 | El sistema elimina todas las republicaciones del mensaje. |
| 6 | El sistema elimina el mensaje junto con sus menciones y sus links, y libera sus etiquetas. {rnf 6.3} |
| 7 | El sistema actualiza la vista. El mensaje deja de figurar en el muro del autor, en los tablones, en las búsquedas por etiqueta y en el conteo de los temas del momento. |
| 8 | FIN CASO DE USO |
 
### Cursos alternativos
 
**ca 6.1 — El mensaje ya no existe**
 
| N° | Paso |
|---|---|
| 6.1.1 | El mensaje fue eliminado previamente. |
| 6.1.2 | El sistema actualiza la vista sin informar error. |
| 6.1.3 | FIN CASO DE USO |
 
**ca 6.2 — El Usuario no es el autor**
 
| N° | Paso |
|---|---|
| 6.2.1 | El sistema determina que el mensaje pertenece a otro usuario. |
| 6.2.2 | El sistema rechaza la operación e informa que solo el autor puede borrar un mensaje. |
| 6.2.3 | FIN CASO DE USO |
 
**ca 6.3 — El Usuario cancela la confirmación**
 
| N° | Paso |
|---|---|
| 6.3.1 | El Usuario rechaza la confirmación. |
| 6.3.2 | El sistema mantiene el mensaje sin cambios. |
| 6.3.3 | FIN CASO DE USO |
 
### Requerimientos no funcionales
 
| Cod | Nombre | Descripción |
|---|---|---|
| rnf 6.1 | Verificación de autoría en el servidor | Igual que en CU0005: la autoría se verifica del lado del servidor. Deriva de RNF10. |
| rnf 6.2 | Confirmación explícita | Toda operación irreversible exige confirmación explícita del Usuario, con un mensaje que describe las consecuencias. Deriva de RNF16. |
| rnf 6.3 | Atomicidad del borrado | La eliminación del mensaje y de sus republicaciones conforma una única transacción: no puede quedar una republicación apuntando a un mensaje inexistente. Deriva de RNF23. |
 
### Observaciones
 
| Cod | Descripción |
|---|---|
| {Ob 6.1} | Este caso de uso realiza la regla automática RA06. |
| {Ob 6.2} | El borrado es físico, no lógico. El enunciado no pide papelera ni recuperación. Una etiqueta que queda sin mensajes asociados permanece registrada, pero deja de aparecer en los temas del momento por no tener apariciones en la ventana de `n` días. |
 
### Documentación anexa
 
| Nombre | Tipo | Nombre/Lugar |
|---|---|---|
| — | — | — |
 
---
 
## CU0007 — Republicar Mensaje
 
### Resumen ejecutivo
 
| Campo | Contenido |
|---|---|
| Código | CU0007 |
| Paquete | Gestión de Mensajes |
| Nombre | Republicar Mensaje |
| Versión | 1.0 |
| Prioridad | 7 |
| Confeccionó | Abel |
| Relevó | Abel |
| Revisó | — |
| Descripción | Permite que un usuario reenvíe a sus propios seguidores un mensaje de su tablón creado por alguien a quien sigue. |
| Actores | **Usuario**: empleado registrado con sesión activa. |
| Frecuencia | Media. |
| Comentarios | La republicación no copia el texto: crea una referencia al mensaje original (característica C23). |
| Observaciones | Ver {Ob 7.1} |
 
### Curso normal
 
| Precondición |
|---|
| El Usuario debe tener sesión activa y el mensaje debe estar en su tablón. |
 
| N° | Paso (Flujo de Sucesos) |
|---|---|
| 1 | El Usuario selecciona la opción de republicar sobre un mensaje de su tablón. {ca 7.4} |
| 2 | El sistema verifica que el mensaje sea público y que su autor sea un usuario al que el Usuario sigue. {ca 7.1} {ca 7.2} |
| 3 | El sistema verifica que el Usuario no haya republicado ya ese mensaje. {ca 7.3} |
| 4 | El sistema registra la republicación con el Usuario que la realiza, la fecha y la referencia al mensaje original. |
| 5 | El sistema muestra el mensaje republicado en el tablón del Usuario, indicando quién es el autor original. A partir de ese momento la republicación aparece en el tablón de los seguidores del Usuario. {rnf 7.1} |
| 6 | FIN CASO DE USO |
 
### Cursos alternativos
 
**ca 7.1 — El autor del mensaje no es seguido por el Usuario**
 
| N° | Paso |
|---|---|
| 7.1.1 | El Usuario intenta republicar un mensaje cuyo autor no sigue. Ocurre, por ejemplo, cuando el mensaje llegó a su tablón como republicación de un usuario al que sí sigue. |
| 7.1.2 | El sistema rechaza la operación e informa que solo pueden republicarse mensajes de usuarios a los que se sigue. |
| 7.1.3 | FIN CASO DE USO |
 
**ca 7.2 — El mensaje es propio**
 
| N° | Paso |
|---|---|
| 7.2.1 | El Usuario intenta republicar un mensaje del que es autor. |
| 7.2.2 | El sistema rechaza la operación: el mensaje ya está en su muro y en el tablón de sus seguidores. |
| 7.2.3 | FIN CASO DE USO |
 
**ca 7.3 — El mensaje ya fue republicado por el Usuario**
 
| N° | Paso |
|---|---|
| 7.3.1 | Ya existe una republicación de ese mensaje realizada por el Usuario. |
| 7.3.2 | El sistema informa que el Usuario ya republicó ese mensaje y no registra una segunda republicación. |
| 7.3.3 | FIN CASO DE USO |
 
**ca 7.4 — El mensaje ya no existe**
 
| N° | Paso |
|---|---|
| 7.4.1 | El mensaje fue borrado mientras el Usuario tenía la pantalla abierta. |
| 7.4.2 | El sistema informa que el mensaje ya no está disponible y actualiza la vista. |
| 7.4.3 | FIN CASO DE USO |
 
### Requerimientos no funcionales
 
| Cod | Nombre | Descripción |
|---|---|---|
| rnf 7.1 | Identificación del autor original | En toda republicación se muestra de forma visible el autor original del mensaje y el usuario que lo republicó. El texto mostrado es siempre el vigente del mensaje original. Deriva de RNF14. |
| rnf 7.2 | Exclusión del conteo de etiquetas | Una republicación no incrementa el conteo de las etiquetas del mensaje original en el cálculo de los temas del momento. La etiqueta se cuenta una sola vez, en el mensaje original. Deriva de RNF01 y de la regla RA03. |
 
### Observaciones
 
| Cod | Descripción |
|---|---|
| {Ob 7.1} | Este caso de uso realiza la regla automática RA09. |
| {Ob 7.2} | Los mensajes privados no pueden republicarse: no aparecen en ningún tablón, por lo que la operación no es alcanzable. |
| {Ob 7.3} | El curso alternativo **ca 7.1** **es alcanzable desde la interfaz** en esta versión. Si el Usuario sigue a B y no sigue a C, y B (que sí sigue a C) republica un mensaje de C, esa republicación aparece en el tablón del Usuario (CU0009 paso 3) con la opción de republicar; lo que se republicaría es el mensaje de C. La opción se muestra en todo elemento cuyo autor original no sea el Usuario, y la verificación la hace el servidor en el paso 2. El plan de pruebas lo ejercita por interfaz con ese escenario. *Corrige la versión 1.1, que lo declaraba no alcanzable; detectado en el flujo de Diseño (`DISEÑO_MiBlog.md` §1, H5).* |
| {Ob 7.4} | No existe la operación de deshacer una republicación: no está entre los 21 casos de uso especificados. Por eso el `ca 7.3` se limita a informar. *La versión 1.1 ofrecía deshacerla; corregido en el flujo de Diseño (H3).* |
| {Ob 7.5} | El `ca 7.4` es el mismo caso que `ca 5.1` y `ca 6.1`: el mensaje se borra entre que se muestra la pantalla y se elige la opción. *Agregado en el flujo de Diseño (H6).* |
 
### Documentación anexa
 
| Nombre | Tipo | Nombre/Lugar |
|---|---|---|
| — | — | — |
 
---
 
## CU0008 — Enviar Mensaje Privado
 
### Resumen ejecutivo
 
| Campo | Contenido |
|---|---|
| Código | CU0008 |
| Paquete | Gestión de Mensajes |
| Nombre | Enviar Mensaje Privado |
| Versión | 1.0 |
| Prioridad | 6 |
| Confeccionó | Abel |
| Relevó | Abel |
| Revisó | — |
| Descripción | Permite que un usuario publique un mensaje de hasta 140 caracteres dirigido a un único destinatario. |
| Actores | **Usuario**: empleado registrado con sesión activa. |
| Frecuencia | Media. |
| Comentarios | Es el único canal restringido del sistema. Todos los demás mensajes son públicos dentro de la empresa (característica C19). |
| Observaciones | Ver {Ob 8.1} |
 
### Curso normal
 
| Precondición |
|---|
| El Usuario debe tener una sesión activa. |
 
| N° | Paso (Flujo de Sucesos) |
|---|---|
| 1 | El Usuario selecciona la opción de enviar un mensaje privado. |
| 2 | El sistema muestra el campo de redacción con el contador de caracteres y el campo de destinatario. {rnf 8.1} |
| 3 | El Usuario indica el destinatario, escribe el texto y confirma. {ca 8.1} {ca 8.2} {ca 8.3} |
| 4 | El sistema verifica que el destinatario exista, esté activo y no sea el propio Usuario. |
| 5 | El sistema valida que el texto no esté vacío y no supere los 140 caracteres. |
| 6 | El sistema almacena el mensaje como privado, con su autor, su destinatario y su fecha. |
| 7 | El sistema informa que el mensaje fue enviado. El mensaje queda accesible únicamente para el autor y el destinatario. {rnf 8.2} |
| 8 | FIN CASO DE USO |
 
### Cursos alternativos
 
**ca 8.1 — El destinatario no existe o no está activo**
 
| N° | Paso |
|---|---|
| 8.1.1 | El nombre de usuario indicado no corresponde a ninguna cuenta activa. |
| 8.1.2 | El sistema informa que el destinatario no existe y no envía el mensaje. |
| 8.1.3 | El caso de uso continúa en el paso 3 del curso normal. |
 
**ca 8.2 — El destinatario es el propio Usuario**
 
| N° | Paso |
|---|---|
| 8.2.1 | El Usuario se indica a sí mismo como destinatario. |
| 8.2.2 | El sistema rechaza la operación e informa que no puede enviarse un mensaje privado a uno mismo. |
| 8.2.3 | El caso de uso continúa en el paso 3 del curso normal. |
 
**ca 8.3 — Texto inválido**
 
| N° | Paso |
|---|---|
| 8.3.1 | El texto está vacío o supera los 140 caracteres. |
| 8.3.2 | El sistema informa el problema y no envía el mensaje. |
| 8.3.3 | El caso de uso continúa en el paso 3 del curso normal. |
 
### Requerimientos no funcionales
 
| Cod | Nombre | Descripción |
|---|---|---|
| rnf 8.1 | Formulario de mensaje privado | Campos solicitados: destinatario (obligatorio, un único usuario) y texto (obligatorio, máximo 140 caracteres). Deriva de RNF01. |
| rnf 8.2 | Confidencialidad del mensaje | Un mensaje privado solo es accesible para su autor y su destinatario. No aparece en muros, tablones, búsquedas por etiqueta, temas del momento ni respuestas de la API. Deriva de RNF11. |
 
### Observaciones
 
| Cod | Descripción |
|---|---|
| {Ob 8.1} | Este caso de uso realiza la regla automática RA04. |
| {Ob 8.2} | Un mensaje privado admite un único destinatario. El enunciado dice expresamente "a un único usuario". |
| {Ob 8.3} | Las etiquetas y menciones dentro de un mensaje privado se registran, pero no se cuentan para los temas del momento ni aparecen en las búsquedas por etiqueta. |
 
### Documentación anexa
 
| Nombre | Tipo | Nombre/Lugar |
|---|---|---|
| — | — | — |
 
---
 
## CU0009 — Visualizar Tablón
 
### Resumen ejecutivo
 
| Campo | Contenido |
|---|---|
| Código | CU0009 |
| Paquete | Gestión de Mensajes |
| Nombre | Visualizar Tablón |
| Versión | 1.0 |
| Prioridad | 10 |
| Confeccionó | Abel |
| Relevó | Abel |
| Revisó | — |
| Descripción | Muestra al usuario el listado cronológico de los mensajes de los usuarios a los que sigue, de los propios y de las republicaciones de ambos. |
| Actores | **Usuario**: empleado registrado con sesión activa. |
| Frecuencia | Muy alta. Es la pantalla principal del sistema. |
| Comentarios | Es la consulta más costosa del sistema y la que define el rendimiento percibido. |
| Observaciones | Ver {Ob 9.1} |
 
### Curso normal
 
| Precondición |
|---|
| El Usuario debe tener una sesión activa. |
 
| N° | Paso (Flujo de Sucesos) |
|---|---|
| 1 | El Usuario accede a su página principal, sea al iniciar sesión o desde el menú. |
| 2 | El sistema determina el conjunto de usuarios a los que el Usuario sigue. |
| 3 | El sistema reúne los mensajes públicos de esos usuarios, los mensajes públicos propios y las republicaciones realizadas por unos y otro. {rnf 9.1} |
| 4 | El sistema ordena el conjunto de más reciente a más antiguo, tomando la fecha de publicación del mensaje o la fecha de la republicación según corresponda. {rnf 9.2} |
| 5 | El sistema muestra el listado. De cada elemento presenta el autor, la fecha, el texto vigente y, si corresponde, la marca de editado y el usuario que republicó. {rnf 9.3} {ca 9.1} |
| 6 | El sistema muestra además el listado de seguidores y seguidos (CU0013) y los temas del momento (CU0015). **FUERA DEL ALCANCE DE REALIZACIÓN de esta versión: CU0013 y CU0015 quedan especificados y no se implementan. El tablón de esta iteración presenta únicamente el listado de elementos del paso 5.** Ver {Ob 9.4}. |
| 7 | FIN CASO DE USO |
 
### Cursos alternativos
 
**ca 9.1 — El tablón está vacío**
 
| N° | Paso |
|---|---|
| 9.1.1 | El Usuario no sigue a nadie y no ha publicado mensajes. |
| 9.1.2 | El sistema muestra un mensaje explicativo y ofrece buscar usuarios a quienes seguir (CU0014). |
| 9.1.3 | FIN CASO DE USO |
 
### Requerimientos no funcionales
 
| Cod | Nombre | Descripción |
|---|---|---|
| rnf 9.1 | Exclusión de mensajes privados | El tablón nunca incluye mensajes privados, ni propios ni ajenos. Deriva de RNF11. |
| rnf 9.2 | Orden cronológico descendente | Los elementos se presentan del más reciente al más antiguo. Deriva de RNF14. |
| rnf 9.3 | Tiempo de respuesta | Con el juego de datos de prueba definido para el proyecto, el tablón se muestra en menos de 3 segundos. Deriva de RNF19. |
 
### Observaciones
 
| Cod | Descripción |
|---|---|
| {Ob 9.1} | Este caso de uso realiza la regla automática RA07. |
| {Ob 9.2} | El tablón y el muro no son lo mismo. El tablón es lo que ve un usuario en su página principal: reúne mensajes de varios autores. El muro es el conjunto de mensajes públicos de un único usuario, y es lo que expone la API en CU0021. |
| {Ob 9.3} | La paginación del tablón no forma parte del alcance. El juego de datos de prueba está dimensionado para que el listado completo sea manejable. |
| {Ob 9.4} | El paso 6 describe el tablón completo del sistema. En la versión que se realiza, los paneles de seguidores y seguidos (CU0013) y de temas del momento (CU0015) no se construyen, porque esos dos casos de uso están fuera del alcance de realización. Detectado y registrado en el flujo de Análisis (`ANALISIS_MiBlog.md` §1.2). No hay clase de interfaz ni de control que los realice. |
 
### Documentación anexa
 
| Nombre | Tipo | Nombre/Lugar |
|---|---|---|
| Prototipo de la página principal | Diseño de interfaz | `Prototipo de Interfaces` (carpeta `1. Requerimientos`), pantalla 3, «Tablón» |
 
---
 
## CU0010 — Consultar Muro de un Usuario
 
### Resumen ejecutivo
 
| Campo | Contenido |
|---|---|
| Código | CU0010 |
| Paquete | Gestión de Mensajes |
| Nombre | Consultar Muro de un Usuario |
| Versión | 1.0 |
| Prioridad | 6 |
| Confeccionó | Abel |
| Relevó | Abel |
| Revisó | — |
| Descripción | Permite que un usuario consulte el perfil de otro: su foto, su descripción y sus mensajes públicos. |
| Actores | **Usuario**: empleado registrado con sesión activa. |
| Frecuencia | Alta. |
| Comentarios | Es el equivalente web de lo que la API expone en CU0021. Proviene de la característica C20. |
| Observaciones | Ver {Ob 10.1} |
 
### Curso normal
 
| Precondición |
|---|
| El Usuario debe tener una sesión activa. |
 
| N° | Paso (Flujo de Sucesos) |
|---|---|
| 1 | El Usuario selecciona a otro usuario desde una búsqueda, desde un mensaje de su tablón o desde su listado de seguidores y seguidos. {ca 10.1} |
| 2 | El sistema muestra la foto, el nombre completo, el nombre de usuario y la descripción del usuario consultado. |
| 3 | El sistema muestra los mensajes públicos de ese usuario y sus republicaciones, ordenados de más reciente a más antiguo. {rnf 10.1} {ca 10.2} |
| 4 | El sistema indica si el Usuario ya sigue al usuario consultado y ofrece la acción correspondiente: seguir (CU0011) o dejar de seguir (CU0012). |
| 5 | FIN CASO DE USO |
 
### Cursos alternativos
 
**ca 10.1 — El usuario consultado no existe o no está activo**
 
| N° | Paso |
|---|---|
| 10.1.1 | El nombre de usuario indicado no corresponde a ninguna cuenta activa. |
| 10.1.2 | El sistema informa que el usuario no existe. |
| 10.1.3 | FIN CASO DE USO |
 
**ca 10.2 — El usuario consultado no tiene mensajes**
 
| N° | Paso |
|---|---|
| 10.2.1 | El usuario consultado no ha publicado ningún mensaje público. |
| 10.2.2 | El sistema muestra el perfil con un texto indicando que todavía no hay mensajes. |
| 10.2.3 | FIN CASO DE USO |
 
### Requerimientos no funcionales
 
| Cod | Nombre | Descripción |
|---|---|---|
| rnf 10.1 | Contenido del muro | El muro contiene únicamente los mensajes públicos del usuario y sus republicaciones. Nunca incluye mensajes privados, ni siquiera para el propio autor. Deriva de RNF11 y RNF14. |
| rnf 10.2 | Datos no expuestos | El muro no muestra la dirección de correo del usuario consultado ni ningún dato de autenticación. Deriva de RNF38. |
 
### Observaciones
 
| Cod | Descripción |
|---|---|
| {Ob 10.1} | Este caso de uso es accesible para cualquier usuario del sistema, siga o no al usuario consultado. Es la consecuencia directa de la característica C19: el seguimiento determina qué llega al tablón, no qué se puede leer. |
| {Ob 10.2} | El muro propio es el mismo caso de uso aplicado al usuario en sesión. |
 
### Documentación anexa
 
| Nombre | Tipo | Nombre/Lugar |
|---|---|---|
| — | — | — |
 
---
---
 
# PAQUETE: GESTIÓN DE RELACIONES
 
---
 
## CU0011 — Seguir Usuario
 
### Resumen ejecutivo
 
| Campo | Contenido |
|---|---|
| Código | CU0011 |
| Paquete | Gestión de Relaciones |
| Nombre | Seguir Usuario |
| Versión | 1.0 |
| Prioridad | 9 |
| Confeccionó | Abel |
| Relevó | Abel |
| Revisó | — |
| Descripción | Permite que un usuario comience a seguir a otro, de modo que sus mensajes empiecen a aparecer en su tablón. |
| Actores | **Usuario**: empleado registrado con sesión activa. |
| Frecuencia | Alta al comienzo de uso; baja una vez consolidada la red de contactos. |
| Comentarios | Sin este caso de uso el tablón (CU0009) no tiene contenido ajeno. El seguimiento es unilateral: no requiere aprobación del seguido (característica C18). |
| Observaciones | Ver {Ob 11.1} |
 
### Curso normal
 
| Precondición |
|---|
| El Usuario debe tener una sesión activa. |
 
| N° | Paso (Flujo de Sucesos) |
|---|---|
| 1 | El Usuario selecciona la opción "Seguir" desde el muro de otro usuario o desde un resultado de búsqueda. {ca 11.1} |
| 2 | El sistema verifica que el usuario a seguir exista y esté activo. |
| 3 | El sistema verifica que el Usuario no sea el mismo usuario a seguir. {ca 11.2} |
| 4 | El sistema verifica que no exista ya un seguimiento entre ambos. {ca 11.3} |
| 5 | El sistema registra el seguimiento con su fecha de inicio. {rnf 11.1} |
| 6 | El sistema actualiza la vista indicando que ahora lo sigue. A partir de ese momento los mensajes y republicaciones del usuario seguido aparecen en el tablón del Usuario. |
| 7 | FIN CASO DE USO |
 
### Cursos alternativos
 
**ca 11.1 — El usuario a seguir no existe o no está activo**
 
| N° | Paso |
|---|---|
| 11.1.1 | El usuario indicado no corresponde a ninguna cuenta activa. |
| 11.1.2 | El sistema informa la situación y no registra el seguimiento. |
| 11.1.3 | FIN CASO DE USO |
 
**ca 11.2 — El Usuario intenta seguirse a sí mismo**
 
| N° | Paso |
|---|---|
| 11.2.1 | El usuario a seguir coincide con el Usuario en sesión. |
| 11.2.2 | El sistema rechaza la operación. Los mensajes propios ya forman parte del tablón. |
| 11.2.3 | FIN CASO DE USO |
 
**ca 11.3 — El seguimiento ya existe**
 
| N° | Paso |
|---|---|
| 11.3.1 | Ya hay un seguimiento registrado entre ambos usuarios. |
| 11.3.2 | El sistema no crea un segundo seguimiento y actualiza la vista indicando que el Usuario ya lo sigue, con la opción "Dejar de seguir" (CU0012). **La opción "Dejar de seguir" queda FUERA DEL ALCANCE DE REALIZACIÓN de esta versión: CU0012 queda especificado y no se implementa. En esta iteración la vista muestra únicamente la marca "Siguiendo", sin acción asociada.** Ver {Ob 11.4}. |
| 11.3.3 | FIN CASO DE USO |
 
### Requerimientos no funcionales
 
| Cod | Nombre | Descripción |
|---|---|---|
| rnf 11.1 | Unicidad del seguimiento | No pueden existir dos seguimientos con el mismo par seguidor-seguido. La restricción se aplica en el modelo de datos, no solo en la interfaz. Deriva de RNF23. |
| rnf 11.2 | Seguimiento unilateral | El seguimiento tiene efecto inmediato y no requiere aceptación del usuario seguido. Deriva de la característica C18. |
 
### Observaciones
 
| Cod | Descripción |
|---|---|
| {Ob 11.1} | Este caso de uso realiza la regla automática RA08. |
| {Ob 11.2} | El usuario seguido no recibe ninguna notificación. Esa característica es C27, registrada y no aprobada. |
| {Ob 11.3} | Seguir a un usuario no da acceso a nada nuevo en términos de lectura: sus mensajes públicos ya eran accesibles desde su muro. Lo que cambia es la entrega: pasan a aparecer en el tablón. |
| {Ob 11.4} | CU0012 está fuera del alcance de realización, de modo que en esta versión ninguna pantalla ofrece dejar de seguir. Un seguimiento registrado no se puede deshacer desde la interfaz. *Detectado en el flujo de Diseño (`DISEÑO_MiBlog.md` §1, H4).* |
 
### Documentación anexa
 
| Nombre | Tipo | Nombre/Lugar |
|---|---|---|
| — | — | — |
 
---
 
## CU0012 — Dejar de Seguir Usuario
 
### Resumen ejecutivo
 
| Campo | Contenido |
|---|---|
| Código | CU0012 |
| Paquete | Gestión de Relaciones |
| Nombre | Dejar de Seguir Usuario |
| Versión | 1.0 |
| Prioridad | 3 |
| Confeccionó | Abel |
| Relevó | Abel |
| Revisó | — |
| Descripción | Permite que un usuario deje de seguir a otro, de modo que sus mensajes dejen de aparecer en su tablón. |
| Actores | **Usuario**: empleado registrado con sesión activa. |
| Frecuencia | Baja. |
| Comentarios | Complementa a CU0011. Proviene de la característica C18. |
| Observaciones | Ver {Ob 12.1} |
 
### Curso normal
 
| Precondición |
|---|
| El Usuario debe tener una sesión activa y estar siguiendo al usuario en cuestión. |
 
| N° | Paso (Flujo de Sucesos) |
|---|---|
| 1 | El Usuario selecciona la opción "Dejar de seguir" desde el muro del usuario seguido o desde su listado de seguidos. |
| 2 | El sistema verifica que exista el seguimiento. {ca 12.1} |
| 3 | El sistema elimina el seguimiento. |
| 4 | El sistema actualiza la vista. Los mensajes y republicaciones de ese usuario dejan de aparecer en el tablón del Usuario. {rnf 12.1} |
| 5 | FIN CASO DE USO |
 
### Cursos alternativos
 
**ca 12.1 — El seguimiento no existe**
 
| N° | Paso |
|---|---|
| 12.1.1 | No hay seguimiento registrado entre ambos usuarios. |
| 12.1.2 | El sistema actualiza la vista mostrando la opción "Seguir", sin informar error. |
| 12.1.3 | FIN CASO DE USO |
 
### Requerimientos no funcionales
 
| Cod | Nombre | Descripción |
|---|---|---|
| rnf 12.1 | Conservación de las republicaciones | Dejar de seguir a un usuario no elimina las republicaciones que el Usuario haya hecho de sus mensajes: esas republicaciones son publicaciones propias y permanecen en su muro. Deriva de RNF14. |
 
### Observaciones
 
| Cod | Descripción |
|---|---|
| {Ob 12.1} | La operación no requiere confirmación: es reversible en un paso mediante CU0011. |
| {Ob 12.2} | El usuario que deja de ser seguido no recibe ninguna notificación. |
 
### Documentación anexa
 
| Nombre | Tipo | Nombre/Lugar |
|---|---|---|
| — | — | — |
 
---
 
## CU0013 — Consultar Seguidores y Seguidos
 
### Resumen ejecutivo
 
| Campo | Contenido |
|---|---|
| Código | CU0013 |
| Paquete | Gestión de Relaciones |
| Nombre | Consultar Seguidores y Seguidos |
| Versión | 1.0 |
| Prioridad | 6 |
| Confeccionó | Abel |
| Relevó | Abel |
| Revisó | — |
| Descripción | Permite que el usuario consulte, desde su página principal, quiénes lo siguen y a quiénes sigue. |
| Actores | **Usuario**: empleado registrado con sesión activa. |
| Frecuencia | Media. |
| Comentarios | El enunciado exige expresamente que esta consulta esté disponible en la página principal. |
| Observaciones | Ver {Ob 13.1} |
 
### Curso normal
 
| Precondición |
|---|
| El Usuario debe tener una sesión activa. |
 
| N° | Paso (Flujo de Sucesos) |
|---|---|
| 1 | El Usuario accede a su página principal o selecciona la opción de ver sus contactos. |
| 2 | El sistema obtiene el listado de usuarios que siguen al Usuario y el listado de usuarios a los que el Usuario sigue. |
| 3 | El sistema muestra ambos listados por separado, con la cantidad de cada uno, indicando de cada usuario su foto, su nombre de usuario y su nombre completo. {rnf 13.1} {ca 13.1} |
| 4 | El Usuario puede seleccionar a cualquiera de ellos para ver su muro (CU0010). |
| 5 | FIN CASO DE USO |
 
### Cursos alternativos
 
**ca 13.1 — Alguno de los listados está vacío**
 
| N° | Paso |
|---|---|
| 13.1.1 | El Usuario no tiene seguidores, no sigue a nadie, o ambas cosas. |
| 13.1.2 | El sistema muestra el listado vacío con un texto explicativo, y en el caso de los seguidos ofrece buscar usuarios (CU0014). |
| 13.1.3 | El caso de uso continúa en el paso 4 del curso normal. |
 
### Requerimientos no funcionales
 
| Cod | Nombre | Descripción |
|---|---|---|
| rnf 13.1 | Ubicación en la página principal | Ambos listados deben ser alcanzables desde la página principal del usuario, en cumplimiento del requisito R08 del enunciado. Deriva de RNF14. |
 
### Observaciones
 
| Cod | Descripción |
|---|---|
| {Ob 13.1} | El enunciado no pide que un usuario pueda ver los seguidores de otro. Este caso de uso se limita a los propios. |
 
### Documentación anexa
 
| Nombre | Tipo | Nombre/Lugar |
|---|---|---|
| — | — | — |
 
---
 
## CU0014 — Buscar Usuarios
 
### Resumen ejecutivo
 
| Campo | Contenido |
|---|---|
| Código | CU0014 |
| Paquete | Gestión de Relaciones |
| Nombre | Buscar Usuarios |
| Versión | 1.0 |
| Prioridad | 3 |
| Confeccionó | Abel |
| Relevó | Abel |
| Revisó | — |
| Descripción | Permite que un usuario encuentre a otros usuarios del sistema por su nombre de usuario o su nombre completo. |
| Actores | **Usuario**: empleado registrado con sesión activa. |
| Frecuencia | Media. |
| Comentarios | No está en el enunciado. Proviene de la característica C21: sin buscador no hay forma de encontrar a quién seguir. |
| Observaciones | Ver {Ob 14.1} |
 
### Curso normal
 
| Precondición |
|---|
| El Usuario debe tener una sesión activa. |
 
| N° | Paso (Flujo de Sucesos) |
|---|---|
| 1 | El Usuario ingresa un criterio de búsqueda en el campo correspondiente y confirma. {ca 14.1} |
| 2 | El sistema busca las cuentas activas cuyo nombre de usuario o nombre completo contengan el criterio ingresado. {rnf 14.1} |
| 3 | El sistema muestra los resultados con la foto, el nombre de usuario y el nombre completo de cada uno, e indica si el Usuario ya los sigue. {ca 14.2} |
| 4 | El Usuario puede acceder al muro de cualquier resultado (CU0010) o seguirlo directamente (CU0011). **El acceso al muro queda FUERA DEL ALCANCE DE REALIZACIÓN de esta versión: CU0010 queda especificado y no se implementa. En esta iteración el resultado de búsqueda solo ofrece seguir.** Ver {Ob 14.3}. |
| 5 | FIN CASO DE USO |
 
### Cursos alternativos
 
**ca 14.1 — Criterio de búsqueda vacío**
 
| N° | Paso |
|---|---|
| 14.1.1 | El Usuario confirma sin ingresar ningún criterio. |
| 14.1.2 | El sistema no ejecuta la búsqueda e indica que debe ingresar al menos un carácter. |
| 14.1.3 | El caso de uso continúa en el paso 1 del curso normal. |
 
**ca 14.2 — Sin resultados**
 
| N° | Paso |
|---|---|
| 14.2.1 | Ninguna cuenta activa coincide con el criterio. |
| 14.2.2 | El sistema informa que no se encontraron usuarios y sugiere revisar el criterio. |
| 14.2.3 | FIN CASO DE USO |
 
### Requerimientos no funcionales
 
| Cod | Nombre | Descripción |
|---|---|---|
| rnf 14.1 | Búsqueda parcial e insensible a mayúsculas | La búsqueda devuelve coincidencias parciales y no distingue mayúsculas de minúsculas ni acentos. Deriva de RNF16. |
| rnf 14.2 | Datos no expuestos en los resultados | Los resultados no muestran la dirección de correo de los usuarios encontrados. Deriva de RNF38. |
 
### Observaciones
 
| Cod | Descripción |
|---|---|
| {Ob 14.1} | Este caso de uso busca usuarios, no mensajes. La búsqueda de mensajes se realiza por etiqueta en CU0016. La búsqueda de texto libre dentro de los mensajes es la característica C28, registrada y no aprobada. |
| {Ob 14.2} | Las cuentas no activas no aparecen en los resultados. |
| {Ob 14.3} | CU0010 está fuera del alcance de realización, de modo que en esta versión la pantalla de búsqueda es el **único** punto de entrada a CU0011 Seguir Usuario. Detectado y registrado en el flujo de Análisis (`ANALISIS_MiBlog.md` §1.3). |
 
### Documentación anexa
 
| Nombre | Tipo | Nombre/Lugar |
|---|---|---|
| — | — | — |
 
---
---
 
# PAQUETE: TENDENCIAS
 
---
 
## CU0015 — Ver Temas del Momento
 
### Resumen ejecutivo
 
| Campo | Contenido |
|---|---|
| Código | CU0015 |
| Paquete | Tendencias | 
| Nombre | Ver Temas del Momento |
| Versión | 1.0 |
| Prioridad | 10 |
| Confeccionó | Abel |
| Relevó | Abel |
| Revisó | — |
| Descripción | Muestra el listado de las etiquetas más repetidas en los mensajes publicados durante los últimos `n` días. |
| Actores | **Usuario**: empleado registrado con sesión activa. |
| Frecuencia | Alta. Se muestra junto con el tablón. |
| Comentarios | Es el caso de uso con el algoritmo más sensible del sistema. El mismo cálculo se reutiliza en el resumen semanal (CU0019). |
| Observaciones | Ver {Ob 15.1} |
 
### Curso normal
 
| Precondición |
|---|
| El Usuario debe tener una sesión activa. Debe existir un valor configurado de `n` (CU0017). |
 
| N° | Paso (Flujo de Sucesos) |
|---|---|
| 1 | El Usuario accede a su página principal o a la sección de temas del momento. |
| 2 | El sistema obtiene el valor vigente de `n` de la configuración del sitio. |
| 3 | El sistema cuenta, para cada etiqueta, en cuántos mensajes públicos publicados dentro de los últimos `n` días aparece. {rnf 15.1} {rnf 15.2} |
| 4 | El sistema ordena las etiquetas de mayor a menor cantidad de apariciones. {ca 15.1} |
| 5 | El sistema muestra el listado con cada etiqueta y su cantidad de apariciones. Cada etiqueta es un enlace al listado de mensajes que la contienen (CU0016). {rnf 15.3} {rnf 15.4} |
| 6 | FIN CASO DE USO |
 
### Cursos alternativos
 
**ca 15.1 — No hay etiquetas en la ventana de tiempo**
 
| N° | Paso |
|---|---|
| 15.1.1 | Ningún mensaje público publicado en los últimos `n` días contiene etiquetas. |
| 15.1.2 | El sistema muestra la sección con un texto indicando que todavía no hay temas del momento. |
| 15.1.3 | FIN CASO DE USO |
 
### Requerimientos no funcionales
 
| Cod | Nombre | Descripción |
|---|---|---|
| rnf 15.1 | Alcance del conteo | Solo se cuentan los mensajes públicos. Los mensajes privados quedan excluidos del cálculo. Una republicación no incrementa el conteo: la etiqueta se cuenta una sola vez, en el mensaje original. Deriva de RNF11 y de la regla RA03. |
| rnf 15.2 | Configuración vigente | El valor de `n` se lee en cada cálculo, de modo que un cambio hecho por el administrador se refleje de inmediato sin reiniciar el sistema. Deriva de RNF06 y RNF28. |
| rnf 15.3 | Tiempo de respuesta | Con el juego de datos de prueba definido para el proyecto, el cálculo se resuelve en menos de 3 segundos. Deriva de RNF20. |
| rnf 15.4 | Contenido del listado | Cada entrada muestra la etiqueta y su cantidad de apariciones, y la etiqueta es un enlace navegable al listado de mensajes que la contienen. Deriva de RNF17. |
 
### Observaciones
 
| Cod | Descripción |
|---|---|
| {Ob 15.1} | Este caso de uso realiza la regla automática RA03. |
| {Ob 15.2} | El enunciado no fija cuántas etiquetas se muestran. Se adopta un máximo de diez, documentado acá para que el plan de pruebas pueda verificarlo. |
| {Ob 15.3} | El criterio de desempate entre etiquetas con la misma cantidad de apariciones es la fecha de aparición más reciente. |
 
### Documentación anexa
 
| Nombre | Tipo | Nombre/Lugar |
|---|---|---|
| — | — | — |
 
---
 
## CU0016 — Buscar Mensajes por Etiqueta
 
### Resumen ejecutivo
 
| Campo | Contenido |
|---|---|
| Código | CU0016 |
| Paquete | Tendencias |
| Nombre | Buscar Mensajes por Etiqueta |
| Versión | 1.0 |
| Prioridad | 6 |
| Confeccionó | Abel |
| Relevó | Abel |
| Revisó | — |
| Descripción | Muestra el listado de los mensajes públicos que contienen una etiqueta determinada. |
| Actores | **Usuario**: empleado registrado con sesión activa. |
| Frecuencia | Media. |
| Comentarios | Es el destino de los enlaces del resumen semanal por email (R15) y de los enlaces de los temas del momento. Sin este caso de uso, esos enlaces no tienen adónde apuntar. |
| Observaciones | Ver {Ob 16.1} |
 
### Curso normal
 
| Precondición |
|---|
| El Usuario debe tener una sesión activa. |
 
| N° | Paso (Flujo de Sucesos) |
|---|---|
| 1 | El Usuario selecciona una etiqueta desde un mensaje, desde los temas del momento o desde un enlace del resumen semanal. |
| 2 | El sistema verifica que la etiqueta exista. {ca 16.1} |
| 3 | El sistema reúne los mensajes públicos que contienen esa etiqueta. {rnf 16.1} |
| 4 | El sistema ordena los mensajes de más reciente a más antiguo. {ca 16.2} |
| 5 | El sistema muestra el listado indicando de cada mensaje su autor, su fecha y su texto vigente. |
| 6 | FIN CASO DE USO |
 
### Cursos alternativos
 
**ca 16.1 — La etiqueta no existe**
 
| N° | Paso |
|---|---|
| 16.1.1 | La etiqueta indicada no está registrada en el sistema. |
| 16.1.2 | El sistema informa que no existen mensajes con esa etiqueta. |
| 16.1.3 | FIN CASO DE USO |
 
**ca 16.2 — La etiqueta existe pero ya no tiene mensajes**
 
| N° | Paso |
|---|---|
| 16.2.1 | Todos los mensajes que contenían la etiqueta fueron borrados o editados. |
| 16.2.2 | El sistema muestra el listado vacío con un texto explicativo. |
| 16.2.3 | FIN CASO DE USO |
 
### Requerimientos no funcionales
 
| Cod | Nombre | Descripción |
|---|---|---|
| rnf 16.1 | Alcance del listado | El listado contiene únicamente mensajes públicos. Los mensajes privados que contienen la etiqueta quedan excluidos, cualquiera sea el usuario que consulta. Deriva de RNF11. |
| rnf 16.2 | Sin límite temporal | A diferencia de los temas del momento, este listado no se restringe a los últimos `n` días: incluye todos los mensajes históricos con esa etiqueta. Deriva del requisito R15 del enunciado. |
 
### Observaciones
 
| Cod | Descripción |
|---|---|
| {Ob 16.1} | La diferencia entre CU0015 y CU0016 es importante y conviene tenerla clara: CU0015 cuenta etiquetas dentro de una ventana de `n` días; CU0016 lista mensajes de una etiqueta sin límite de tiempo. |
| {Ob 16.2} | El acceso a este caso de uso desde el enlace de un email requiere sesión activa. Si el usuario no la tiene, el sistema lo lleva a CU0002 y luego al listado solicitado. |
 
### Documentación anexa
 
| Nombre | Tipo | Nombre/Lugar |
|---|---|---|
| — | — | — |
 
---
---
 
# PAQUETE: ADMINISTRACIÓN
 
---
 
## CU0017 — Configurar Ventana de Días `n`
 
### Resumen ejecutivo
 
| Campo | Contenido |
|---|---|
| Código | CU0017 |
| Paquete | Administración |
| Nombre | Configurar Ventana de Días `n` |
| Versión | 1.0 |
| Prioridad | 6 |
| Confeccionó | Abel |
| Relevó | Abel |
| Revisó | — |
| Descripción | Permite que el administrador del sitio modifique la cantidad de días que se consideran para calcular los temas del momento. |
| Actores | **Administrador del Sitio**: usuario con permisos de configuración. Es una especialización del actor Usuario. |
| Frecuencia | Muy baja. Se ajusta al poner en marcha el sistema y luego de forma esporádica. |
| Comentarios | Es el único parámetro de configuración que el enunciado pone expresamente en manos del administrador. |
| Observaciones | Ver {Ob 17.1} |
 
### Curso normal
 
| Precondición |
|---|
| El Administrador debe tener una sesión activa y su cuenta debe tener rol de administrador. |
 
| N° | Paso (Flujo de Sucesos) |
|---|---|
| 1 | El Administrador accede a la sección de configuración del sitio. {ca 17.1} |
| 2 | El sistema muestra el valor vigente de `n` expresado en días. |
| 3 | El Administrador ingresa el nuevo valor y confirma. {ca 17.2} {ca 17.3} |
| 4 | El sistema valida que el valor sea un número entero dentro del rango admitido. {rnf 17.1} |
| 5 | El sistema guarda el nuevo valor, junto con la fecha de modificación y el administrador que la realizó. |
| 6 | El sistema informa que la configuración fue actualizada. El nuevo valor rige para los siguientes cálculos de temas del momento, tanto en CU0015 como en CU0019. {rnf 17.2} |
| 7 | FIN CASO DE USO |
 
### Cursos alternativos
 
**ca 17.1 — El usuario no tiene rol de administrador**
 
| N° | Paso |
|---|---|
| 17.1.1 | Un usuario sin rol de administrador intenta acceder a la sección de configuración. |
| 17.1.2 | El sistema rechaza el acceso e informa que no tiene permisos suficientes. |
| 17.1.3 | FIN CASO DE USO |
 
**ca 17.2 — Valor no numérico o fuera de rango**
 
| N° | Paso |
|---|---|
| 17.2.1 | El valor ingresado no es un número entero, o está fuera del rango admitido. |
| 17.2.2 | El sistema informa el rango válido y conserva el valor anterior sin modificar. |
| 17.2.3 | El caso de uso continúa en el paso 3 del curso normal. |
 
**ca 17.3 — El Administrador cancela**
 
| N° | Paso |
|---|---|
| 17.3.1 | El Administrador selecciona "Cancelar". |
| 17.3.2 | El sistema descarta el cambio y mantiene el valor vigente. |
| 17.3.3 | FIN CASO DE USO |
 
### Requerimientos no funcionales
 
| Cod | Nombre | Descripción |
|---|---|---|
| rnf 17.1 | Rango admitido | El valor de `n` debe ser un número entero entre 1 y 365 días. El enunciado no fija un rango; se adopta este criterio para que la validación sea verificable. Deriva de RNF06. |
| rnf 17.2 | Vigencia inmediata | El cambio tiene efecto en el siguiente cálculo, sin reiniciar el sistema ni volver a desplegarlo. El valor no puede estar fijo en el código. Deriva de RNF06 y RNF28. |
| rnf 17.3 | Control de permisos en el servidor | La verificación del rol de administrador se realiza del lado del servidor en cada solicitud. Ocultar la opción en el menú no se considera control suficiente. Deriva de RNF09 y RNF10. |
 
### Observaciones
 
| Cod | Descripción |
|---|---|
| {Ob 17.1} | El alcance del administrador se limita a este caso de uso y a CU0018. No modera contenido ni da de baja usuarios: esas son las características C31 y C32, registradas y no aprobadas. |
| {Ob 17.2} | El sistema debe tener un valor inicial de `n` cargado al ponerse en marcha, para que CU0015 y CU0019 puedan ejecutarse antes de la primera configuración. |
 
### Documentación anexa
 
| Nombre | Tipo | Nombre/Lugar |
|---|---|---|
| — | — | — |
 
---
 
## CU0018 — Registrar Aplicación Externa
 
### Resumen ejecutivo
 
| Campo | Contenido |
|---|---|
| Código | CU0018 |
| Paquete | Administración |
| Nombre | Registrar Aplicación Externa |
| Versión | 1.0 |
| Prioridad | 7 |
| Confeccionó | Abel |
| Relevó | Abel |
| Revisó | — |
| Descripción | Permite que el administrador dé de alta una aplicación autorizada a consumir la API REST, le emita su credencial de acceso y pueda darla de baja. |
| Actores | **Administrador del Sitio**: usuario con permisos de configuración. |
| Frecuencia | Muy baja. |
| Comentarios | El enunciado exige que el acceso a la API esté restringido a aplicaciones registradas, pero no define quién las registra. La respuesta es la característica C24. |
| Observaciones | Ver {Ob 18.1} |
 
### Curso normal
 
| Precondición |
|---|
| El Administrador debe tener una sesión activa y su cuenta debe tener rol de administrador. |
 
| N° | Paso (Flujo de Sucesos) |
|---|---|
| 1 | El Administrador accede a la sección de aplicaciones externas. {ca 18.1} |
| 2 | El sistema muestra el listado de aplicaciones registradas con su nombre, su fecha de registro y su estado. |
| 3 | El Administrador selecciona la opción de registrar una nueva aplicación e ingresa su nombre. {ca 18.2} {ca 18.3} |
| 4 | El sistema verifica que no exista otra aplicación registrada con el mismo nombre. |
| 5 | El sistema genera una credencial de acceso, la almacena cifrada y registra la aplicación en estado activo. {rnf 18.1} |
| 6 | El sistema muestra la credencial generada una única vez, advirtiendo que no volverá a mostrarse y que debe entregarse al responsable de la aplicación por un canal seguro. {rnf 18.2} |
| 7 | El sistema actualiza el listado. La aplicación ya puede consumir CU0020 y CU0021. |
| 8 | FIN CASO DE USO |
 
### Cursos alternativos
 
**ca 18.1 — El usuario no tiene rol de administrador**
 
| N° | Paso |
|---|---|
| 18.1.1 | Un usuario sin rol de administrador intenta acceder a la sección. |
| 18.1.2 | El sistema rechaza el acceso e informa que no tiene permisos suficientes. |
| 18.1.3 | FIN CASO DE USO |
 
**ca 18.2 — Nombre de aplicación duplicado o vacío**
 
| N° | Paso |
|---|---|
| 18.2.1 | El nombre ingresado está vacío o ya pertenece a otra aplicación registrada. |
| 18.2.2 | El sistema informa el problema y no registra la aplicación ni emite credencial. |
| 18.2.3 | El caso de uso continúa en el paso 3 del curso normal. |
 
**ca 18.3 — Baja de una aplicación registrada**
 
| N° | Paso |
|---|---|
| 18.3.1 | El Administrador selecciona la opción de dar de baja sobre una aplicación del listado. |
| 18.3.2 | El sistema solicita confirmación e informa que la aplicación perderá el acceso a la API de forma inmediata. |
| 18.3.3 | El Administrador confirma. |
| 18.3.4 | El sistema marca la aplicación como inactiva. Su credencial deja de ser válida para CU0020 y CU0021. Los mensajes publicados anteriormente a través de ella se conservan. {rnf 18.3} |
| 18.3.5 | FIN CASO DE USO |
 
### Requerimientos no funcionales
 
| Cod | Nombre | Descripción |
|---|---|---|
| rnf 18.1 | Almacenamiento de la credencial | La credencial se guarda mediante función de hash, igual que las claves de los usuarios. El sistema no puede recuperarla en texto plano después de emitirla. Deriva de RNF12. |
| rnf 18.2 | Exhibición única | La credencial se muestra una sola vez, en el momento de la emisión. Si se pierde, la única opción es dar de baja la aplicación y registrarla nuevamente. Deriva de RNF12. |
| rnf 18.3 | Efecto inmediato de la baja | Una credencial dada de baja deja de ser válida en la siguiente llamada a la API, sin necesidad de reiniciar el sistema. Deriva de RNF12. |
 
### Observaciones
 
| Cod | Descripción |
|---|---|
| {Ob 18.1} | El mecanismo de autenticación elegido es una credencial de aplicación enviada en cada llamada, conforme a la característica C25. La alternativa OAuth es la característica C34, registrada y no aprobada por exceder el alcance de esta versión. |
| {Ob 18.2} | La limitación de cantidad de llamadas por aplicación queda expresamente fuera de alcance, según lo indicado en el documento de requisitos no funcionales. |
 
### Documentación anexa
 
| Nombre | Tipo | Nombre/Lugar |
|---|---|---|
| Documentación de la API | Documento técnico | Pendiente |
 
---
---
 
# PAQUETE: NOTIFICACIONES
 
---
 
## CU0019 — Enviar Email Semanal de Temas del Momento
 
### Resumen ejecutivo
 
| Campo | Contenido |
|---|---|
| Código | CU0019 |
| Paquete | Notificaciones |
| Nombre | Enviar Email Semanal de Temas del Momento |
| Versión | 1.0 |
| Prioridad | 10 |
| Confeccionó | Abel |
| Relevó | Abel |
| Revisó | — |
| Descripción | Una vez por semana, el sistema calcula los temas del momento y envía a cada usuario un email con el listado y los enlaces al listado de mensajes de cada etiqueta. |
| Actores | **Tiempo** (actor primario): evento temporal que dispara la ejecución semanal. No es una persona ni un sistema externo: es el vencimiento del plazo configurado. **Servidor de Correo** (actor secundario): servicio externo al que el sistema entrega los emails para su distribución. |
| Frecuencia | Semanal. |
| Comentarios | Es el único caso de uso del sistema que no inicia una persona, y el de mayor riesgo técnico: depende de un planificador de tareas, de un proceso que se ejecuta sin interfaz y de un servicio externo de correo. |
| Observaciones | Ver {Ob 19.1} |
 
### Curso normal
 
| Precondición |
|---|
| Debe existir un valor configurado de `n` (CU0017) y una configuración válida de conexión al servidor de correo. |
 
| N° | Paso (Flujo de Sucesos) |
|---|---|
| 1 | El Tiempo alcanza el día y la hora configurados para el envío semanal. {rnf 19.1} |
| 2 | El sistema obtiene el valor vigente de `n` de la configuración del sitio. |
| 3 | El sistema calcula los temas del momento aplicando el mismo criterio que CU0015: cuenta las apariciones de cada etiqueta en los mensajes públicos de los últimos `n` días y las ordena de mayor a menor. {rnf 19.2} {ca 19.1} |
| 4 | El sistema obtiene el listado de todos los usuarios activos. |
| 5 | El sistema arma el contenido del email, incluyendo cada etiqueta, su cantidad de apariciones y el enlace al listado de mensajes que la contienen (CU0016). {rnf 19.3} |
| 6 | El sistema entrega cada email al servidor de correo, usuario por usuario. {ca 19.2} {ca 19.3} |
| 7 | El sistema registra el envío con su fecha, la cantidad de destinatarios alcanzados y los temas incluidos. {rnf 19.4} |
| 8 | FIN CASO DE USO |
 
### Cursos alternativos
 
**ca 19.1 — No hay temas del momento en la ventana de tiempo**
 
| N° | Paso |
|---|---|
| 19.1.1 | Ningún mensaje público publicado en los últimos `n` días contiene etiquetas. |
| 19.1.2 | El sistema no envía ningún email y registra la ejecución indicando que no hubo temas para informar. |
| 19.1.3 | FIN CASO DE USO |
 
**ca 19.2 — Falla el envío a un destinatario**
 
| N° | Paso |
|---|---|
| 19.2.1 | El servidor de correo rechaza el email de un destinatario, o la dirección es inválida. |
| 19.2.2 | El sistema registra el error en el log con la identificación del destinatario y el motivo informado. |
| 19.2.3 | El sistema continúa con el destinatario siguiente. El fallo de un envío individual no interrumpe el proceso. |
| 19.2.4 | El caso de uso continúa en el paso 6 del curso normal. |
 
**ca 19.3 — El servidor de correo no está disponible**
 
| N° | Paso |
|---|---|
| 19.3.1 | El sistema no logra establecer conexión con el servidor de correo. |
| 19.3.2 | El sistema interrumpe el proceso y registra el error en el log, indicando cuántos destinatarios quedaron sin alcanzar. |
| 19.3.3 | El sistema deja la ejecución registrada como fallida, de modo que pueda reintentarse manualmente. |
| 19.3.4 | FIN CASO DE USO |
 
### Requerimientos no funcionales
 
| Cod | Nombre | Descripción |
|---|---|---|
| rnf 19.1 | Planificación configurable | El día y la hora de ejecución son configurables y no están fijos en el código. La ejecución se programa fuera del horario laboral. Deriva de RNF07 y RNF28. |
| rnf 19.2 | Reutilización del cálculo | El cálculo de los temas del momento se resuelve con el mismo componente que utiliza CU0015. No puede haber dos implementaciones del algoritmo, porque derivarían con el tiempo y el email informaría algo distinto de lo que muestra la pantalla. Deriva de RNF26. |
| rnf 19.3 | Enlaces absolutos | Los enlaces del email deben ser direcciones absolutas y alcanzables desde el cliente de correo del usuario. Deriva del requisito R15 del enunciado. |
| rnf 19.4 | Ejecución asíncrona y registrada | El proceso se ejecuta de forma asíncrona y no bloquea el uso de la aplicación web. Su inicio, su fin y sus errores quedan registrados en el log con fecha y hora. Deriva de RNF21, RNF22 y RNF24. |
| rnf 19.5 | Credenciales fuera del repositorio | Los datos de conexión al servidor de correo se leen de variables de entorno y no se versionan junto con el código. Deriva de RNF13. |
 
### Observaciones
 
| Cod | Descripción |
|---|---|
| {Ob 19.1} | Este caso de uso realiza las reglas automáticas RA03 y RA11. |
| {Ob 19.2} | Es el caso de uso arquitectónicamente más significativo del sistema: es el único que incorpora planificador de tareas, proceso sin interfaz y servicio externo. Por eso se diseña temprano, aunque su prioridad para el usuario final no sea la más alta. |
| {Ob 19.3} | El enunciado no prevé que un usuario pueda darse de baja del envío. Todos los usuarios activos son destinatarios. |
| {Ob 19.4} | El destinatario no necesita tener sesión activa para recibir el email, pero sí para abrir los enlaces, que lo llevan a CU0016. |
 
### Documentación anexa
 
| Nombre | Tipo | Nombre/Lugar |
|---|---|---|
| Plantilla del email semanal | Diseño de interfaz | Pendiente |
 
---
---
 
# PAQUETE: INTEGRACIÓN
 
---
 
## CU0020 — Publicar Mensaje vía API REST
 
### Resumen ejecutivo
 
| Campo | Contenido |
|---|---|
| Código | CU0020 |
| Paquete | Integración |
| Nombre | Publicar Mensaje vía API REST |
| Versión | 1.0 |
| Prioridad | 7 |
| Confeccionó | Abel |
| Relevó | Abel |
| Revisó | — |
| Descripción | Permite que una aplicación externa registrada publique un mensaje en nombre de un usuario del sistema. |
| Actores | **Aplicación Externa**: sistema de terceros previamente registrado mediante CU0018, que se autentica con su credencial. |
| Frecuencia | Variable, según las integraciones existentes. |
| Comentarios | El mensaje publicado por esta vía es indistinguible de uno publicado desde la web, salvo por el registro de su origen. |
| Observaciones | Ver {Ob 20.1} |
 
### Curso normal
 
| Precondición |
|---|
| La Aplicación Externa debe estar registrada y activa (CU0018), y debe contar con su credencial vigente. |
 
| N° | Paso (Flujo de Sucesos) |
|---|---|
| 1 | La Aplicación Externa envía la solicitud de publicación indicando su credencial, el usuario en cuyo nombre publica y el texto del mensaje. {rnf 20.1} |
| 2 | El sistema valida la credencial recibida y verifica que la aplicación esté activa. {ca 20.1} |
| 3 | El sistema verifica que el usuario indicado exista y esté activo. {ca 20.2} |
| 4 | El sistema valida que el texto no esté vacío y no supere los 140 caracteres. {ca 20.3} |
| 5 | El sistema analiza el texto y extrae etiquetas, menciones y links, con el mismo componente que utiliza CU0004. {rnf 20.2} |
| 6 | El sistema almacena el mensaje con su autor, su fecha, la aplicación que lo originó y su origen API. |
| 7 | El sistema responde confirmando la publicación e informando el identificador del mensaje creado. El mensaje queda disponible en el muro del usuario y en el tablón de sus seguidores. {rnf 20.3} |
| 8 | FIN CASO DE USO |
 
### Cursos alternativos
 
**ca 20.1 — Credencial ausente, inválida o dada de baja**
 
| N° | Paso |
|---|---|
| 20.1.1 | La solicitud no incluye credencial, la credencial no corresponde a ninguna aplicación, o la aplicación está inactiva. |
| 20.1.2 | El sistema rechaza la solicitud con el código de estado de no autenticado y no publica nada. |
| 20.1.3 | El sistema registra el intento en el log. |
| 20.1.4 | FIN CASO DE USO |
 
**ca 20.2 — El usuario indicado no existe o no está activo**
 
| N° | Paso |
|---|---|
| 20.2.1 | El usuario indicado no corresponde a ninguna cuenta activa. |
| 20.2.2 | El sistema rechaza la solicitud con el código de estado de recurso inexistente. |
| 20.2.3 | FIN CASO DE USO |
 
**ca 20.3 — Texto inválido**
 
| N° | Paso |
|---|---|
| 20.3.1 | El texto está vacío o supera los 140 caracteres. |
| 20.3.2 | El sistema rechaza la solicitud con el código de estado de solicitud inválida, indicando el límite y la longitud recibida. El texto no se recorta. |
| 20.3.3 | FIN CASO DE USO |
 
### Requerimientos no funcionales
 
| Cod | Nombre | Descripción |
|---|---|---|
| rnf 20.1 | Formato y versionado | La solicitud y la respuesta se intercambian en formato JSON, sobre una ruta versionada. Deriva de RNF35 y RNF37. |
| rnf 20.2 | Componente único de extracción | El análisis del texto se resuelve con el mismo componente que utiliza la aplicación web, para que un mensaje publicado por API y uno publicado por la web produzcan exactamente las mismas etiquetas y menciones. Deriva de RNF26. |
| rnf 20.3 | Códigos de estado estándar | Las respuestas utilizan los códigos de estado HTTP estándar: creación exitosa, solicitud inválida, no autenticado, recurso inexistente y error interno. Deriva de RNF36. |
| rnf 20.4 | Validación equivalente a la web | Todas las validaciones de CU0004 se aplican igualmente acá. La API no es una puerta trasera con reglas más laxas. Deriva de RNF01 y RNF12. |
 
### Observaciones
 
| Cod | Descripción |
|---|---|
| {Ob 20.1} | Este caso de uso realiza las reglas automáticas RA01, RA02 y RA10. |
| {Ob 20.2} | El mensaje se atribuye al usuario indicado, no a la aplicación. La aplicación queda registrada como origen para poder auditar de dónde vino cada publicación. |
| {Ob 20.3} | La API no permite publicar mensajes privados. El enunciado limita los servicios web a publicar un mensaje y leer el muro de un usuario. |
 
### Documentación anexa
 
| Nombre | Tipo | Nombre/Lugar |
|---|---|---|
| Documentación de la API | Documento técnico | Pendiente |
 
---
 
## CU0021 — Leer Muro de un Usuario vía API REST
 
### Resumen ejecutivo
 
| Campo | Contenido |
|---|---|
| Código | CU0021 |
| Paquete | Integración |
| Nombre | Leer Muro de un Usuario vía API REST |
| Versión | 1.0 |
| Prioridad | 7 |
| Confeccionó | Abel |
| Relevó | Abel |
| Revisó | — |
| Descripción | Permite que una aplicación externa registrada obtenga los mensajes públicos de un usuario del sistema. |
| Actores | **Aplicación Externa**: sistema de terceros previamente registrado mediante CU0018, que se autentica con su credencial. |
| Frecuencia | Variable, según las integraciones existentes. |
| Comentarios | Es el caso de uso que da sentido a la distinción entre muro y tablón: lo que se expone es el conjunto de mensajes públicos de un único usuario. |
| Observaciones | Ver {Ob 21.1} |
 
### Curso normal
 
| Precondición |
|---|
| La Aplicación Externa debe estar registrada y activa (CU0018), y debe contar con su credencial vigente. |
 
| N° | Paso (Flujo de Sucesos) |
|---|---|
| 1 | La Aplicación Externa envía la solicitud de lectura indicando su credencial y el usuario cuyo muro desea consultar. {rnf 21.1} |
| 2 | El sistema valida la credencial recibida y verifica que la aplicación esté activa. {ca 21.1} |
| 3 | El sistema verifica que el usuario indicado exista y esté activo. {ca 21.2} |
| 4 | El sistema reúne los mensajes públicos de ese usuario y sus republicaciones, ordenados de más reciente a más antiguo. {rnf 21.2} {ca 21.3} |
| 5 | El sistema responde con el listado, informando de cada mensaje su identificador, su texto vigente, su fecha de publicación, si fue editado y sus etiquetas. |
| 6 | FIN CASO DE USO |
 
### Cursos alternativos
 
**ca 21.1 — Credencial ausente, inválida o dada de baja**
 
| N° | Paso |
|---|---|
| 21.1.1 | La solicitud no incluye credencial, la credencial no corresponde a ninguna aplicación, o la aplicación está inactiva. |
| 21.1.2 | El sistema rechaza la solicitud con el código de estado de no autenticado y no devuelve ningún dato. |
| 21.1.3 | El sistema registra el intento en el log. |
| 21.1.4 | FIN CASO DE USO |
 
**ca 21.2 — El usuario indicado no existe o no está activo**
 
| N° | Paso |
|---|---|
| 21.2.1 | El usuario indicado no corresponde a ninguna cuenta activa. |
| 21.2.2 | El sistema rechaza la solicitud con el código de estado de recurso inexistente. |
| 21.2.3 | FIN CASO DE USO |
 
**ca 21.3 — El usuario no tiene mensajes públicos**
 
| N° | Paso |
|---|---|
| 21.3.1 | El usuario existe pero no ha publicado ningún mensaje público. |
| 21.3.2 | El sistema responde con un listado vacío y el código de estado de éxito. La ausencia de mensajes no es un error. |
| 21.3.3 | FIN CASO DE USO |
 
### Requerimientos no funcionales
 
| Cod | Nombre | Descripción |
|---|---|---|
| rnf 21.1 | Formato y versionado | La solicitud y la respuesta se intercambian en formato JSON, sobre una ruta versionada. Deriva de RNF35 y RNF37. |
| rnf 21.2 | Exclusión de contenido privado | La respuesta contiene únicamente mensajes públicos. Nunca incluye mensajes privados, ni la clave del usuario, ni su dirección de correo. Deriva de RNF11 y RNF38. |
| rnf 21.3 | Códigos de estado estándar | Las respuestas utilizan los códigos de estado HTTP estándar. Deriva de RNF36. |
 
### Observaciones
 
| Cod | Descripción |
|---|---|
| {Ob 21.1} | Este caso de uso expone el muro, no el tablón. La diferencia es la que se explica en {Ob 9.2} de CU0009: el muro pertenece a un único usuario, el tablón reúne mensajes de varios autores. Una aplicación externa no puede consultar el tablón de nadie. |
| {Ob 21.2} | El acceso no depende de relaciones de seguimiento: la aplicación puede consultar el muro de cualquier usuario activo. Es la consecuencia de la característica C19. |
| {Ob 21.3} | La paginación de resultados no forma parte del alcance. |
 
### Documentación anexa
 
| Nombre | Tipo | Nombre/Lugar |
|---|---|---|
| Documentación de la API | Documento técnico | Pendiente |
 
---
---
 
## Tabla de control
 
| CU | Nombre | Paquete | Prioridad | Actor primario | RF |
|---|---|---|---|---|---|
| CU0001 | Registrar Usuario | Gestión de Usuarios | 10 | Visitante | RF01 |
| CU0002 | Iniciar Sesión | Gestión de Usuarios | 10 | Visitante | RF02 |
| CU0003 | Cerrar Sesión | Gestión de Usuarios | 3 | Usuario | RF03 |
| CU0004 | Publicar Mensaje | Gestión de Mensajes | 10 | Usuario | RF04 |
| CU0005 | Editar Mensaje Propio | Gestión de Mensajes | 7 | Usuario | RF05 |
| CU0006 | Borrar Mensaje Propio | Gestión de Mensajes | 7 | Usuario | RF06 |
| CU0007 | Republicar Mensaje | Gestión de Mensajes | 7 | Usuario | RF07 |
| CU0008 | Enviar Mensaje Privado | Gestión de Mensajes | 6 | Usuario | RF08 |
| CU0009 | Visualizar Tablón | Gestión de Mensajes | 10 | Usuario | RF09 |
| CU0010 | Consultar Muro de un Usuario | Gestión de Mensajes | 6 | Usuario | RF10 |
| CU0011 | Seguir Usuario | Gestión de Relaciones | 9 | Usuario | RF11 |
| CU0012 | Dejar de Seguir Usuario | Gestión de Relaciones | 3 | Usuario | RF12 |
| CU0013 | Consultar Seguidores y Seguidos | Gestión de Relaciones | 6 | Usuario | RF13 |
| CU0014 | Buscar Usuarios | Gestión de Relaciones | 3 | Usuario | RF14 |
| CU0015 | Ver Temas del Momento | Tendencias | 10 | Usuario | RF15 |
| CU0016 | Buscar Mensajes por Etiqueta | Tendencias | 6 | Usuario | RF16 |
| CU0017 | Configurar Ventana de Días `n` | Administración | 6 | Administrador | RF17 |
| CU0018 | Registrar Aplicación Externa | Administración | 7 | Administrador | RF18 |
| CU0019 | Enviar Email Semanal de Temas del Momento | Notificaciones | 10 | Tiempo | RF19 |
| CU0020 | Publicar Mensaje vía API REST | Integración | 7 | Aplicación Externa | RF20 |
| CU0021 | Leer Muro de un Usuario vía API REST | Integración | 7 | Aplicación Externa | RF21 |
 
**Total: 21 casos de uso especificados · 6 paquetes · 6 actores.**
 
---
 
## Control del documento
 
| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.0 | 13/09/2026 | Requisitos | Versión inicial: 21 casos de uso especificados con la plantilla de la cátedra. |
| 1.1 | 14/09/2026 | Análisis | Marcados como fuera del alcance de realización el paso 6 de CU0009 (CU0013 y CU0015) y el paso 4 de CU0014 (CU0010). Agregadas las observaciones {Ob 9.4}, {Ob 14.3} y {Ob 7.3}. Estado del documento a `[DECIDIDO]`. |
| 1.2 | 15/09/2026 | Diseño | Correcciones de los hallazgos del flujo de Diseño. CU0007: quitada la oferta de deshacer del `ca 7.3` (H3); `{Ob 7.3}` reescrita porque el `ca 7.1` sí es alcanzable, con el `ca 7.1` y la precondición ajustados (H5); agregado el `ca 7.4` para mensaje inexistente (H6); nuevas `{Ob 7.4}` y `{Ob 7.5}`. CU0011: "Dejar de seguir" del `ca 11.3` marcado fuera de alcance, con `{Ob 11.4}` (H4). CU0009: `rnf 9.3` referenciado desde el paso 5 y no desde el 6 (H12.1). CU0001: longitud mínima de clave en `rnf 1.1` y `{Ob 1.1}` corregida (H12.2). Convención 3: rango de RNF corregido a RNF42. Convención 7: la fila de RNF41 dice "dependencias adicionales **de autenticación**", como el propio RNF41. |
| 1.3 | 28/10/2026 | Implementación | CU0001: se documenta la forma admitida del nombre de usuario (letras, números y guion bajo; punto y guion solo en el medio), que antes solo estaba en el código: `ca 1.1` paso 1.1.1, `rnf 1.1` y la observación nueva `{Ob 1.3}`, que la explica como criterio propio y aclara que no cambia el RNF02. «Documentación anexa» de CU0001, CU0002, CU0004 y CU0009: en lugar de «Pendiente», apunta a las pantallas del `Prototipo de Interfaces`, que ya existe y se actualizó al diseño visual implementado. Ningún caso de uso cambia de curso normal ni de alcance. |
