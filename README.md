# MiBlog — Sistema de microblogging interno

Trabajo final de la materia **Ingeniería de Software**. 

MiBlog es una red social interna de una empresa, del tipo *microblogging*: los
empleados publican mensajes de hasta 140 caracteres, siguen a otros empleados y
ven en su tablón lo que publican quienes siguen. Los mensajes admiten etiquetas
`#`, menciones `@` y enlaces, que el sistema reconoce y registra por separado
para poder clasificarlos y buscarlos.

El proyecto se desarrolló siguiendo el **Proceso Unificado**, con sus cinco
flujos de trabajo: Requisitos, Análisis, Diseño, Implementación y Prueba.

---

## Alcance de esta entrega

**21 casos de uso especificados · 10 realizados** (analizados, diseñados,
implementados y probados): CU0001, CU0002, CU0003, CU0004, CU0005, CU0006,
CU0007, CU0009, CU0011 y CU0014. Los once restantes quedan completamente
especificados en el flujo de Requisitos y no forman parte del alcance de
implementación de esta versión.

El recorte es una **decisión propia del alumno** y no está acordado con la
cátedra. El proyecto está planteado para grupos de ocho personas y se cursó en
solitario; según lo que comentaron compañeros de la materia, el mínimo esperado
eran cuatro casos de uso realizados.

---

## Dónde está cada cosa

| Carpeta | Qué contiene |
|---|---|
| `1. Requerimientos/` | Requisitos candidatos, funcionales y no funcionales · actores · catálogo y especificación de los 21 casos de uso · modelo de dominio · diagrama único de casos de uso · prototipo de interfaces |
| `2. Análisis/` | Clases de análisis · diagrama de clases · diagrama de paquetes · diagramas de colaboración de los 10 casos de uso realizados |
| `3. Diseño/` | Arquitectura en capas y mecanismos de diseño · diagrama de clases de diseño integral con los cuatro patrones · despliegue · subsistemas · diagramas de secuencia · diagramas de estado |
| `4. Implementacion/codigo/` | El código fuente del sistema, con su propio `README.md` |
| `5. Pruebas/` | Plan de pruebas, casos de prueba y procedimientos de prueba |
| `docs/` | Los mismos documentos en markdown. **se encuentran en la rama docs-proyecto**|

---

## Sobre la carpeta `docs/`

Los entregables de la materia son los archivos **`.docx`, `.pdf` y `.png`** que
están en las cinco carpetas de etapa. La carpeta `docs/` contiene los **once
documentos en markdown** a partir de los cuales se redactaron.

**Cuando un documento de `docs/` y su entregable difieren, manda el
entregable de la carpeta de etapa.**

Los markdown están en el repositorio por dos razones: llevan el control de
versiones del proyecto (encabezado de versión y bloque de control en cada
uno, según la convención de `docs/00_INDICE.md` §7, que es lo que pide el
RNF27 de gestión de configuración), y se leen sin convertir, lo que hace más
simple retomar el trabajo.

`docs/00_INDICE.md` es el punto de entrada: dice qué contiene cada documento y
en qué versión está.

> **Nota temporal.** La carpeta `docs/` vive hoy en la rama **`docs-proyecto`**
> y todavía no está integrada a la rama principal. Para verla:
> `git switch docs-proyecto`. **Este párrafo se borra cuando la rama se
> integre**, que es lo que corresponde antes de la entrega: un repositorio
> entregado cuya rama principal no incluye la documentación obliga a quien lo
> clona a saber que hay otra rama donde buscarla.

---

## Cómo ejecutar el sistema

Las instrucciones completas, dependencias, creación de la base de
datos, datos de demostración y ejecución de las pruebas— están en
`4. Implementacion/codigo/README.md`.

En resumen: **Python 3 · Flask · plantillas Jinja2 · hojas de estilo propias ·
SQLite mediante `sqlite3` · Linux.** Sin ORM, sin framework de frontend y sin
servidor de aplicaciones de producción. Las únicas dos dependencias declaradas
son **Flask** y **python-dotenv**, y el motivo de cada una está en
`docs/REQUISITOS_NO_FUNCIONALES_MiBlog.md` §8.0.

El sistema se ejecuta sobre el servidor de desarrollo de Flask en un ambiente
local, para la demostración (RNF42).

---

## Nota sobre secretos

La clave de firma de sesión y las rutas configurables se leen de un archivo
`.env` que **no está en el repositorio** (RNF13). La plantilla sin valores
secretos es `.env.example`. Tampoco se versionan la base de datos, el archivo
de registro ni las fotos de perfil que suben los usuarios.