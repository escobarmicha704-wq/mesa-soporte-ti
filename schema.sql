-- Mesa de Soporte TI - Script de creación de base de datos (SQLite)
-- Ejecutar con: sqlite3 mesa.db < schema.sql   (o dejar que app.py lo haga: python app.py --init)

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS historial_cambios;
DROP TABLE IF EXISTS tickets;
DROP TABLE IF EXISTS categorias;
DROP TABLE IF EXISTS usuarios;

-- Responsables (personal de soporte)
CREATE TABLE usuarios (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre  TEXT NOT NULL UNIQUE,
    email   TEXT NOT NULL UNIQUE
);

CREATE TABLE categorias (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre  TEXT NOT NULL UNIQUE
);

CREATE TABLE tickets (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,      -- RF-02 identificador único
    codigo         TEXT NOT NULL UNIQUE,                   -- ej: TCK-0001
    solicitante    TEXT NOT NULL,
    titulo         TEXT NOT NULL,
    descripcion    TEXT NOT NULL,
    categoria_id   INTEGER NOT NULL REFERENCES categorias(id),
    prioridad      TEXT NOT NULL CHECK (prioridad IN ('Baja','Media','Alta','Crítica')),
    estado         TEXT NOT NULL DEFAULT 'Nuevo'
                   CHECK (estado IN ('Nuevo','En proceso','Resuelto','Cerrado')),
    responsable_id INTEGER REFERENCES usuarios(id),
    fecha_creacion TEXT NOT NULL DEFAULT (datetime('now','localtime'))  -- RF-02
);

-- Cambios relevantes (BD-01)
CREATE TABLE historial_cambios (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id   INTEGER NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
    campo       TEXT NOT NULL,
    valor_antes TEXT,
    valor_nuevo TEXT,
    fecha       TEXT NOT NULL DEFAULT (datetime('now','localtime'))
);

CREATE INDEX idx_tickets_estado    ON tickets(estado);
CREATE INDEX idx_tickets_prioridad ON tickets(prioridad);
CREATE INDEX idx_tickets_categoria ON tickets(categoria_id);
