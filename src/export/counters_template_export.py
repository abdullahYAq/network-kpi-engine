import pandas as pd
import openpyxl
from openpyxl.worksheet.datavalidation import DataValidation
import os
def download_template_flow():
    pass
def generate_counters_template(header_name,rows,tech_values,excel_path):
    try:
        if not rows:
            return None
        if len(header_name) != len(rows[0]):
            raise ValueError(f"Header length ({len(header_name)}) != Row length ({len(rows[0])})")
        counters_excel_data = pd.DataFrame(data=rows,columns=header_name)
        counters_sheet_name = "New Counters Insertion"
        #print(counters_excel_data)
        counters_excel_data.to_excel(excel_path,sheet_name=counters_sheet_name,index=False)
        workbook = openpyxl.load_workbook(excel_path)
        sheet_counters_opxl = workbook[counters_sheet_name]
        rows_num = sheet_counters_opxl.max_row
        if rows_num>1:  
            validation_units = DataValidation(type="list",formula1='"count,percentage,kbps,ms"')
            sheet_counters_opxl.add_data_validation(validation_units)
            validation_units.add(f"D2:D{rows_num}")         
            validation_tech = DataValidation(type="list",formula1=f'"{tech_values}"')
            sheet_counters_opxl.add_data_validation(validation_tech)
            validation_tech.add(f"E2:E{rows_num}")
            workbook.save(excel_path)
            #os.startfile(excel_path)
            return excel_path
    except Exception as e:
        raise       
def write_errors_report(excel_path, errors_df, warnings_df):
    all_errors_df = pd.concat([errors_df,warnings_df], ignore_index=True)
    with pd.ExcelWriter(excel_path,engine="openpyxl",mode="a",if_sheet_exists="replace") as writer:
        all_errors_df.to_excel(writer,sheet_name="Validation Report",index=False)
def write_success_report(excel_path, warnings_df):
    success_row = [(0,"-","Data Uploded successfully","SUCCESS")]
    success_df = pd.DataFrame(success_row,columns=["row_num","column", "message","type"])
    succes_ans_warning = pd.concat([success_df,warnings_df],ignore_index=True)
    with pd.ExcelWriter(excel_path,engine="openpyxl",mode="a",if_sheet_exists="replace") as writer:
        succes_ans_warning.to_excel(writer,sheet_name="Validation Report",index=False) 