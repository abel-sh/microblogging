# 00 — ÍNDICE DEL PROYECTO (leer primero)
 
**Versión:** 1.15 · **Última modificación:** 28/10/2026 · **Etapa:** Gestión del proyecto
 
**Materia:** Ingeniería de Software · **Alumno:** Abel · **Mi proyecto:** sistema de **microblogging**
**Fecha de entrega y defensa:** 24/11/2026
 
---
 
## 1. Regla de oro
 
En la raíz de este proyecto conviven **dos cosas distintas**:
 
| | Qué es | Archivos |
|---|---|---|
| **MI PROYECTO** | Sistema de **microblogging** (mensajes ≤140 caracteres, seguidores, `#etiquetas`, `@menciones`, temas del momento, email semanal, API REST) | `enunciado_microblogging.pdf`, `ESTADO_MI_PROYECTO.md` |
| **REFERENCIA AJENA** | **UMBook**, proyecto ya aprobado de un compañero, con **otro enunciado** (red social tipo Facebook: amigos, álbumes, fotos, muro, cumpleaños) | Todos los `CU00xx`, diagramas, arquitectura, pruebas, correcciones, el enunciado 2022 y los repos de GitHub |
| **TEORÍA** | Resúmenes de la materia (Proceso Unificado, Pressman, SCRUM, calidad, métricas) | 7 PDF de resúmenes |
 
**UMBook sirve como molde de formato, rúbrica y nivel de detalle esperado. Nunca como contenido de mi proyecto.**
No mezclar: mi dominio no tiene amigos, álbumes, fotos ni cumpleaños; tiene seguidores, mensajes y etiquetas.
 
---
 
## 2. Advertencias técnicas de los archivos
 
1. **Los `.pdf` de la raíz NO son PDF.** Son archivos **ZIP** con `N.jpeg` + `N.txt` por página y un `manifest.json`.
   - `pdftotext` / `pdfinfo` / `pypdf` **fallan**.
   - Leer así: `unzip -o archivo.pdf -d destino/` y luego los `.txt` **ordenados numéricamente** (1, 2, 3… no alfabéticamente).
   - Si `manifest.json` dice `has_visual_content: true` en una página, ahí hay un diagrama → ver el `.jpeg`.
2. **`EJEMPLO.docx` no es un Word.** Es texto plano con tablas Markdown: es la **plantilla de casos de uso de la cátedra**. Se lee con `cat`.
3. **`Modelo_de_Dominio.pdf`** no tiene capa de texto: es solo imagen.
4. Los nombres tienen `_` en lugar de espacios y `___` donde iba un guión largo (ej. `CASO_DE_USO_CU0007___COMENTAR_PUBLICACIÓN.pdf`).
5. **`estructura_proyecto_aprobado.txt`** reconstruye las carpetas originales de UMBook (Requerimientos / Análisis / Diseño / Pruebas), porque los archivos se subieron sueltos.
---
 
## 3. Dónde buscar cada cosa
 
El análisis completo está en **`INFORME_CONTEXTO_PROYECTO.md`** (16 secciones). Atajos:
 
| Necesito… | Ir a |
|---|---|
| **Qué se construyó de verdad, qué se decidió al programar y qué quedó abierto** | **`CONTEXTO_IMPLEMENTACION_MiBlog.md`** |
| Correr el programa, correr las pruebas automáticas o llenar la base con datos de demostración | `CONTEXTO_IMPLEMENTACION_MiBlog.md` §2 (comandos) y §7 (comprobación rápida). El `README.md` de `4. Implementacion/codigo/` lo explica completo |
| Mi enunciado desglosado en requisitos R00–R17 | Informe §3 · y `ESTADO_MI_PROYECTO.md` §2 |
| Qué exige la cátedra (checklist real de entregables) | Informe §5 |
| La plantilla de especificación de casos de uso | Informe §6.1 · archivo `EJEMPLO.docx` |
| Ejemplos de casos de uso ya escritos (18 fichas) | Informe §6.3 |
| Modelo de dominio de ejemplo | Informe §6.4 |
| Diagrama de paquetes y de colaboración | Informe §7.1–7.2 |
| Documento de requisitos no funcionales | Informe §7.3 |
| Arquitectura, capas, mecanismos y los 5 patrones GoF | Informe §8 |
| Despliegue, subsistemas, secuencia, estados | Informe §8.5–8.8 |
| Plan de pruebas, casos y procedimientos | Informe §9 |
| Cómo implementaron el código (Flask + Angular) | Informe §10 |
| Qué contiene cada resumen de teoría y en qué página | Informe §11 (y §11.8 para elegir cuál abrir) |
| Mapa entregable → ejemplo → teoría | Informe §12 |
| Qué reutilizar y qué NO para microblogging | Informe §13 |
| Errores del proyecto ajeno que no hay que repetir | Informe §6.7 y §13.4 |
| Límites de este informe / qué verificar | Informe §14 |
 
