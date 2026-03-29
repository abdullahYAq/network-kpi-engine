from src.db.counters_repository import get_all_counter_codes,insert_counters_to_db
from src.db.technology_repository import get_tech_from_db
from src.export.counters_template_export import generate_counters_template, write_errors_report,write_success_report
from src.config.db_config import db_config
import pandas as pd
from src.parsers.counters_csv_parser import extract_counters_from_csv_header
from src.validation.counters_validations import validate_counters_template
def detect_counters_flow(csv_path):
    counters_dict = extract_counters_from_csv_header(csv_path)
    if not counters_dict:
        return None
    db_counters_codes = get_all_counter_codes(db_config) 
    new_counters_rows = filter_new_counters(db_counters_codes,counters_dict)
    if not new_counters_rows:
        return None
    tech_values = get_tech_from_db(db_config)
    return new_counters_rows, tech_values
def handle_counters_template_upload(excel_path):
    db_counters_codes = get_all_counter_codes(db_config)
    excel_df = pd.read_excel(excel_path,sheet_name="New Counters Insertion")
    errors_df,warnings_df = validate_counters_template(excel_df,db_counters_codes)
    if not errors_df.empty:
        write_errors_report(excel_path, errors_df, warnings_df)
        return
    counters_number = insert_counters_to_db(excel_df,db_config)
    write_success_report(excel_path, warnings_df)
    print(f"{counters_number} counters inserted to DB")
def filter_new_counters(db_counters_codes,counters_dict):
    codes_set = {row[0] for row in db_counters_codes}
    new_counters= {
        name : code 
        for name, code in counters_dict.items()
        if code not in codes_set
    }   
    print(f"{len(new_counters)} new counters in your data from {len(counters_dict)} imported")
    rows = [[name,code,"","",""] for name,code in new_counters.items()]
    return rows


