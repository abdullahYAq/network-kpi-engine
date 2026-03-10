CREATE TABLE kpi.kpi_def (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    kpi_name TEXT NOT NULL,
    kpi_description TEXT,
    source_type TEXT NOT NULL
         CHECK (source_type IN ('formula', 'system')),
    technology_id INTEGER NOT NULL,
    UNIQUE (kpi_name, technology_id),
    FOREIGN KEY (technology_id) REFERENCES kpi.technology(id)
)