### 3.1 Documentos propios del proyecto MiBlog
 
Son los que se entregan. El informe de contexto y los archivos de UMBook no se entregan: son insumo.
 
| Documento | Flujo del PU | Versión | Qué contiene |
|---|---|---|---|
| `REQUISITOS_CANDIDATOS_MiBlog.md` | Requisitos | 1.1 | C01–C38, características evaluadas. La 1.1 agregó el encabezado y el bloque de control, y pasó el estado a `[DECIDIDO]` |
| `REQUISITOS_FUNCIONALES_MiBlog.md` | Requisitos | 1.1 | RF01–RF21 y reglas automáticas RA01–RA11. La 1.1 agregó el encabezado y el bloque de control, y pasó el estado a `[DECIDIDO]` |
| `REQUISITOS_NO_FUNCIONALES_MiBlog.md` | Requisitos | 1.1 | RNF01–RNF42 y las dependencias declaradas del código (§8.0) |
| `DIA1_REQUISITOS_MiBlog.md` | Requisitos | 1.2 | Actores, catálogo de 21 CU priorizado, modelo de dominio, diagrama único de casos de uso, alcance de la iteración. La 1.1 agregó el encabezado y el bloque de control y corrigió la afirmación falsa sobre la cátedra: la §7.0 declara el recorte como decisión propia del alumno. La 1.2 pasó a `[DECIDIDO]` las §2, §3, §4, §5 y §7, que seguían diciendo `[PROPUESTA]` con todo el proyecto construido sobre ellas |
| `ESPECIFICACIONES_CASOS_DE_USO_MiBlog.md` | Requisitos | 1.3 | Los 21 casos de uso con la plantilla de la cátedra. La 1.3 documenta la forma admitida del nombre de usuario (`{Ob 1.3}`) y apunta a las pantallas del prototipo |
| `Prototipo de Interfaces.pdf` | Requisitos | — | Las vistas de la aplicación, actualizadas el 28/10/2026 al diseño visual implementado. **Fija qué elementos tiene cada vista y cómo se navega**; lo que el diseño visual trae de más no se programa, ver `PLAN_DEL_PROYECTO.md` §ETAPA 4 |
| `ANALISIS_MiBlog.md` | Análisis | 2.2 | 23 clases de análisis, diagrama de clases, diagrama de paquetes, los 10 diagramas de colaboración con mensajes numerados, y la evaluación de patrones de diseño con anclaje real |
| `DISEÑO_MiBlog.md` | Diseño | 1.4 | Arquitectura en cuatro capas con rutas, esquema SQL y tabla de mecanismos · diagrama de clases de diseño **integral** con los cuatro patrones · despliegue · subsistemas en capas · las 10 secuencias con fragmentos `alt` · estados de `Mensaje` y `Usuario` · doce hallazgos · teoría del flujo de Diseño. La 1.3 corrigió la §2.4 por la estructura real del repositorio y la 1.4 pasó al diseño los desvíos DV-4 a DV-8 (`CONTEXTO_IMPLEMENTACION_MiBlog.md` §6.1) |
| `CONTEXTO_IMPLEMENTACION_MiBlog.md` | Implementación | 1.9 | **Documento de traspaso entre los seis bloques de la Etapa 4 (cerrada el 28/10/2026):** repositorio real, estado por bloque, lo que existe en el código, decisiones D-xx, desvíos DV-x respecto del diseño, pendientes, comprobaciones, protocolo de cierre e informes de cierre. La Etapa 5 lo lee |
| `ESTADO_MI_PROYECTO.md` | Gestión del proyecto | 1.13 | Documento vivo: decisiones, estado de los entregables, bitácora |
| `PLAN_DEL_PROYECTO.md` | Gestión del proyecto | 1.15 | Las cinco etapas con sus prompts, alcance, riesgos, preguntas de defensa |
| `00_INDICE.md` | Gestión del proyecto | 1.15 | Este archivo |
 
**Los once documentos propios cumplen la regla de control de versiones de la §7**, desde el 28/10/2026: `REQUISITOS_CANDIDATOS`, `REQUISITOS_FUNCIONALES` y `DIA1_REQUISITOS` eran los tres que no la cumplían y pasaron a 1.1. Las correcciones que pidió el Diseño están aplicadas; el detalle, en `ESTADO_MI_PROYECTO.md` §7.

