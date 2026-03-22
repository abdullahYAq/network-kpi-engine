from psycopg2 import connect, extras
import pandas as pd
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
def insert_counters_to_db(df,db_config):
    tech_map = {"LTE":1,"UMTS":2,"GSM":3,"NSANR":0}
    df_copy = df
    df_copy["tech_name"] = df_copy["tech_name"].map(tech_map)
    df_reordered = df[["counter_code", "counter_name", "counter_description", "unit", "tech_name"]]
    counters_tuple = list(df_reordered.itertuples(index=False,name=None))
    with connect(**db_config) as conn:
        with conn.cursor() as cur:
            sql='''
                INSERT INTO kpi.counters_def
                (counter_code, counter_name, counter_description, unit, tech_id)
                VALUES %s
                RETURNING counter_code
            '''
            inserted_counters = extras.execute_values(cur,sql,counters_tuple, fetch=True)
            return len(inserted_counters)