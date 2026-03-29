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
        raise e