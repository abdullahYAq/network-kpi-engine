from psycopg2 import connect, extras
def ingest_sites_to_db(db_config, sites_rows):
    try:
        sites_without_lnbts = []
        for row in sites_rows:
            if "lnbts" not in row:
                sites_without_lnbts.append(row["mrbts"])
        sites_tuple = [
            (row["mrbts"], row.get("lnbts"), row.get("mrbts_name"), row.get("lnbts_name"), row.get("distname"))
            for row in sites_rows
            if "lnbts" in row
        ]
        with connect(**db_config) as conn:
            with conn.cursor() as cur:
                sql = """INSERT INTO kpi.sites 
                (mrbts, lnbts, mrbts_name, lnbts_name, distname) 
                VALUES %s 
                ON CONFLICT (mrbts) DO NOTHING
                RETURNING mrbts"""
                inserted =extras.execute_values(cur,sql,sites_tuple, fetch=True)
                 
                inserted_count = len(inserted) 
                
                print("sites parsed:", len(sites_tuple))
                print("sites inserted:", inserted_count)
                print("sites skipped:", len(sites_tuple) - inserted_count)
                print("example sites:", sites_tuple[:3])
    except Exception as e:
        print(e)
def select_mrbts_site_id(db_config):
    try:
        sites_id_mrbts = {}
        with connect(**db_config) as conn:
            with conn.cursor() as cur:
                sql = "SELECT mrbts, id FROM kpi.sites"
                cur.execute(sql)
                sites = cur.fetchall()
                for site in sites:
                    sites_id_mrbts.update({site[0]:site[1]})
                return sites_id_mrbts
    except Exception as e:
        print(e)