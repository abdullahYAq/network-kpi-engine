import tkinter as tk
from tkinter import filedialog
import questionary
from src.db.technology_repository import insert_technology
from src.config.db_config import db_config

def user_selections():
    """
    prompt user for choose functions of the program 
        1- ingest Site and cells configration to the DB
            - XCEL, CSV or XML
        2- extract classes from XML dump
        3- Ingest KPI and counters values
        4- define new counter and ingest it in DB 
        5- define new KPI and ingest it in DB
    """
    selected = questionary.select(
            "Choose a function to perform:",
            choices=[
                "ingest Site and cells configration to the DB",
                "extract classes from XML dump",
                "Ingest KPI and counters values",
                "define new counter and ingest it in DB",
                "define new KPI and ingest it in DB",
                "INSERT New Technology",
                "Exit"
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
def select_classes_ui(classes):
    """
    Prompt user to select classes from a list.
    Args:
        classes (list): list of class names"""
    selected_classes = set()
    while True:
        keywords = questionary.text(
        "Enter keywords to filter classes (comma or space separated, leave empty for all):"
        ).ask()
        if keywords is None:
            return []
        filtered_classes = filter_classes_by_keywords(classes, keywords)
        if not filtered_classes:
            print("No classes match your search.")
            continue
        chosen_classes = questionary.checkbox(
            f"{len(filtered_classes)} classes found:",
            choices=sorted(filtered_classes)
        ).ask()
        if not chosen_classes:
            print("No classes selected from the search results.")
        if chosen_classes:
            before = len(selected_classes)
            selected_classes.update(chosen_classes)
            added = len(selected_classes) - before
            print(f"{added} new classes added. Total selected: {len(selected_classes)}")
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
            if not selected_classes:
                print("No classes selected yet.")
            else:
                print("Selected classes:")
                for c in sorted(selected_classes):
                    print(f" - {c}")
        elif action == "remove from selection":
            if not selected_classes:
                print("No classes to remove. Selection is empty.")
                continue
            to_remove = questionary.checkbox(
                "Select classes to remove from selection:",
                choices=sorted(selected_classes)
            ).ask()
            if to_remove:
                for c in to_remove:
                    selected_classes.discard(c)
                print(f"{len(to_remove)} classes removed. Total selected: {len(selected_classes)}")
            else:
                print("No classes removed.")
        elif action == "confirm selection":
            if not selected_classes:
                print("No classes selected. Please select at least one class.") 
                continue
            confirm = questionary.confirm(f"Confirm selection of {len(selected_classes)} classes?").ask()
            if confirm:
                return sorted(selected_classes)
        elif action == "Exit":
            break
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
                "Insert KPIs hourly values",
                "Back"
            ]).ask()
    return selected
def kpi_def_sub_menu():
    selected = questionary.select(
            "Choose a function to perform:",
            choices=[
                "Generate excel template for KPI definition",
                "upload excel file with KPI definitions",
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