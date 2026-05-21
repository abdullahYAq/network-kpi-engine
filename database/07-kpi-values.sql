CREATE TABLE kpi.kpi_values (
    period_start_time TIMESTAMP NOT NULL,
    cell_id INTEGER NOT NULL,
    kpi_id INTEGER NOT NULL,
    kpi_value BIGINT NOT NULL,
    FOREIGN KEY (cell_id) REFERENCES kpi.cells(id),
    FOREIGN KEY (kpi_id) REFERENCES kpi.kpi_def(id),
    PRIMARY KEY (cell_id, period_start_time, kpi_id)
)