from psycopg2 import connect, extras
import pandas as pd
def get_counter_id_counter_code_map(db_config):
    with connect(**db_config) as conn:
        with conn.cursor() as cur:
            sql = '''
                SELECT counter_code ,id
                FROM kpi.counters_def
            ''' 
            cur.execute(sql)
            codes_id_db = cur.fetchall()
            if not codes_id_db:
                 return {}
            codes = [i[0] for i in codes_id_db]

            if len(codes) != len(set(codes)):
                raise ValueError("Duplicate counter_code detected in DB")
            counters_map = {
                i[0].strip().upper() : i[1]
                for i in codes_id_db
            }
            return counters_map
def get_all_counter_codes(db_config):
    with connect(**db_config) as conn:
        with conn.cursor() as cur:
            sql = '''
                SELECT counter_code 
                FROM kpi.counters_def
            '''
            cur.execute(sql)
            codes_db = cur.fetchall()
            codes_db_list = [i[0] for i in codes_db]
            return codes_db_list
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
def get_raw_counters_values_df(db_config,counters_list,start_time,end_time,lncel_list):
    with connect(**db_config) as conn:
        with conn.cursor() as cur:
            sql = '''
                SELECT cv.period_start_time, c.lncel, cd.counter_name, cv.counter_value
                FROM kpi.counter_values cv
                JOIN kpi.counters_def cd ON cv.counter_id = cd.id
                JOIN kpi.cells c ON cv.cell_id = c.id
                WHERE cd.counter_code IN %s
                AND cv.period_start_time BETWEEN %s AND %s
                AND c.lncel IN %s
                
            '''
            cur.execute(sql, (tuple(counters_list), start_time, end_time, tuple(lncel_list)))
            counters_db = cur.fetchall()
            values_df = pd.DataFrame(counters_db, columns=["period_start_time", "lncel","counter_name" , "counter_value"])

            return values_df
def get_daily_counters_values_df(db_config,counters_list,start_time,end_time,lncel_list):
    with connect(**db_config) as conn:
        with conn.cursor() as cur:
            sql = '''
                SELECT cvd.period_start_time, c.lncel, cd.counter_name, cvd.counter_value
                FROM kpi.counter_values_daily cvd
                JOIN kpi.counters_def cd ON cvd.counter_id = cd.id
                JOIN kpi.cells c ON cvd.cell_id = c.id
                WHERE cd.counter_code IN %s
                AND cvd.period_start_time BETWEEN %s AND %s
                AND c.lncel IN %s
                
            '''
            cur.execute(sql, (tuple(counters_list), start_time, end_time, tuple(lncel_list)))
            counters_db = cur.fetchall()
            values_df = pd.DataFrame(counters_db, columns=["period_start_time", "lncel","counter_name" , "counter_value"])

            return values_df
def get_counters_in_list(counters_list,db_config):
    with connect(**db_config) as conn:
        with conn.cursor() as cur:
            sql = '''
                SELECT counter_code 
                FROM kpi.counters_def
                WHERE counter_code IN %s
            '''
            cur.execute(sql, (tuple(counters_list),))
            codes_db = cur.fetchall()
            codes_db_list = [i[0] for i in codes_db]
            return codes_db_list
def get_all_counters_codes(db_config):
    with connect(**db_config) as conn:
        with conn.cursor() as cur:
            sql = '''
                SELECT counter_code 
                FROM kpi.counters_def
            '''
            cur.execute(sql)
            codes_db = cur.fetchall()
            codes_db_list = [i[0] for i in codes_db]
            return codes_db_list