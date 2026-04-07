from src.config.db_config import db_config
import pandas as pd
from src.db.counters_repository import get_all_counter_codes, get_counter_id_counter_code_map
from src.db.kpi_def_repository import insert_kpis_to_db
from src.validation.kpi_validations import validate_kpi_template_statics, validate_kpi_template_dynamic
from src.export.kpi_template_export import write_errors_report,write_success_report
import datetime
def read_xcel_file(excel_path):
    df = pd.read_excel(excel_path)
    return df
def handle_kpi_template_upload(excel_path):
    try:
        kpi_df = read_xcel_file(excel_path)
        errors, warnings = validate_kpi_template_statics(kpi_df)
        counter_codes = get_all_counter_codes(db_config)
        errors_dynamic, all_counters = validate_kpi_template_dynamic(kpi_df, counter_codes)
        all_errors_df = pd.concat([errors, errors_dynamic], ignore_index=True)
        if all_errors_df.empty:
            counter_code_counter_id_map = get_counter_id_counter_code_map(db_config)
            #parsed_functions = 
            insert_kpis_to_db(kpi_df, db_config, counter_code_counter_id_map)
            write_success_report(excel_path, warnings)
            print("KPI definitions are valid. KPI definitions have been inserted into the database successfully.")
        else:
            write_errors_report(excel_path, all_errors_df, warnings)
    except Exception as e:
        print(f"An error occurred while processing the KPI template: {e}")   
    
        

