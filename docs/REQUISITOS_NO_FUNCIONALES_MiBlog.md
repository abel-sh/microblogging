# LISTA DE REQUISITOS NO FUNCIONALES — Sistema MiBlog

**Versión:** 1.1 · **Última modificación:** 15/09/2026 · **Etapa:** Requisitos

**Materia:** Ingeniería de Software · **Alumno:** Abel · **Modalidad:** proyecto grupal, cursado en solitario
**Flujo del Proceso Unificado:** Requisitos (los RNF forman parte del modelo de requisitos, no son un anexo del Análisis)
**Trabajador responsable:** Analista de Sistemas, con revisión del Arquitecto
**Documentos previos:** `REQUISITOS_CANDIDATOS_MiBlog.md` · `REQUISITOS_FUNCIONALES_MiBlog.md`
**Estado del documento:** `[DECIDIDO]` — confirmado el 15/09/2026. La decisión tecnológica de la sección 8 rige desde el 13/09/2026.

---

## 1. Qué es este documento

Un requisito no funcional describe **cómo** tiene que comportarse el sistema, no **qué** tiene que hacer. No es una acción de un actor: es una condición que el sistema cumple siempre.

Dos aclaraciones que conviene tener presentes:

1. Los límites duros del enunciado —los 140 caracteres del mensaje y los 15 del nombre de usuario— son **requisitos no funcionales**, no casos de uso. Son restricciones sobre los datos, no acciones.
2. Cada RNF de este documento tiene una columna **Verificación**. Un requisito no funcional que ninguna prueba puede comprobar no es un requisito: es una expresión de deseo. Por eso acá no se prometen cifras de disponibilidad, usuarios concurrentes ni tiempos que después nadie va a medir.

Los RNF se referencian desde las especificaciones de casos de uso con la notación `{rnf XX}`.

### 1.1 Códigos usados en la columna *Origen*

| Código | Significa |
|---|---|
| **R00–R17** | Requisito escrito literalmente en `enunciado_microblogging.pdf`. |
| **C01–C38** | Característica de la lista de requisitos candidatos. Las que llevan código C y no código R son supuestos propios. |
| **Propio** | Restricción de calidad que no proviene del enunciado ni de una característica concreta, sino de una buena práctica de ingeniería adoptada para este proyecto. |
| **Cátedra** | Exigencia explícita de la cátedra. |

---

## 2. Restricciones del dominio

Salen directamente del enunciado. Son las más importantes porque son las que el corrector va a buscar primero.

| ID | Requisito no funcional | Origen | Verificación |
|---|---|---|---|
| RNF01 | El texto de un mensaje no puede superar los 140 caracteres. La validación se hace del lado del servidor, no solo en la interfaz. | R01 | Caso de prueba con mensajes de 139, 140 y 141 caracteres, tanto por la web como por la API. |
| RNF02 | El nombre de usuario no puede superar los 15 caracteres. | R03 | Caso de prueba con 15 y 16 caracteres en el registro. |
| RNF03 | El nombre de usuario es único en el sistema. | R03 | Caso de prueba: intentar registrar un nombre de usuario ya existente. |
| RNF04 | La dirección de correo es única y debe tener formato válido. | R03 | Caso de prueba con email duplicado y con email mal formado. |
| RNF05 | Todo mensaje registra obligatoriamente autor y fecha de publicación. | R05 | Inspección del modelo de datos y caso de prueba de publicación. |
| RNF06 | La cantidad de días `n` de los temas del momento debe poder modificarse en tiempo de ejecución, sin recompilar ni volver a desplegar el sistema. | R10 | Caso de prueba: cambiar `n`, recargar el listado y verificar que el resultado cambió. |
| RNF07 | El envío del resumen semanal se ejecuta una vez por semana, en un día y hora configurables. | R14 | Inspección de la configuración del planificador y ejecución manual forzada del proceso. |

---

## 3. Seguridad

