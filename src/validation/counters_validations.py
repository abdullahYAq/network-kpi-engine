import pandas as pd
def validate_counters_template(excel_df,db_counters_codes):
    expected_columns = ["counter_name","counter_code","counter_description","unit","tech_name"]
    selected_sheet = excel_df
    if list(selected_sheet.columns) != expected_columns:
        raise ValueError("Invalid template format")
    codes_set = {row[0] for row in db_counters_codes}
    duplicate_code = selected_sheet[selected_sheet["counter_code"].isin(codes_set) & selected_sheet["counter_code"].notna()]
    duplicate_code_index = list(duplicate_code.index)
    na_list_counter = selected_sheet[selected_sheet["unit"].isna()]
    inv_list_counter =  selected_sheet[~selected_sheet["unit"].isin(["count","percentage","kbps","ms"])& selected_sheet["unit"].notna()]
    na_list_counter_index = list(na_list_counter.index)
    inv_list_counter_index= list(inv_list_counter.index)
    na_list_tech = selected_sheet[selected_sheet["tech_name"].isna()]
    inv_list_tech =  selected_sheet[~selected_sheet["tech_name"].isin(["LTE","UMTS","GSM","NSANR"])& selected_sheet["tech_name"].notna()]
    na_list_tech_index = list(na_list_tech.index)
    inv_list_tech_index= list(inv_list_tech.index)
    na_list_name = selected_sheet[selected_sheet["counter_name"].isna()]
    na_list_code = selected_sheet[selected_sheet["counter_code"].isna()]
    na_list_name_index = list(na_list_name.index)
    na_list_code_index = list(na_list_code.index)
    na_list_des = selected_sheet[selected_sheet["counter_description"].isna()]
    na_list_des_index = list(na_list_des.index)
    warning_error = [
        (i+2,"counter_description","missing_description","Warning")
        for i in na_list_des_index
    ]
    errors = [
        (i+2,"unit","missing value","error")
        for i in na_list_counter_index
    ]
    errors.extend(
        (i+2,"unit", "invalid value","error")
        for i in inv_list_counter_index
    )
    errors.extend(
        (i+2,"tech_name","missing value","error")
        for i in na_list_tech_index
    )
    errors.extend(
        (i+2,"tech_name","invalid value","error")
        for i in inv_list_tech_index
    )
    errors.extend(
        (i+2,"counter_name","missing value","error")
        for i in na_list_name_index
    )
    errors.extend(
        (i+2,"counter_code","missing value","error")
        for i in na_list_code_index
    )
    warning_error.extend(
        (i+2, "counter_code", "already exists in DB", "Warning")
        for i in duplicate_code_index
    )
    errors_df = pd.DataFrame(errors,columns=["row_number","column", "message","type"])
    warning_df=pd.DataFrame(warning_error,columns=["row_number","column", "message","type"])
    #excel_df = pd.DataFrame()
    return errors_df,warning_df