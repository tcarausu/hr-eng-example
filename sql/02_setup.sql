\c openmind;

-- -----------------------------
-- Schema
-- -----------------------------
CREATE SCHEMA IF NOT EXISTS openmind_ext AUTHORIZATION openmind_user;

-- -----------------------------
-- Tables
-- -----------------------------
CREATE TABLE IF NOT EXISTS openmind_ext.orders (
                                                   name TEXT PRIMARY KEY,
                                                   source TEXT NOT NULL,
                                                   target TEXT NOT NULL,
                                                   status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS openmind_ext.robots (
                                                   name TEXT PRIMARY KEY,
                                                   status TEXT NOT NULL,
                                                   node TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS openmind_ext.routes (
                                                   id BIGSERIAL PRIMARY KEY,
                                                   robot TEXT NOT NULL REFERENCES openmind_ext.robots(name),
                                                   "order" TEXT NOT NULL REFERENCES openmind_ext.orders(name),
                                                   path TEXT NOT NULL -- will store JSON list of nodes
);

CREATE TABLE IF NOT EXISTS openmind_ext.audit_events (
                                                         id BIGSERIAL PRIMARY KEY,
                                                         timestamp TIMESTAMPTZ NOT NULL DEFAULT now(),
                                                         type TEXT NOT NULL,
                                                         details JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS openmind_ext.graph_nodes (
                                                        id TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS openmind_ext.graph_edges (
                                                        id BIGSERIAL PRIMARY KEY,
                                                        from_node TEXT NOT NULL REFERENCES openmind_ext.graph_nodes(id),
                                                        to_node TEXT NOT NULL REFERENCES openmind_ext.graph_nodes(id),
                                                        weight DOUBLE PRECISION DEFAULT 1.0
);

-- -----------------------------
-- Ownership & Grants
-- -----------------------------
ALTER TABLE openmind_ext.orders OWNER TO openmind_user;
ALTER TABLE openmind_ext.robots OWNER TO openmind_user;
ALTER TABLE openmind_ext.routes OWNER TO openmind_user;
ALTER TABLE openmind_ext.audit_events OWNER TO openmind_user;
ALTER TABLE openmind_ext.graph_nodes OWNER TO openmind_user;
ALTER TABLE openmind_ext.graph_edges OWNER TO openmind_user;

GRANT USAGE ON SCHEMA openmind_ext TO openmind_user;
GRANT INSERT, SELECT, UPDATE, DELETE ON ALL TABLES IN SCHEMA openmind_ext TO openmind_user;

-- -----------------------------
-- Seed Data
-- -----------------------------
-- Robots
INSERT INTO openmind_ext.robots (name, status, node) VALUES
                                                         ('R1', 'IDLE', 'A'),
                                                         ('R2', 'EXECUTING', 'C'),
                                                         ('R3', 'IDLE', 'E')
ON CONFLICT (name) DO NOTHING;

-- Orders
INSERT INTO openmind_ext.orders (name, source, target, status) VALUES
    ('O-1001', 'B', 'D', 'NEW')
ON CONFLICT (name) DO NOTHING;

-- Graph nodes
INSERT INTO openmind_ext.graph_nodes (id) VALUES
                                              ('A'), ('B'), ('C'), ('D'), ('E'), ('F')
ON CONFLICT (id) DO NOTHING;

-- Graph edges
INSERT INTO openmind_ext.graph_edges (from_node, to_node, weight) VALUES
                                                                      ('A', 'B', 1),
                                                                      ('B', 'C', 2),
                                                                      ('C', 'D', 2),
                                                                      ('B', 'E', 3),
                                                                      ('E', 'F', 1),
                                                                      ('D', 'F', 2)
ON CONFLICT DO NOTHING;
