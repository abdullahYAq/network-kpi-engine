import xlsxwriter 
def write_to_excel(result, schema,output_path):
    workbook = xlsxwriter.Workbook(output_path)
    sheet_created = False
    for class_name, objects in result.items():
        
        if not objects:
            print(f"Warning: '{class_name}' is empty. Skipping...")
            continue
        sheet_name = class_name[:31].replace("/", "_").replace("\\", "_").replace(":", "_").replace("*", "_").replace("?", "_")  # Truncate to 31 characters and replace slashes

        worksheet = workbook.add_worksheet(sheet_name)
        sheet_created = True
        base_cols = ["MRBTS", "LNBTS", "LNCEL"]
        headers = ["class", "distName"] + [c for c in base_cols if c in schema[class_name]]+sorted(col for col in schema[class_name] if col not in {"class", "distName", *base_cols})  # Ensure 'class' and 'distName' are first
        worksheet.write_row(0, 0, headers)  # Write headers in the first row
        for row_num, obj in enumerate(objects, start=1):
            row_data = [obj.get(header, "") for header in headers]
            worksheet.write_row(row_num, 0, row_data)
    if not sheet_created:
        print("No valid sheets were created. Please check the input data.")
    
    workbook.close()
    print("Done. Output saved to:", output_path)