**Ningún documento propio afirma que la cátedra haya acordado el alcance reducido.** No se conversó con la cátedra: el recorte es una decisión propia del alumno y así está declarado en `DIA1_REQUISITOS_MiBlog.md` §7.0, `PLAN_DEL_PROYECTO.md` §7 riesgo 3, `ESTADO_MI_PROYECTO.md` §1 y `CONTEXTO_IMPLEMENTACION_MiBlog.md` P-5. Si en algún documento vuelve a aparecer la afirmación contraria, es un resto de las versiones anteriores al 28/10/2026 y hay que corregirlo.
 
### 3.2 Diagramas de Diseño
 
El **código PlantUML de los 17 diagramas está dentro de `DISEÑO_MiBlog.md`**, que es la fuente. Las imágenes `.png` generadas **viven en la carpeta `diagramas_diseno/` de la entrega a la cátedra, no en este Project**: no aportan nada a los chats, porque el PlantUML ya está en el documento.
 
| Imagen de la entrega | Diagrama |
|---|---|
| `capas.png` | Arquitectura en capas |
| `clases.png` | Clases de diseño integral |
| `despliegue.png` | Despliegue |
| `subsistemas_metasistema.png` | **Subsistemas, el que se entrega**: paquetes anidados por capa |
| `subsistemas.png` | Subsistemas en las cuatro capas del PU, vista complementaria |
| `cu0001.png` … `cu0014.png` | Las 10 secuencias |
| `estado_mensaje.png`, `estado_usuario.png` | Estados |
 
**Advertencia:** el diagrama de clases mide casi 5000 píxeles de ancho. En `plantuml.com` hay que pedirlo como **SVG**, porque la salida PNG del servidor recorta las imágenes grandes. Localmente: `java -DPLANTUML_LIMIT_SIZE=16384 -jar plantuml.jar clases.puml`. **El diagrama de clases cambió en la versión 1.4 del diseño** (miembros de apoyo y la nota N4): la imagen `clases.png` de la entrega hay que regenerarla (P-18 del documento de contexto).
 
---
 
## 4. Estado de mi proyecto
 
Vive en **`ESTADO_MI_PROYECTO.md`** (decisiones y entregables) y, para la Etapa 4, en **`CONTEXTO_IMPLEMENTACION_MiBlog.md`** (qué se construyó y qué se decidió al programar).
Cualquier chat que vaya a producir un artefacto **debe leerlos antes**, para no re-decidir lo ya decidido ni inventar decisiones que no tomé. **Un chat de Implementación o de Prueba lee primero este índice y después el documento de contexto.**
 
**Dónde estoy:** Requerimientos, Análisis, Diseño e **Implementación** cerrados. La **Etapa 4** se cerró el 28/10 con el bloque 4.6 (cierre del código): los seis bloques —4.1 cimientos (24/10), 4.2 sesión (24/10), 4.3 relaciones (26/10), 4.4 mensajes y tablón (27/10), 4.5 edición y republicación (27/10) y 4.6 cierre del código (28/10)— están cerrados. Ya se puede registrar una cuenta, entrar, salir, buscar a un usuario y seguirlo, publicar un mensaje con `#etiquetas`, `@menciones` y enlaces, verlo en el tablón junto con los de quienes se sigue, y editar, borrar y republicar (los 10 casos de uso funcionan); los errores muestran una página y quedan anotados en `instance/miblog.log`. La carpeta `4. Implementacion/codigo/` trae un `README.md` completo, `sembrar_datos.py` (datos de demostración) y `pruebas/` con 262 pruebas automáticas. **Sigue la Etapa 5, Prueba**, solo sobre los 10 casos de uso realizados (su prompt está en `PLAN_DEL_PROYECTO.md`).
 
**La Implementación se hizo en chats de este proyecto, no en Claude Code**, para poder explicar el código en la defensa. Fueron **seis bloques**, cada uno en su chat y cada uno terminando en algo que se podía correr: cimientos · sesión · relaciones · mensajes y tablón · edición y republicación · cierre del código. Los prompts y el informe de cierre de cada bloque están en la Etapa 4 de `PLAN_DEL_PROYECTO.md`. **Cada chat dejó lo que decidió en el documento de contexto, y el siguiente lo leyó**: así se transmitió el estado de un bloque al otro.
 
---
 
## 5. Cosas que la cátedra marcó FALTA en el proyecto ajeno (y que igual aprobó)
 
Que estén así en el ejemplo **no significa que se puedan omitir**:
 
- Diagrama de casos de uso **único para toda la aplicación** (el compañero hizo uno por caso de uso → marcado FALTA dos veces).
- Listado de requisitos no funcionales dentro del flujo de **Requerimientos**.
- Diagrama de **clases de diseño integral** con los patrones embebidos (había uno por patrón, aislados). → En MiBlog: `DISEÑO_MiBlog.md` §3, uno solo.
- Casos y procedimientos de prueba **completos**.
---
 