| ID | Requisito no funcional | Origen | Verificación |
|---|---|---|---|
| RNF08 | Las claves de los usuarios se almacenan cifradas mediante función de hash con salt. En ningún momento se guardan ni se registran en texto plano. | C17 | Inspección de la base de datos después de un registro. |
| RNF09 | Toda operación del sistema, salvo el registro y el inicio de sesión, requiere una sesión activa. | C17 | Caso de prueba: invocar cada pantalla sin sesión y verificar el rechazo. |
| RNF10 | El sistema verifica del lado del servidor que el usuario sea el autor antes de permitir editar o borrar un mensaje. Ocultar el botón en la interfaz no alcanza. | R13 | Caso de prueba: intentar editar un mensaje ajeno invocando directamente la operación. |
| RNF11 | Un mensaje privado solo es accesible para su autor y su destinatario. No aparece en muros, tablones, búsquedas, temas del momento ni respuestas de la API. | R12, C19 | Caso de prueba con un tercer usuario intentando acceder al mensaje privado. |
| RNF12 | El acceso a la API REST exige una credencial válida y activa de una aplicación registrada. Las credenciales se almacenan cifradas mediante hash. | R17, C25 | Casos de prueba: sin credencial, con credencial inválida y con credencial dada de baja. |
| RNF13 | Las credenciales de acceso al servidor de correo y las claves de firma de sesión se leen de variables de entorno y no se versionan en el repositorio. | Gestión de configuración | Inspección del repositorio: el archivo de entorno debe figurar en `.gitignore` y no debe haber secretos en el historial. |

> **Nota.** RNF13 responde a un problema real encontrado en el repositorio del proyecto de referencia, que tenía credenciales de correo reales versionadas en un repositorio público.

---

## 4. Usabilidad

| ID | Requisito no funcional | Origen | Verificación |
|---|---|---|---|
| RNF14 | El tablón, el muro y las búsquedas muestran los mensajes ordenados del más reciente al más antiguo. | R04 | Inspección visual con un juego de datos de fechas conocidas. |
| RNF15 | Al redactar un mensaje, la interfaz muestra la cantidad de caracteres restantes y bloquea la escritura al llegar a 140. | R01 | Prueba manual sobre el formulario de publicación. |
| RNF16 | Todos los textos de la interfaz y los mensajes de error se presentan en español y describen la causa del error, no un código genérico. | Propio | Revisión de la interfaz. |
| RNF17 | El listado de temas del momento muestra la etiqueta y su cantidad de apariciones, y cada etiqueta es un link al listado de mensajes que la contienen. | R09, R15 | Prueba manual sobre el listado. |
| RNF18 | El sistema es una aplicación web accesible desde navegador de escritorio actualizado. El diseño adaptable a móvil no forma parte del alcance. | Propio | Prueba manual en dos navegadores. |

---

## 5. Rendimiento

Las cifras de esta sección están calibradas contra el juego de datos de prueba del proyecto, no contra un entorno productivo hipotético. No se declara nada que no se vaya a medir.

| ID | Requisito no funcional | Origen | Verificación |
|---|---|---|---|
| RNF19 | Con un juego de datos de 100 usuarios, 1.000 mensajes y 500 relaciones de seguimiento, el tablón de un usuario se muestra en menos de 3 segundos. | Propio | Caso de prueba de rendimiento con el juego de datos cargado y medición del tiempo de respuesta. |
| RNF20 | Con el mismo juego de datos, el cálculo de los temas del momento se resuelve en menos de 3 segundos. | R09 | Medición sobre el mismo juego de datos. |
| RNF21 | El proceso de envío semanal se ejecuta de forma asíncrona y no bloquea el uso normal de la aplicación web mientras corre. | R14 | Caso de prueba: forzar la ejecución del proceso y navegar la aplicación en paralelo. |

---

## 6. Fiabilidad

| ID | Requisito no funcional | Origen | Verificación |
|---|---|---|---|
| RNF22 | Si el envío del email semanal falla para un destinatario, el sistema registra el error en el log y continúa con los destinatarios restantes. | R14 | Caso de prueba con una dirección de correo inválida entre los destinatarios. |
| RNF23 | Las operaciones que afectan a más de una entidad —registrar un usuario, publicar un mensaje con sus etiquetas y menciones, borrar un mensaje con sus republicaciones— son transaccionales: se completan por entero o no dejan datos parciales. | Propio | Caso de prueba forzando un fallo a mitad de la operación y verificando el estado de la base. |
| RNF24 | El sistema registra en un archivo de log los errores no controlados y la ejecución del proceso semanal, con fecha y hora. | Propio | Inspección del archivo de log después de ejecutar el proceso. |

---

## 7. Mantenibilidad y escalabilidad

