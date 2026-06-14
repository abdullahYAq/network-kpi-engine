import tkinter as tk
from tkinter import filedialog
import questionary
from src.db.technology_repository import insert_technology
from src.config.db_config import db_config

def user_selections():
    """
    prompt user for choose functions of the program 
        1- export counters and KPIs reports
        2- ingest Site and cells configration to the DB
            - XCEL, CSV or XML
        3- extract classes from XML dump
        4- Ingest KPI and counters values
        5- define new counter and ingest it in DB 
        6- define new KPI and ingest it in DB
        7- INSERT New Technology
        8- Compare two XML dumps
        9- Exit
    """
    selected = questionary.select(
            "Choose a function to perform:",
            choices=[
                "export counters and KPIs reports",
                "ingest Site and cells configration to the DB",
                "extract classes from XML dump",
                "Ingest KPI and counters values",
                "define new counter and ingest it in DB",
                "define new KPI and ingest it in DB",
                "INSERT New Technology",
                "Compare two XML dumps",
                "Exit"
            ]).ask()
    return selected
def params_compare_sub_menu():
    selected = questionary.select(
            "Choose a function to perform:",
            choices=[
                "Generate template to compare.",
                "Compare new data",
                "Back"
            ]).ask()
    return selected
def open_file(path):
    open_file = questionary.confirm("Do you want to open the output file now?").ask()
    if open_file:
        import os
        os.startfile(path)
def choose_xml_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    root.attributes("-topmost", True)
    root.update()
    xml_path = filedialog.askopenfilename(title="Select XML File", filetypes=[("XML Files", "*.xml")])
    if not xml_path:
        print("No XML file selected. Exiting.")
        root.destroy()
        return "No file selected"
    root.destroy()
    return xml_path
def choose_csv_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    root.attributes("-topmost", True)
    root.update()
    csv_file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSVL Files", "*.csv")])
    if not csv_file_path:
        print("No CSV file selected. Exiting.")
        root.destroy()
        return "No file selected"
    root.destroy()
    return csv_file_path
def choose_excel_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    root.attributes("-topmost", True)
    root.update()
    excel_file_path = filedialog.askopenfilename(title="Select excel File", filetypes=[("excel Files", "*.xlsx")])
    if not excel_file_path:
        print("No excel file selected. Exiting.")
        root.destroy()
        return "No file selected"
    root.destroy()
    return excel_file_path
