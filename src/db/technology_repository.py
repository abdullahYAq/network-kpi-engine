from psycopg2 import connect, extras
def insert_technology(db_config, technology_name, tech_priority):
    try:
        with connect(**db_config) as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO kpi.technology (tech_name, tech_priority) VALUES (%s, %s) ON CONFLICT (tech_name) DO NOTHING RETURNING id", (technology_name, tech_priority))
                result = cur.fetchone()
                if result is not None:
                    tech_id = result[0]
                    print(f"Inserted technology '{technology_name}' with ID: {tech_id} and priority: {tech_priority}")
                    return tech_id
                else:
                    print(f"Technology '{technology_name}' already exists.")
                    return None
    except Exception as e:
        print(f"Error inserting technology: {e}")
        return None
def get_tech_from_db(db_config):
    try:
        with connect(**db_config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT tech_name FROM kpi.technology")
                result = cur.fetchall()
                print(result)
                tech_values = []
                if result is not None:
                    for res in result:
                        tech_values.append(res[0])
                    tech_values_str = ','.join(tech_values)    
                    return tech_values_str
                else:
                    print(f"No Technology exists.")
                    return None
    except Exception as e:
        print(f"Error getting technology: {e}")
        return None