## 6. Advertencia de seguridad sobre los repos ajenos
 
`final-software/backend/test_smtp.py` tiene credenciales reales de Gmail commiteadas en un repo público. No copiar ese archivo ni ese patrón. En mi proyecto: todo secreto va en `.env` y `.env` va en `.gitignore`.
 
---
 
## 7. Control de versiones de los documentos
 
Es un requisito de gestión de configuración de la cátedra y aplica a **todos** los documentos propios de la §3.1.
 
**Encabezado**, debajo del título:
 
```
**Versión:** X.Y · **Última modificación:** DD/MM/AAAA · **Etapa:** <flujo del PU>
```
 
**Bloque de cierre**, al final:
 
```
## Control del documento
 
| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.0 | DD/MM/AAAA | <flujo del PU> | Versión inicial |
```
 
**Reglas:**
 
- Una fila **por cambio con contenido**. Una corrección de tipeo no genera fila ni sube la versión.
- Se conservan **como máximo las últimas cuatro filas**.
- **X.1, X.2…** para cambios menores. **X.0** para cambios de alcance o decisiones estructurales.
- En **Etapa / Chat** va el flujo del Proceso Unificado: Requisitos, Análisis, Diseño, Implementación, Prueba, o **Gestión del proyecto** para el índice, el plan y el estado.
La tabla de disparadores —qué evento obliga a actualizar qué documento— está en `ANALISIS_MiBlog.md` §7.4.
 
---
 
## Control del documento
 
| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.12 | 27/10/2026 | Gestión del proyecto | **Bloque 4.4 cerrado.** CONTEXTO a 1.6, ESTADO a 1.10 y PLAN a 1.12. §3: fila nueva para correr el programa, las pruebas y los datos de demostración. §4: dónde estoy (7 de 10 casos de uso funcionando; sigue el 4.5; la carpeta `codigo/` trae README completo, `sembrar_datos.py` y 83 pruebas). |
| 1.13 | 27/10/2026 | Gestión del proyecto | **Bloque 4.5 cerrado.** CONTEXTO a 1.7, ESTADO a 1.11 y PLAN a 1.13. §4: dónde estoy (los 10 casos de uso funcionan; sigue el 4.6; la carpeta `codigo/` trae 183 pruebas). |
| 1.14 | 28/10/2026 | Gestión del proyecto | **Bloque 4.6 cerrado; Etapa 4 (Implementación) cerrada.** DISEÑO a 1.4, ESPECIFICACIONES a 1.3, CONTEXTO a 1.8, ESTADO a 1.12 y PLAN a 1.14. §3.1: versiones y descripción del diseño, las especificaciones y el prototipo (actualizado al diseño visual implementado). §3.2: la imagen del diagrama de clases hay que regenerarla. §4: dónde estoy (Implementación cerrada, 262 pruebas; sigue la Etapa 5). |
| 1.15 | 28/10/2026 | Gestión del proyecto | **Verificación del juego de documentos que va al repositorio, y corrección de dos afirmaciones falsas.** PLAN a 1.15 y ESTADO a 1.13: ninguno afirma más que el alcance reducido esté acordado con la cátedra, porque no lo está. §3.1: los documentos sin encabezado de versión ni bloque de control son tres y no uno (`DIA1_REQUISITOS`, `REQUISITOS_CANDIDATOS` y `REQUISITOS_FUNCIONALES`), los dos últimos además con el estado `[PROPUESTA]`; y se señala que `DIA1_REQUISITOS` todavía afirma el acuerdo con la cátedra en tres secciones. CONTEXTO a 1.9 por la misma corrección en su P-5, su P-6 y su P-19, hecha por el chat de coordinación porque la Etapa 4 está cerrada y sus seis chats de bloque ya no tienen dueño asignado. **El P-6 queda cerrado en su parte de encabezados:** `REQUISITOS_CANDIDATOS` y `REQUISITOS_FUNCIONALES` pasan a 1.1 con encabezado, bloque de control y estado `[DECIDIDO]`, y `DIA1_REQUISITOS` pasa a 1.1 con lo mismo más la corrección de la afirmación sobre la cátedra en sus §1.1, §7, §8 y §9, y a 1.2 con sus §2, §3, §4, §5 y §7 en `[DECIDIDO]`. Los once documentos propios cumplen ya la regla de control de versiones de la §7, y **ninguno conserva una marca `[PROPUESTA]` que contradiga el estado real del proyecto.** |