| ID | Requisito no funcional | Origen | Verificación |
|---|---|---|---|
| RNF25 | El sistema se organiza en capas separadas de presentación, lógica de negocio y persistencia. Ninguna capa de presentación accede directamente a la base de datos. | Propio | Inspección de la estructura del código contra el diagrama de arquitectura. |
| RNF26 | La lógica de extracción de etiquetas, menciones y links reside en un único componente, reutilizado tanto por la aplicación web como por la API REST. | R06, R16 | Inspección del código: una sola implementación referenciada desde ambos puntos de entrada. |
| RNF27 | El código fuente se versiona en un repositorio Git con historial de cambios, en cumplimiento de la gestión de configuración exigida por la cátedra. | Cátedra | Inspección del historial del repositorio. |
| RNF28 | El sistema no contiene valores fijos en el código para los parámetros configurables: la ventana `n`, la frecuencia del envío semanal y los datos de conexión se leen de la configuración. | R10, R14 | Búsqueda de valores fijos en el código. |

---

## 8. Restricciones técnicas

Decisión tomada el 13/09/2026. Criterio: **con cuatro días y una sola persona, no se incorpora ninguna herramienta que no se sepa usar.** Cada elección de esta sección está justificada por experiencia previa disponible, no por preferencia técnica ni por modernidad.

**Esta tecnología debe ser la misma en este documento, en el diagrama de despliegue, en el diagrama de subsistemas, en el plan de pruebas y en el código.** El proyecto de referencia falló en este punto: el texto de arquitectura nombraba una tecnología y el diagrama de despliegue y el plan de pruebas nombraban otra.

| ID | Requisito no funcional | Verificación |
|---|---|---|
| RNF29 | El almacenamiento de datos se realiza sobre una base de datos relacional **SQLite**, mediante el módulo `sqlite3` de la biblioteca estándar de Python. La base reside en un archivo dentro del proyecto, excluido del repositorio. | Inspección del motor en el ambiente de ejecución y del script de creación del esquema. |
| RNF30 | El backend se implementa en **Python 3** con el framework **Flask**. | Inspección del código y del archivo de dependencias: coincide con la tabla de §8.0. |
| RNF31 | El frontend se resuelve con **HTML renderizado en el servidor mediante plantillas Jinja2** y hojas de estilo propias. No se incorpora ningún framework de frontend. La única lógica ejecutada en el navegador es el contador de caracteres del formulario de publicación, escrito en JavaScript sin dependencias. | Inspección del código: ausencia de framework de frontend en el árbol del proyecto y en las dependencias. |
| RNF32 | El envío de correo se realiza contra un servidor SMTP externo; el sistema no implementa entrega de correo propia. **Alcance:** se define en el diseño y no se implementa en esta versión, por corresponder a CU0019, fuera del alcance de realización. | Inspección del documento de arquitectura. Sin caso de prueba asociado en esta versión. |
| RNF33 | La ejecución periódica del proceso semanal se resuelve mediante un planificador de tareas del sistema operativo (**cron**). **Alcance:** se define en el diseño y no se implementa en esta versión, por corresponder a CU0019, fuera del alcance de realización. | Inspección del documento de arquitectura. Sin caso de prueba asociado en esta versión. |
| RNF34 | El sistema se ejecuta y se despliega sobre sistema operativo **Linux**. | Inspección del ambiente de ejecución. |
| RNF40 | El acceso a la base de datos se encapsula en un **módulo de acceso a datos con sentencias SQL parametrizadas**. Ninguna capa superior emite SQL directamente ni concatena valores dentro de una consulta. | Inspección del código: las consultas existen únicamente dentro del módulo de acceso a datos y no hay concatenación de parámetros. |
| RNF41 | La gestión de sesiones y el cifrado de claves utilizan los mecanismos provistos por Flask y su biblioteca base, sin incorporar dependencias adicionales de autenticación. | Inspección del archivo de dependencias. |
| RNF42 | El sistema se ejecuta, para la demostración, sobre el **servidor de desarrollo de Flask en un ambiente local**. No se declara ni se configura un servidor de aplicaciones de producción. | Inspección del procedimiento de ejecución documentado en el README. |

### 8.0 Dependencias declaradas

El archivo `requirements.txt` del repositorio contiene **exactamente** estas dependencias. Cualquier otra que aparezca en el código es una incoherencia entre este documento y el código, y se detecta con la verificación de RNF30 y RNF41.

