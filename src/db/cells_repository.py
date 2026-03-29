from psycopg2 import connect, extras
def ingest_cells_to_db(db_config,cells_rows):
    try:
        cells_tuple = [
            (row["lncel"],row.get("lncel_name"),row.get("distname"),1,row.get("site_id"))
            for row in cells_rows
        ]
        print(f"cell example: {cells_tuple[:1]}")
        print(f"{len(cells_tuple)} cells is there")
        with connect(**db_config) as conn:
            with conn.cursor() as cur:
                sql = '''INSERT INTO kpi.cells 
                (lncel,lncel_name,distname,technology_id,site_id) 
                VALUES %s 
                ON CONFLICT (distname) DO NOTHING
                RETURNING distname'''
                inserted=extras.execute_values(cur,sql,cells_tuple, fetch=True)
                inserted_count = len(inserted)
                print(f"{len(cells_tuple)} cells are inserted")
                print("cells skipped", len(cells_tuple)-inserted_count)
    except Exception as e:
        raise e
def get_lncel_name_id_map(db_config):
    with connect(**db_config) as conn:
        with conn.cursor() as cur:
            sql = '''
                SELECT lncell_name ,id
                FROM kpi.cells
            ''' 
            cur.execute(sql)
            lncel_name_id = cur.fetchall()
            if not lncel_name_id:
                raise ValueError("No cells found in DB")
            lncel_name = [i[0] for i in lncel_name_id]

            if len(lncel_name) != len(set(lncel_name)):
                raise ValueError("Duplicate lncel_name detected in DB")
            lncel_map = {
                i[0].strip().upper() : i[1]
                for i in lncel_name_id
            }
            return lncel_map
def get_distname_id_map(db_config):
    with connect(**db_config) as conn:
        with conn.cursor() as cur:
            sql = '''
                SELECT distname ,id
                FROM kpi.cells
            ''' 
            cur.execute(sql)
            distname_id = cur.fetchall()
            if not distname_id:
                raise ValueError("No cells found in DB")
            distname = [i[0] for i in distname_id]

            if len(distname) != len(set(distname)):
                raise ValueError("Duplicate distname detected in DB")
            distname_map = {
                i[0].strip().upper() : i[1]
                for i in distname_id
            }
            return distname_map