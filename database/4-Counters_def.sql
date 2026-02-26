CREATE TABLE IF NOT EXISTS kpi.counters_def (
  id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  counter_code TEXT NOT NULL,
  counter_name TEXT NOT NULL,
  counter_description TEXT,
  unit TEXT,
  technology_id INTEGER NOT NULL,
  UNIQUE (counter_name, technology_id),
  UNIQUE (counter_code, technology_id),
  FOREIGN KEY (technology_id) REFERENCES kpi.technology(id)
);