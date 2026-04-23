from psycopg2 import connect, extras
from src.parsers.kpi_formula_parser import parse_expression
def get_kpi_id_name_from_db(db_config):
    id_kpi_dict = {}
    with connect(**db_config) as conn:
        with conn.cursor() as cur:
            sql = '''
                SELECT kpi_name, id FROM kpi.kpi_def;
            '''
            cur.execute(sql)
            kpis = cur.fetchall()
            for kpi in kpis:
                id_kpi_dict.update({kpi[0]:kpi[1]})
            return id_kpi_dict
def insert_kpis_to_db(kpi_df, db_config):
    tech_map = {"LTE":1,"UMTS":2,"GSM":3,"NSANR":0}
    df_copy = kpi_df.copy()
    df_copy["tech_id"] = df_copy["tech_name"].map(tech_map)
    
    kpi_tuple = [
        (row["kpi_name"], row["description"], "formula",row["tech_id"])
        for _, row in df_copy.iterrows()
    ]
    kpi_formula_rows = []
    with connect(**db_config) as conn:
        with conn.cursor() as cursor:
            try:
                sql_insert_kpi_def = """
                    INSERT INTO kpi.kpi_def (kpi_name, kpi_description, source_type, technology_id)
                    VALUES %s
                    RETURNING kpi_name, id
                """
                
                kpi_ids = extras.execute_values(cursor, sql_insert_kpi_def, kpi_tuple, fetch=True)
                kpi_id_map = {
                        i[0] : i[1]
                        for i in kpi_ids
                    }
                # mapping counter codes to IDs for the inserted kpis
                for i, row in df_copy.iterrows():
                    expression = row["formula"]
                    kpi_formula_rows.append((
                        kpi_id_map[row["kpi_name"]],  
                        expression,
                        expression.replace(" ","").replace("=","")
                    ))
                
                sql_insert_kpi_formula = """
                    INSERT INTO kpi.kpi_formula (kpi_id, raw_formula, norm_formula)
                    VALUES %s 
                """
                
                extras.execute_values(cursor,sql_insert_kpi_formula, kpi_formula_rows)
            except Exception as e:
                
                raise e   
            
def get_all_kpi_names(db_config):
    with connect(**db_config) as conn:
        with conn.cursor() as cur:
            sql = '''
                SELECT kpi_name 
                FROM kpi.kpi_def
            '''
            cur.execute(sql)
            kpi_db = cur.fetchall()
            return kpi_db