CREATE TABLE IF NOT EXISTS CountrsDef (
    CounterId SERIAL PRIMARY KEY,
    CounterName VARCHAR(255) NOT NULL,
    CounterDescription TEXT
)    