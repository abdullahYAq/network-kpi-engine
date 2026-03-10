CREATE TABLE kpi.counter_values (
    period_start_time TIMESTAMP NOT NULL,
    cell_id INTEGER NOT NULL,
    counter_id INTEGER NOT NULL,
    counter_value BIGINT NOT NULL,
    FOREIGN KEY (cell_id) REFERENCES kpi.cells(id),
    FOREIGN KEY (counter_id) REFERENCES kpi.counters_def(id),
    PRIMARY KEY (cell_id, period_start_time, counter_id)
)