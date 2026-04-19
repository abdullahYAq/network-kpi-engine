import pandas as pd
def write_compare_template_to_excel(grouped_by_class_params, saved_path):
    '''
        create data frame from parameter_list_of_dict and save in the saved_path
    '''
    headers = ["class_name","param","value","warning","type"]
    with pd.ExcelWriter(saved_path,engine='xlsxwriter',mode='w') as writer:
        for class_name, class_params in grouped_by_class_params.items():
            class_df = pd.DataFrame(data=class_params,columns=headers)
            sheet_name = class_name
            class_df.to_excel(writer,sheet_name=sheet_name,index=False)
def export_mismatch_to_excel(result_dict, result_xl_path):
    mismatch_only = [row for row in result_dict if row["status"] == "Mismatch"]
    if not mismatch_only:
        print("No mismatches found.")
        return
    grouped = {}
    columns = ["id", "class", "parameter", "template", "actual", "status"]
    for row in mismatch_only:
        class_name = row["class"]
        if class_name not in grouped:
            grouped[class_name] = []
        grouped[class_name].append(row)
    with pd.ExcelWriter(result_xl_path,engine="xlsxwriter", mode='w') as writer:
        for class_name, rows in grouped.items():
            df = pd.DataFrame(rows)
            df = df.reindex(columns=columns)
            df = df.sort_values(by=["id", "parameter"])
            safe_name = class_name[:31]
            df.to_excel(writer, sheet_name=safe_name, index=False)
            worksheet = writer.sheets[safe_name]
            worksheet.freeze_panes(1, 0)
    
    