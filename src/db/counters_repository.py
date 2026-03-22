from psycopg2 import connect, extras
def get_all_counter_codes(db_config):
    with connect(**db_config) as conn:
        with conn.cursor() as cur:
            sql = '''
                SELECT counter_code 
                FROM kpi.counters_def
            '''
            cur.execute(sql)
            codes_db = cur.fetchall()
            return codes_db
def insert_counters_to_db(excel_path,db_config):
    with connect(**db_config) as conn:
        with conn.cursor() as cur:
            sql='''

            '''
            
            pass