from src.cli.menu import user_selections, choose_xml_file,select_classes_ui, open_file, choose_csv_file, handle_tech_ingest,counter_def_sub_menu,choose_excel_save_path
from src.ingestion.ingest_xml_topology import ingest_xml_topology
from tkinter import filedialog
from src.parsers.xml_parser import extract_classes,extract_selected_objects
from src.export.xml_dump_excel_export import write_to_excel
from src.export.counters_template_export import generate_counters_template 
from src.ingestion.counters_def_ingestion import detect_counters_flow 
def main():
    while True:
        user_selection = user_selections()
        if user_selection == "ingest Site and cells configration to the DB":
            ingest_xml_topology(xml_path=choose_xml_file())          
        elif user_selection == "Ingest KPI and counters values":
            print("This function is not implemented yet.")           
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
                        continue
                    header_name = ["counter_name","counter_code","counter_description","unit","tech_name"]
                    generate_counters_template(header_name,rows,tech_values,excel_path)
                elif choice == "Download counters template":
                    #download_template_flow()
                    continue
                elif choice == "Import counters from template":
                    #import_template_flow()
                    continue
                elif choice == "Back":
                    break
        elif user_selection == "define new KPI and ingest it in DB":
            print("This function is not implemented yet.")            
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
   