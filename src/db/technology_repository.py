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