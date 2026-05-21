from psycopg2 import connect, extras
def insert_counter_values_to_db(csv_path,db_config):
    try:
        with connect(**db_config) as conn:
            with conn.cursor() as cur:
                sql = '''
                        COPY kpi.counter_values (period_start_time, cell_id, counter_id, counter_value)
                        FROM STDIN WITH CSV HEADER DELIMITER AS ','
                    '''
                # Execute the SQL statement csv file using copy_from for efficient bulk insert
                with open(csv_path, 'r', encoding='utf-8') as f:
                    cur.copy_expert(sql, f)
    except Exception as e:
        print(f"Error occurred while inserting counter values to DB: {e}")
        print("Failed to insert counter values into the database.")
def insert_kpi_values_to_db(csv_path,db_config):
    try:
        with connect(**db_config) as conn:
            with conn.cursor() as cur:
                sql = '''
                        COPY kpi.kpi_values (period_start_time, cell_id, kpi_id, kpi_value)
                        FROM STDIN WITH CSV HEADER DELIMITER AS ','
                    '''
                # Execute the SQL statement csv file using copy_from for efficient bulk insert
                with open(csv_path, 'r', encoding='utf-8') as f:
                    cur.copy_expert(sql, f)
    except Exception as e:
        print(f"Error occurred while inserting kpi values to DB: {e}")
        print("Failed to insert kpi values into the database.")        
def get_kpi_id_kpi_name_map(db_config):
    try:
        with connect(**db_config) as conn:
            with conn.cursor(cursor_factory=extras.DictCursor) as cur:
                cur.execute("SELECT kpi_id, kpi_name FROM kpi.kpi_definitions")
                rows = cur.fetchall()
                kpi_id_kpi_name_map = {row['kpi_name']: row['kpi_id'] for row in rows}
                return kpi_id_kpi_name_map
    except Exception as e:
        print(f"Error occurred while fetching KPI ID to KPI Name map: {e}")
        return {}        