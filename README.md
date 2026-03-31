# Network KPI Engine

## Overview

A modular data pipeline for telecom network automation, focused on ingesting and processing network counters and KPI-related data.

---

## Features

### Counters Pipeline

* Detect counters from raw data
* Compare with database records
* Insert new counters

### Counter Values Ingestion

* Transform data from wide to long format
* Map counters and cells to database IDs
* Normalize timestamp format
* Export data to CSV
* Bulk insert using PostgreSQL COPY

---

## Tech Stack

* Python (pandas)
* PostgreSQL
* psycopg2

---

## Project Structure

* ingestion/
* db/
* validation/
* main.py

---

## Status

* Counters pipeline: Completed
* Counter values ingestion: Implemented
* KPI calculations: In progress
