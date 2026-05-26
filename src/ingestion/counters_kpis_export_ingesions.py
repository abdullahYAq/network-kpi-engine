from src.cli.menu import export_level_sub_menu,export_time_custom_range,export_time_range_sub_menu,export_period_sub_menu
from datetime import datetime, timedelta
from src.db.counters_repository import get_counters_in_list, get_raw_counters_values_df, get_all_counters_codes
from src.db.cells_repository import get_cells_in_list, get_all_cells
from src.db.kpi_def_repository import get_kpis_in_list, get_all_kpi_names_list
from src.db.kpi_counter_values_repository import get_kpis_row_values_df
from src.config.db_config import db_config
import pandas as pd
def get_report_config():
    level = export_level_sub_menu() # cell level, site level
    period = export_period_sub_menu() # daily,hourly
    time_range = export_time_range_sub_menu() # last 24 hours, last 7 days, last 30 days, custom range
    if time_range == "custom range":
        start_time, end_time = export_time_custom_range()
        start_time_dt = datetime.strptime(start_time, "%Y-%m-%d") if start_time else None
        end_time_dt = datetime.strptime(end_time, "%Y-%m-%d") if end_time else None
        if not start_time_dt or not end_time_dt:
            print("Invalid start or end time. Please provide valid dates.")
            return None
        if start_time_dt >= end_time_dt:
            print("Invalid time range. Start time must be before end time.")
            return None
        end_time_dt = end_time_dt + timedelta(days=1)
    elif time_range == "last 24 hours":
        end_time_dt = datetime.now()
        start_time_dt = end_time_dt - timedelta(hours=24)
    elif time_range == "last 7 days":
        end_time_dt = datetime.now()
        start_time_dt = end_time_dt - timedelta(days=8)
    elif time_range == "last 30 days":
        end_time_dt = datetime.now()
        start_time_dt = end_time_dt - timedelta(days=31)
    print(f"Level: {level}, Period: {period}, Time Range: {time_range}, Start Time: {start_time_dt}, End Time: {end_time_dt}")
    report_config = {
        "level": level,
        "period": period,
        "time_range": time_range,
        "start_time": start_time_dt,
        "end_time": end_time_dt
    }
    return report_config
def get_counters_and_cells_db():
    cells_db = get_all_cells(db_config)
    counters_db = get_all_counters_codes(db_config)
    return cells_db, counters_db
def get_kpis_and_cells_db():
    cells_db = get_all_cells(db_config)
    kpis_db = get_all_kpi_names_list(db_config)
    return cells_db, kpis_db
def handle_kpis_export_ingestion(report_config,kpis_user_list,cells_user_list):
    '''    compare the user selected cells with the ones in the database, if any of them is not in the database, inform the user and skip it, then get the values of the existing cells and export them to excel file
    '''
    existing_cells = get_cells_in_list(cells_user_list, db_config)
    existing_cells_str = [str(n) for n in existing_cells]
    print(f"Existing cells in DB: {existing_cells_str}")
    missing_cells = set(cells_user_list) - set(existing_cells_str)
    if missing_cells:
        print(f"The following cells are not found in the database and will be skipped: {', '.join(missing_cells)}")
    if not existing_cells:
        print("No valid cells found.")
        return
    existing_kpis = get_kpis_in_list(kpis_user_list, db_config)
    if not existing_kpis:
        print("No valid KPIs found.")
        return  
    missing_kpis = set(kpis_user_list) - set(existing_kpis)
    if missing_kpis:
        print(f"The following KPIs are not found in the database and will be skipped: {', '.join(missing_kpis)}")
    kpis_values_df = get_kpis_row_values_df(db_config, existing_kpis, report_config["start_time"], report_config["end_time"], existing_cells_str)
    if kpis_values_df.empty or len(kpis_values_df) == 0:
        print("No data found for the selected KPIs and cells in the given time range.")
        return None
    pivot_df = kpis_values_df.pivot_table(index=["period_start_time", "lncel"], columns="kpi_name", values="kpi_value")
    
    pivot_df.reset_index(inplace=True)
    '''covert period_start_time to 2 columns date and time and drop period_start_time'''
    pivot_df["date"] = pivot_df["period_start_time"].dt.date
    pivot_df["time"] = pivot_df["period_start_time"].dt.time
    pivot_df.drop(columns=["period_start_time"], inplace=True)
    '''reorder columns to have date and time at the start and remove index column if exists'''
    cols = pivot_df.columns.tolist()
    cols = [col for col in cols if col != "index"]
    cols = ["date", "time"] + [col for col in cols if col not in ["date", "time"]]
    pivot_df = pivot_df[cols]
    # remove coulumn A
    pivot_df.drop(columns=["A"], inplace=True)
    return pivot_df
    
def handle_counters_export_ingestion(report_config,counters_user_list,cells_user_list):
    """
    compare the user selected counters with the ones in the database, if any of them is not in the database, inform the user and skip it, then get the values of the existing counters and export them to excel file
    compare the user selected cells with the ones in the database, if any of them is not in the database, inform the user and skip it, then get the values of the existing cells and export them to excel file
    """
    existing_counters = get_counters_in_list(counters_user_list, db_config)
    existing_cells = get_cells_in_list(cells_user_list, db_config)
    existing_cells_str = [str(n) for n in existing_cells]
    print(f"Existing counters in DB: {existing_counters}")
    print(f"Existing cells in DB: {existing_cells_str}")
    missing_counters = set(counters_user_list) - set(existing_counters)
    missing_cells = set(cells_user_list) - set(existing_cells_str)
    print(f"Missing counters: {missing_counters}")
    print(f"Missing cells: {missing_cells}")
    if not existing_cells:
        print("No valid cells found.")
        return
    if not existing_counters:
        print("No valid counters found.")
        return
    if missing_counters:
        print(f"The following counters are not found in the database and will be skipped: {', '.join(missing_counters)}")
    if missing_cells:
        print(f"The following cells are not found in the database and will be skipped: {', '.join(missing_cells)}")
    
    counters_values_df = get_raw_counters_values_df(db_config, existing_counters, report_config["start_time"], report_config["end_time"], existing_cells)
    if counters_values_df.empty or len(counters_values_df) == 0:
        print("No data found for the selected counters and cells in the given time range.")
        return None
    # Export counters_values_df to Excel file
    pivot_df = counters_values_df.pivot_table(index=["period_start_time", "lncel"], columns="counter_name", values="counter_value")
    pivot_df.reset_index(inplace=True)
    '''covert period_start_time to 2 columns date and time and drop period_start_time'''
    pivot_df["date"] = pivot_df["period_start_time"].dt.date
    pivot_df["time"] = pivot_df["period_start_time"].dt.time
    pivot_df.drop(columns=["period_start_time"], inplace=True)
    '''reorder columns to have date and time at the start and remove index column if exists'''
    cols = pivot_df.columns.tolist()
    cols = [col for col in cols if col != "index"]
    cols = ["date", "time"] + [col for col in cols if col not in ["date", "time"]]
    pivot_df = pivot_df[cols]
    # remove coulumn A 
    pivot_df.drop(columns=["A"], inplace=True)
    return pivot_df