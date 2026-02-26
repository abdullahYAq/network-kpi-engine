CREATE TABLE IF NOT EXISTS kpi.cells (
  id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  cell_code TEXT NOT NULL,
  lncel_name TEXT NOT NULL,
  dn_cell_name TEXT NOT NULL,
  site_id INTEGER NOT NULL,
  technology_id INTEGER NOT NULL,
  UNIQUE (cell_code, site_id),
  FOREIGN KEY (site_id) REFERENCES kpi.sites(id),
  FOREIGN KEY (technology_id) REFERENCES kpi.technology(id)
);