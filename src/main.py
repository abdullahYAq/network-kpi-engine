from src.cli.menu import user_selections, choose_xml_file,select_classes_ui, open_file, choose_csv_file, handle_tech_ingest,counter_def_sub_menu,choose_excel_save_path, choose_excel_file,counters_kpi_value_sub_menu,missing_cells_insert_sub_menu,kpi_def_sub_menu
from src.ingestion.ingest_xml_topology import ingest_xml_topology
from tkinter import filedialog
import questionary
from src.parsers.xml_parser import extract_classes,extract_selected_objects
from src.export.xml_dump_excel_export import write_to_excel
from src.export.counters_template_export import generate_counters_template ,create_empty_counters_template
from src.export.kpi_template_export import create_empty_kpi_template
from src.ingestion.counters_def_ingestion import detect_counters_flow, handle_counters_template_upload,filter_new_counters
from src.ingestion.counters_value_ingestion import ingest_counters_values, rename_counter_column_to_id,load_counter_values,transform_wide_to_long,map_and_rename_column_from_dict
from src.ingestion.kpi_def_ingestion import handle_kpi_template_upload
from src.utils.distname_utils import distName_to_dict
def main():
    while True:
        user_selection = user_selections()
        if user_selection == "ingest Site and cells configration to the DB":
            ingest_xml_topology(xml_path=choose_xml_file())          
        elif user_selection == "Ingest KPI and counters values":
            while True:
                choice = counters_kpi_value_sub_menu()
                if choice == "Insert CSV raw counters hourly values":
                    csv_path = choose_csv_file()
                    counter_list,df = load_counter_values(csv_path)
                    
                    new_df = rename_counter_column_to_id(counter_list,df)
                    
                    long_df = transform_wide_to_long(new_df)
                    
                    cleaned_mapped_df,mapped_df = map_and_rename_column_from_dict(long_df,"DN")
                    
                    missed_cells = mapped_df[mapped_df["cell_id"].isna()]["DN"].unique()
                    print(f"missed_cells that will not be ingested: {missed_cells}")

                    if len(missed_cells)>0:
                        print(f"missed_cells: {missed_cells}")
                        missing_cells_choice = missing_cells_insert_sub_menu()
                        while True:
                            if missing_cells_choice == "Insert missing cells to DB":
                                print("no function implemented yet to insert cells based on DN, you can insert them manually in the DB and try again")
                                continue                      
                            elif missing_cells_choice == "continue without inserting":
                                # you can choose to continue without inserting the missing cells, but the corresponding counter values will not be ingested for those cells.
                                print("continuing without inserting missing cells, the corresponding counter values will not be ingested for those cells.")
                                cleaned_missed_cells = cleaned_mapped_df[cleaned_mapped_df["cell_id"].isna()]["DN"].unique()
                                print(f"missed_cells that will not be ingested: {cleaned_missed_cells}")
                                print(cleaned_mapped_df)
                                print(cleaned_mapped_df.isna().sum(), "\n", cleaned_mapped_df.dtypes)
                                #ingest_counters_values(cleaned_mapped_df)
                                ingest_counters_values(cleaned_mapped_df)
                                break
                            elif missing_cells_choice == "Back":
                                break
                    else:
                        print("All cells are mapped successfully!")
                        ingest_counters_values(mapped_df)
                        break
                elif choice == "Insert KPIs hourly values":
                    print("This function is not implemented yet.")
                    continue
                elif choice == "Back":
                    break
        elif user_selection == "define new counter and ingest it in DB":
            #handle_counters_definition()
            while True:
                choice = counter_def_sub_menu()

                if choice == "Detect counters from CSV":
                    csv_path = choose_csv_file()
                    result=detect_counters_flow(csv_path)
                    if not result:
                        print("No new counters to insert")
                        continue
                    rows, tech_values = result
                    excel_path = choose_excel_save_path()
                    if not excel_path:
                        print("No excel file selected!")
                        continue
                    header_name = ["counter_name","counter_code","counter_description","unit","tech_name"]
                    created_excel = generate_counters_template(header_name,rows,tech_values,excel_path)
                    open_file(created_excel)
                elif choice == "Upload counters from template":
                    counter = 0
                    edited_excel = choose_excel_file()
                    while counter<3:
                        try:
                            handle_counters_template_upload(edited_excel)
                            open_file(edited_excel)
                            break
                        except PermissionError:
                            attempt = counter + 1
                            counter+=1
                            questionary.confirm(f"Please close the selected file to continue! | attempt number: {attempt} | do you want to try again").ask()
                            continue
                    if counter ==3:
                        print("Operation cancelled")
                        continue
                elif choice == "Download counters template":
                    header_name = ["counter_name","counter_code","counter_description","unit","tech_name"]
                    excel_path = choose_excel_save_path()
                    if not excel_path:
                        print("You did not choose path for the new template!")
                        continue
                    create_empty_counters_template(excel_path,header_name)
                    print("Template created successfully")
                    open_file(excel_path)
                    continue
                
                elif choice == "Back":
                    break
        elif user_selection == "define new KPI and ingest it in DB":
            while True:
                choice = kpi_def_sub_menu()
                if choice == "Generate excel template for KPI definition":
                    header_name = ["kpi_name","kpi_type","numerator (ratio only)","denominator (ratio only)","expression (expression only)","multiplier","description","tech_name"]
                    excel_path = choose_excel_save_path()
                    if not excel_path:
                        print("You did not choose path for the new template!")
                        continue
                    create_empty_kpi_template(excel_path,header_name)
                    print("Template created successfully")
                    open_file(excel_path)
                    continue
                elif choice == "upload excel file with KPI definitions":
                    counter = 0
                    edited_excel = choose_excel_file()
                    while counter<3:
                        try:
                            handle_kpi_template_upload(edited_excel)
                            open_file(edited_excel)
                            break
                        except PermissionError:
                            attempt = counter + 1
                            counter+=1
                            questionary.confirm(f"Please close the selected file to continue! | attempt number: {attempt} | do you want to try again").ask()
                            continue
                    if counter ==3:
                        print("Operation cancelled")
                        continue
                    continue
                elif choice == "Back":
                    break          
        elif user_selection == "extract classes from XML dump":
            print("You chose to extract classes from XML dump.")
            xml_path = choose_xml_file() 
            if not xml_path:
                continue
            classes, object_counter = extract_classes(xml_path)
            classes_list = sorted(classes)

            selected_classes = select_classes_ui(classes_list)
            print(selected_classes)
            if not selected_classes:
                print("No classes selected. Exiting.")
                continue
            result, schema, scanned_obj = extract_selected_objects(xml_path, selected_classes, object_counter)
        
            output_path = filedialog.asksaveasfilename(title="Save Excel File", defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        
            if not output_path:
                print("No output file selected. Exiting.")
                continue
            write_to_excel(result, schema, output_path)
            open_file(output_path)
        elif user_selection == "INSERT New Technology":
            handle_tech_ingest()
        elif user_selection == "Exit":
            break
if __name__ == "__main__":
   main()
   