def choose_excel_save_path():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    root.attributes("-topmost", True)
    while True:
        root.update()  # Update the window to ensure it is active
        excel_path = filedialog.asksaveasfilename(title="Save Excel File", defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if not excel_path:
            ask_cont=questionary.confirm("Do you want to continue choose file?").ask()
            if ask_cont:
                continue
            else:
                root.destroy()
                return None
        root.destroy()  # Close the Tkinter window
        return excel_path
def select_names_ui(names_list, names):
    """
    Prompt user to select names from a list.
    Args:
        names_list (list): list of chosen names"""
    selected = set()
    while True:
        keywords = questionary.text(
        f"Enter keywords to filter '{names}' (comma or space separated, leave empty for all):"
        ).ask()
        if keywords is None:
            return []
        filtered = filter_classes_by_keywords(names_list, keywords)
        if not filtered:
            print(f"No '{names}' match your search.")
            continue
        chosen_names = questionary.checkbox(
            f"{len(filtered)} {names} found:",
            choices=sorted(filtered)
        ).ask()
        if not chosen_names:
            print(f"No {names} selected from the search results.")
        if chosen_names:
            before = len(selected)
            selected.update(chosen_names)
            added = len(selected) - before
            print(f"{added} new {names} added. Total selected: {len(selected)}")
        action = questionary.select(
            "Next Step:",
            choices=[
                "search again",
                "show selected",
                "remove from selection",
                "confirm selection",
                 "Exit"
            ]).ask()
        if action == "search again":
            continue
        elif action == "show selected":
            if not selected:
                print("No names selected yet.")
            else:
                print("Selected names:")
                for c in sorted(selected):
                    print(f" - {c}")
        elif action == "remove from selection":
            if not selected:
                print("No names to remove. Selection is empty.")
                continue
            to_remove = questionary.checkbox(
                "Select names to remove from selection:",
                choices=sorted(selected)
            ).ask()
            if to_remove:
                for c in to_remove:
                    selected.discard(c)
                print(f"{len(to_remove)} names removed. Total selected: {len(selected)}")
            else:
                print("No names removed.")
        elif action == "confirm selection":
            if not selected:
                print("No names selected. Please select at least one name.") 
                continue
            confirm = questionary.confirm(f"Confirm selection of {len(selected)} names?").ask()
            if confirm:
                return sorted(selected)
        elif action == "Exit":
            break
def select_counters_cells_ui():
    """
    user write counter codes and lncel values separated by comma or space, then return 2 lists of counters and lncel values
    """
    counter_codes = questionary.text("Enter counter codes (comma or space separated): ").ask()
    lncel_values = questionary.text("Enter lncel values (comma or space separated): ").ask()
    if counter_codes is None or lncel_values is None:
        print("Input cancelled. Returning empty lists.")
        return [], []
    counter_codes_list = [c.strip().upper() for c in counter_codes.replace(",", " ").split() if c.strip()]
    lncel_values_list = [l.strip() for l in lncel_values.replace(",", " ").split() if l.strip()]
    return counter_codes_list, lncel_values_list
def filter_classes_by_keywords(classes, keywords):
    """
    Filter classes by keywords (case-insensitive).
    keywords: string like "nr,cell" or "ip"
    """
    if not keywords:
        return classes

    # split by comma or space
    tokens = [k.strip().lower() for k in keywords.replace(",", " ").split() if k.strip()]

    filtered = []
    for c in classes:
        name = c.lower()
        if any(t in name for t in tokens):
            filtered.append(c)

    return filtered
def counter_def_sub_menu():
    selected = questionary.select(
            "Choose a function to perform:",
            choices=[
                "Detect counters from CSV",
                "Download counters template",
                "Upload counters from template",
                "Back"
            ]).ask()
    return selected
def counters_kpi_value_sub_menu():
    selected = questionary.select(
            "Choose a function to perform:",
            choices=[
                "Insert CSV raw counters hourly values",
                "Insert CSV raw counters daily values",
                "Insert KPIs hourly values",
                "Back"
            ]).ask()
    return selected
def kpi_def_sub_menu():
    selected = questionary.select(
            "Choose a function to perform:",
            choices=[
                "Generate excel template for KPI definition and formula",
                "upload excel file with KPI definitions to be ingested in the system",
                "define KPI from CSV to be system KPI (no formula)",
                "Back"
            ]).ask()
    return selected
def kpi_def_csv_menu():
    selected = questionary.select(
            "Choose a function to perform:",
            choices=[
                "Detect KPIs from CSV",
                "Upload KPIs template",
                "Back"
            ]).ask()
    return selected
def missing_cells_insert_sub_menu():
    selected = questionary.select(
            "Choose a function to perform:",
            choices=[
                "Insert missing cells to DB",
                "continue without inserting",
                "Back"
            ]).ask()
    return selected
def handle_tech_ingest():
    tech_name = questionary.text("Enter technology name: ").ask()
    tech_priority = questionary.text("Enter technology priority: ").ask()
    if not tech_priority or not tech_priority.isdigit():
        print("Invalid priority. Returning to menu.")
        return None
    tech_priority = int(tech_priority)
    insert_technology(db_config,tech_name,tech_priority)
def export_period_sub_menu():
    selected = questionary.select(
            "Choose a daily or hourly report:",
            choices=[
                "daily",
                "hourly"
            ]).ask()
    return selected
def export_time_range_sub_menu():
    selected = questionary.select(
            "Choose a time range for the report:",
            choices=[
                "last 24 hours",
                "last 7 days",
                "last 30 days",
                "custom range"
            ]).ask()
    return selected
def export_time_custom_range():
    start_date = questionary.text("Enter start date (YYYY-MM-DD): ").ask()
    end_date = questionary.text("Enter end date (YYYY-MM-DD): ").ask()

    return start_date, end_date
def export_selections_config():
    selected = questionary.select(
        "Select which reports to export:",
        choices=[
            "Export counters report",
            "Export KPIs report",
            "Back"
        ]).ask()
    return selected
def export_level_sub_menu():
    selected = questionary.select(
            "Choose a daily or hourly report:",
            choices=[
                "cell level",
                "site level"
            ]).ask()
    return selected