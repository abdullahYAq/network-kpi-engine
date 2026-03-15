from src.cli.menu import user_selections, choose_xml_file,select_classes_ui,open_file
from src.ingestion.ingest_xml_topology import ingest_xml_topology
from tkinter import filedialog
from src.parsers.xml_parser import extract_classes,extract_selected_objects
from src.db.technology_repository import insert_technology
from src.config.db_config import db_config
from src.export.excel_export import write_to_excel

def main():
    user_selection = user_selections()
    if user_selection == "ingest Site and cells configration to the DB":
        ingest_xml_topology(xml_path=choose_xml_file())
        
    elif user_selection == "Ingest KPI and counters values":
        print("This function is not implemented yet.")
        exit()
    elif user_selection == "define new counter and ingest it in DB":
        print("This function is not implemented yet.")
        exit()
    elif user_selection == "define new KPI and ingest it in DB":
        print("This function is not implemented yet.")
        exit()
    elif user_selection == "extract classes from XML dump":
        print("You chose to extract classes from XML dump.")
        xml_path = choose_xml_file()
        classes, object_counter = extract_classes(xml_path)
        classes_list = sorted(classes)

        selected_classes = select_classes_ui(classes_list)
        print(selected_classes)
        if not selected_classes:
            print("No classes selected. Exiting.")
            exit()
        result, schema, scanned_obj = extract_selected_objects(xml_path, selected_classes, object_counter)
    
        output_path = filedialog.asksaveasfilename(title="Save Excel File", defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
    
        if not output_path:
            print("No output file selected. Exiting.")
            exit()
        write_to_excel(result, schema, output_path)
        open_file(output_path)
    elif user_selection == "INSERT New Technology":
        tech_name = input("Enter technology name: ")
        tech_priority = int(input("Enter technology priority (integer): "))
        insert_technology(db_config, tech_name, tech_priority)
if __name__ == "__main__":
   main()
   