| Dependencia | Para qué se usa | Requisito que la sostiene | Relación con RNF41 |
|---|---|---|---|
| **Flask** (trae Werkzeug y Jinja2) | Rutas, sesión firmada, servidor de desarrollo, plantillas. Werkzeug provee además el hash de claves (`werkzeug.security`). | RNF30, RNF31, RNF42 | Es el mecanismo que RNF41 nombra |
| **python-dotenv** | Carga el archivo `.env` al arrancar: Flask lo lee solo si esta biblioteca está instalada. Ahí están la clave de firma de sesión y las rutas, fuera del repositorio. | RNF13, RNF28 | **No choca con RNF41.** RNF41 excluye dependencias adicionales **de autenticación** (sesiones y cifrado de claves). `python-dotenv` no autentica, no maneja sesiones ni cifra nada: solo lee variables de entorno de un archivo. |

**Lo que no es dependencia**, porque viene con Python 3: `sqlite3` (RNF29, RNF40), `secrets` y `hashlib` (token de sesión y su hash), `logging` (RNF24), `re` (extracción de etiquetas, menciones y enlaces), `unicodedata` (búsqueda sin acentos) y `smtplib` (previsto para RNF32).

> **Sobre la sesión y RNF41.** Para poder invalidar la sesión del lado del servidor (`rnf 3.1`), el diseño guarda en la base una fila por sesión abierta, con el hash del token. Se construye con Flask y con `secrets`, `hashlib` y `sqlite3` de la biblioteca estándar, así que tampoco agrega dependencias. El detalle está en `DISEÑO_MiBlog.md` §1, hallazgo H1.

*Sección agregada en la versión 1.1, a partir del hallazgo H10 del flujo de Diseño.*

### 8.1 Alternativas evaluadas y descartadas

| Alternativa | Motivo del descarte |
|---|---|
| Framework de frontend (Angular, Astro, React) | Obliga a separar frontend y backend, lo que implica construir puntos de acceso para cada operación en lugar de devolver la página ya armada. Agrega una cadena de compilación y un conjunto de conceptos nuevos. Ninguna de las siete vistas del alcance de esta versión lo justifica. Los diez casos de uso realizados no dan diez vistas: CU0003 es un botón de la barra superior, CU0004 y CU0007 son zonas o controles dentro de la pantalla del tablón, y CU0011 se ejerce desde la pantalla de búsqueda. Las siete son cinco pantallas —inicio de sesión, registro, tablón, búsqueda de usuarios y confirmación de cierre de sesión— y dos diálogos sobre el tablón: edición de un mensaje propio (CU0005) y confirmación de borrado (CU0006). |
| ORM (SQLAlchemy) | Ordenaría el acceso a datos, pero introduce un modelo de trabajo no dominado. El mismo objetivo de separación de capas se cumple con el módulo de acceso a datos de RNF40. |
| Motor de base de datos cliente-servidor (MariaDB, PostgreSQL) | Ambos son conocidos y darían un diagrama de despliegue con el nodo de datos separado del nodo de aplicación. Se descartan porque obligan a instalar y dejar corriendo un servicio adicional, con sus usuarios y credenciales, y porque un fallo de arranque de ese servicio el día de la demostración dejaría al sistema sin funcionar. SQLite cumple igualmente el requisito de base de datos relacional y reduce el ambiente a una sola pieza. |
| Servidor de aplicaciones de producción (Gunicorn, Nginx) | Declararlo sin configurarlo reproduciría la incoherencia entre documentación y código que la cátedra observó en el proyecto de referencia. |

### 8.2 Correspondencia con la arquitectura

Esta decisión determina las capas que debe mostrar el diagrama de arquitectura del flujo de Diseño:

| Capa | Tecnología |
|---|---|
| Presentación | Plantillas Jinja2 y hojas de estilo propias |
| Lógica de negocio | Módulos Python invocados desde las rutas de Flask |
| Acceso a datos | Módulo Python con SQL parametrizado sobre `sqlite3` (RNF40) |
| Persistencia | SQLite (archivo local) |

### 8.3 Consecuencia sobre el diagrama de despliegue

La decisión deja el sistema en **un único nodo de ejecución**: el proceso de Flask y el archivo de la base de datos conviven en la misma máquina. El diagrama de despliegue del flujo de Diseño debe reflejar eso y no inventar un nodo de datos separado.

El correo y el planificador de tareas (RNF32 y RNF33) corresponden a CU0019, que no se realiza en esta versión. En el diagrama de despliegue se representan como elementos previstos y no desplegados, o se omiten; lo que no puede ocurrir es que aparezcan como si estuvieran en funcionamiento.

---

## 9. Requisitos no funcionales de la API REST

Los servicios web de R16 y R17 tienen requisitos propios que conviene aislar, porque son el punto del sistema que consume un tercero.

