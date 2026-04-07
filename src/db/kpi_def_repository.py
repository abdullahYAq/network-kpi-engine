from psycopg2 import connect, extras
from src.parsers.kpi_formula_parser import parse_expression
def insert_kpis_to_db(kpi_df, db_config,counteridsmap):
    conn = connect(**db_config)
    cursor = conn.cursor()
    tech_map = {"LTE":1,"UMTS":2,"GSM":3,"NSANR":0}
    df_copy = kpi_df.copy()
    df_copy["tech_id"] = df_copy["tech_name"].map(tech_map)
    try:
        # prepare kpi_def_rows
        kpi_def_rows = []
        kpi_formula_rows = []
        source_type = "formula"
        for i, row in df_copy.iterrows():
            kpi_def_rows.append((
                row["kpi_name"],
                row["description"],
                source_type,
                row["tech_id"],
                row["multiplier"],
                row["kpi_type"]
            ))
        sql_insert_kpi_def = """
            INSERT INTO kpi.kpi_def (kpi_name, kpi_description, source_type, technology_id, coefficient, kpi_type)
            VALUES %s
            RETURNING kpi_name, kpi_id
        """
        kpi_ids = extras.execute_values(sql_insert_kpi_def, kpi_def_rows, cursor=cursor, fetch=True)
        kpi_id_map = {
                i[0] : i[1]
                for i in kpi_ids
            }
        # mapping counter codes to IDs for the inserted kpis
        for i, row in df_copy.iterrows():
            if row["kpi_type"] == "ratio (num/den)":
                numerator = row["numerator (ratio only)"]
                denominator = row["denominator (ratio only)"]
                num_list, _ = parse_expression(numerator)
                den_list, _ = parse_expression(denominator)
                for term in num_list:
                    if term["coef"] == 0:
                        continue
                    kpi_formula_rows.append({
                        "kpi_id": kpi_ids[i][1],  
                        "counter_id": counteridsmap[term["counter_code"]],
                        "coef": term["coef"],
                        "part": "numerator"
                    })
                for term in den_list:
                    if term["coef"] == 0:
                        continue
                    kpi_formula_rows.append({
                        "kpi_id": kpi_id_map[row["kpi_name"]],  
                        "counter_id": counteridsmap[term["counter_code"]],
                        "coef": term["coef"],
                        "part": "denominator"
                    })
            elif row["kpi_type"] == "expression":
                expression = row["expression (expression only)"]
                exp_list, _ = parse_expression(expression)
                for term in exp_list:
                    if term["coef"] == 0:
                        continue
                    kpi_formula_rows.append({
                        "kpi_id": kpi_id_map[row["kpi_name"]],  
                        "counter_id": counteridsmap[term["counter_code"]],
                        "coef": term["coef"],
                        "part": "expression"
                    })
        sql_insert_kpi_formula = """
            INSERT INTO kpi.kpi_formula (kpi_id, counter_id, coef, part)
            VALUES %s 
        """
        formula_tuple = [
            (row["kpi_id"], row["counter_id"], row["coef"], row["part"])
            for row in kpi_formula_rows
        ]
        extras.execute_values(sql_insert_kpi_formula, formula_tuple, cursor=cursor)
        conn.commit()
        conn.close()
    except Exception as e:
        conn.rollback()
        conn.close()
            