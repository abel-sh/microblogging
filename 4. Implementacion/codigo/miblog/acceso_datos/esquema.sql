-- Esquema de la base de MiBlog.
-- Se ejecuta una sola vez con:  flask --app miblog iniciar-bd

CREATE TABLE usuarios (
  id_usuario       INTEGER PRIMARY KEY,
  nombre_usuario   TEXT NOT NULL UNIQUE COLLATE NOCASE,
  email            TEXT NOT NULL UNIQUE COLLATE NOCASE,
  clave_hash       TEXT NOT NULL,
  nombre_completo  TEXT NOT NULL,
  descripcion      TEXT,
  url_foto         TEXT,
  rol              TEXT NOT NULL DEFAULT 'EMPLEADO' CHECK (rol IN ('EMPLEADO', 'ADMINISTRADOR')),
  fecha_alta       TEXT NOT NULL,
  activo           INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0, 1))
);

-- Tabla técnica (H1). No tiene clase de dominio.
CREATE TABLE sesiones (
  hash_token        TEXT PRIMARY KEY,
  id_usuario        INTEGER NOT NULL REFERENCES usuarios (id_usuario),
  fecha_expiracion  TEXT NOT NULL
);

CREATE TABLE seguimientos (
  id_seguidor   INTEGER NOT NULL REFERENCES usuarios (id_usuario),
  id_seguido    INTEGER NOT NULL REFERENCES usuarios (id_usuario),
  fecha_inicio  TEXT NOT NULL,
  PRIMARY KEY (id_seguidor, id_seguido),          
  CHECK (id_seguidor <> id_seguido)               
);

CREATE TABLE mensajes (
  id_mensaje            INTEGER PRIMARY KEY,
  id_autor              INTEGER NOT NULL REFERENCES usuarios (id_usuario),   -- RNF05
  texto                 TEXT NOT NULL,
  fecha_publicacion     TEXT NOT NULL,                                       -- RNF05
  fecha_ultima_edicion  TEXT,
  editado               INTEGER NOT NULL DEFAULT 0 CHECK (editado IN (0, 1)),
  origen                TEXT NOT NULL CHECK (origen IN ('WEB', 'API')),       -- rnf 4.5
  CHECK ((editado = 0 AND fecha_ultima_edicion IS NULL)
      OR (editado = 1 AND fecha_ultima_edicion IS NOT NULL))               -- diagrama 7.1
);

CREATE TABLE republicaciones (
  id_republicacion     INTEGER PRIMARY KEY,
  id_usuario           INTEGER NOT NULL REFERENCES usuarios (id_usuario),
  id_mensaje           INTEGER NOT NULL REFERENCES mensajes (id_mensaje),     
  fecha_republicacion  TEXT NOT NULL,
  UNIQUE (id_usuario, id_mensaje)                                            -- ca 7.3
);

CREATE TABLE etiquetas (
  id_etiqueta  INTEGER PRIMARY KEY,
  nombre       TEXT NOT NULL UNIQUE
);

CREATE TABLE mensaje_etiqueta (
  id_mensaje   INTEGER NOT NULL REFERENCES mensajes (id_mensaje),
  id_etiqueta  INTEGER NOT NULL REFERENCES etiquetas (id_etiqueta),
  PRIMARY KEY (id_mensaje, id_etiqueta)
);

CREATE TABLE menciones (
  id_mencion             INTEGER PRIMARY KEY,
  id_mensaje             INTEGER NOT NULL REFERENCES mensajes (id_mensaje),
  id_usuario_mencionado  INTEGER NOT NULL REFERENCES usuarios (id_usuario),
  posicion_en_texto      INTEGER NOT NULL
);

CREATE TABLE enlaces (
  id_enlace   INTEGER PRIMARY KEY,
  id_mensaje  INTEGER NOT NULL REFERENCES mensajes (id_mensaje),
  url         TEXT NOT NULL
);

CREATE INDEX ix_mensajes_autor           ON mensajes (id_autor);
CREATE INDEX ix_republicaciones_usuario  ON republicaciones (id_usuario);
CREATE INDEX ix_seguimientos_seguido     ON seguimientos (id_seguido);