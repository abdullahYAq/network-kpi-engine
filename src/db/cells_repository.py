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
                ON CONFLICT (lncel) DO NOTHING
                RETURNING lncel'''
                inserted=extras.execute_values(cur,sql,cells_tuple, fetch=True)
                inserted_count = len(inserted)
                print(f"{len(cells_tuple)} cells are inserted")
                print("cells skipped", len(cells_tuple)-inserted_count)
                print("example cells:", cells_tuple[:3])
    except Exception as e:
        print(e)