> **Alcance.** Los cinco requisitos de esta sección corresponden a CU0020 y CU0021, que quedan especificados y diseñados pero **no se implementan** en esta versión. No habrá rutas publicadas, respuestas ni códigos de estado que inspeccionar o probar. Por eso los cinco se verifican por inspección del documento de arquitectura y de diseño, y ninguno tiene caso de prueba asociado, igual que RNF32 y RNF33. La ausencia es deliberada: un requisito no funcional cuya funcionalidad no se implementa no puede tener una prueba que lo verifique.

| ID | Requisito no funcional | Origen | Verificación |
|---|---|---|---|
| RNF35 | La API intercambia datos en formato JSON. **Alcance:** definido en el diseño, no implementado en esta versión. | R16 | Inspección del documento de arquitectura. Sin caso de prueba asociado. |
| RNF36 | La API utiliza los códigos de estado HTTP estándar: éxito, solicitud inválida, no autenticado, no autorizado, recurso inexistente, error interno. **Alcance:** definido en el diseño, no implementado en esta versión. | R16 | Inspección del documento de arquitectura. Sin caso de prueba asociado. |
| RNF37 | La API está versionada en la ruta de acceso, de modo que una versión futura no rompa las aplicaciones ya integradas. **Alcance:** definido en el diseño, no implementado en esta versión. | Propio | Inspección del documento de arquitectura. Sin caso de prueba asociado. |
| RNF38 | La API entrega únicamente mensajes públicos. Nunca expone mensajes privados ni datos sensibles del usuario, como su clave. **Alcance:** definido en el diseño, no implementado en esta versión. | R12, C19 | Inspección del documento de arquitectura. Sin caso de prueba asociado. |
| RNF39 | Existe documentación de la API con los recursos disponibles, sus parámetros, sus respuestas y el mecanismo de autenticación. **Alcance:** definido en el diseño, no implementado en esta versión. | R16 | Inspección del documento de arquitectura. Sin caso de prueba asociado. |

> **Se deja explícitamente fuera de alcance** la limitación de cantidad de llamadas por aplicación (*rate limiting*). Es una buena práctica, pero no está pedida en el enunciado y no se va a implementar ni a probar. Declararla acá sin implementarla sería una incoherencia entre documentos.

---

## 10. Resumen

| Categoría | Cantidad |
|---|---|
| Restricciones del dominio | 7 |
| Seguridad | 6 |
| Usabilidad | 5 |
| Rendimiento | 3 |
| Fiabilidad | 3 |
| Mantenibilidad y escalabilidad | 4 |
| Restricciones técnicas | 9 (decisión tecnológica cerrada) |
| API REST | 5 |
| **Total** | **42** |

De los 42, **35 tienen una forma concreta de verificación definida** y alimentan el plan de pruebas o la inspección del código y del ambiente.

Los **7 restantes** corresponden a casos de uso que quedan especificados y diseñados pero no implementados en esta versión. Se verifican por inspección del documento de arquitectura y no tienen caso de prueba asociado:

| RNF | Caso de uso no realizado |
|---|---|
| RNF32 | CU0019 — Enviar email semanal (servidor SMTP) |
| RNF33 | CU0019 — Enviar email semanal (planificador de tareas) |
| RNF35 a RNF39 | CU0020 y CU0021 — API REST |

Esa ausencia es deliberada y está declarada: un requisito no funcional cuya funcionalidad no se implementa no puede tener una prueba que lo verifique. Lo indefendible sería lo contrario: un plan de pruebas que declare verificar una API que no existe.

### 10.1 Requisitos no funcionales de sistema

Doce requisitos no dependen de ningún caso de uso en particular y no derivan en ningún `rnf` local: RNF18, RNF25, RNF27, RNF29, RNF30, RNF31, RNF32, RNF33, RNF34, RNF40, RNF41 y RNF42. Están declarados como tales en la convención 7 de `ESPECIFICACIONES_CASOS_DE_USO_MiBlog.md`.

---

## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.0 | 13/09/2026 | Requisitos | Versión inicial: RNF01 a RNF42, con la decisión tecnológica de la sección 8. |
| 1.1 | 15/09/2026 | Diseño | Agregados el encabezado de versión y este bloque, que faltaban (hallazgo H12.3). Estado del documento a `[DECIDIDO]`. Nueva §8.0 con las dependencias declaradas: Flask y `python-dotenv`, con el motivo de esta última y por qué no choca con RNF41 (hallazgo H10). Verificación de RNF30 referida a esa tabla. |
