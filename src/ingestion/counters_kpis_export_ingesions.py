from src.cli.menu import export_level_sub_menu,export_time_custom_range,export_time_range_sub_menu,export_period_sub_menu
from datetime import datetime, timedelta
def get_report_config():
    level = export_level_sub_menu() # cell level, site level
    period = export_period_sub_menu() # daily,hourly
    time_range = export_time_range_sub_menu() # last 24 hours, last 7 days, last 30 days, custom range
    if time_range == "custom range":
        start_time, end_time = export_time_custom_range()
    elif time_range == "last 24 hours":
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=24)
    elif time_range == "last 7 days":
        end_time = datetime.now()
        start_time = end_time - timedelta(days=7)
    elif time_range == "last 30 days":
        end_time = datetime.now()
        start_time = end_time - timedelta(days=30)
    print(f"Level: {level}, Period: {period}, Time Range: {time_range}, Start Time: {start_time}, End Time: {end_time}")
def handle_kpis_export_ingestion():
    pass
def handle_counters_export_ingestion():
    pass