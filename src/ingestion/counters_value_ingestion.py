from src.db.kpi_counter_values_repository import insert_counter_values_to_db
from src.config.db_config import db_config
import pandas as pd
from src.db.counters_repository import get_all_counter_codes,get_counter_id_counter_code_map
from src.db.cells_repository import get_lncel_name_id_map,get_distname_id_map
from src.utils.counter_code_utils import extract_counter_name_code
import datetime
# === LOADING ===
def load_counter_values(csv_path):
    #csv_df = 
    csv_df = pd.read_csv(csv_path,delimiter=";")
    #csv_df.melt(id_vars=[1,2,3,3],value_vars=["ff","ss"],var_name="counter_id",value_name="value")
    """

    """
    headers_op = {"PERIOD_START_TIME","MRBTS name","LNCEL name","DN", "LNBTS name"}
    column_list = csv_df.columns.to_list()
    counter_list = [
        i
        for i in column_list
        if i not in headers_op
    ]
    return counter_list,csv_df
# === MAPPING ===
def map_cells_to_ids(df):
    lncel_map = get_lncel_name_id_map(db_config)
    df["LNCEL name"] = df["LNCEL name"].map(lncel_map)
    if validate_nan_values(df,"LNCEL name") > 0:
        raise ValueError(f"there is {validate_nan_values(df,"LNCEL name")} not in DB!")
    return df  
def map_cells_to_distname(df):
    distname_map = get_distname_id_map(db_config)
    df["distname"] = df["distname"].map(distname_map)
    if validate_nan_values(df,"distname") > 0:
        raise ValueError(f"there is {validate_nan_values(df,"distname")} not in DB!")
    return df
# === TRANSFORM ===
def rename_counter_column_to_id(counter_columns,df):
    counter_map = get_counter_id_counter_code_map(db_config)
    skeped_counters = []
    id_vars = ["PERIOD_START_TIME","LNCEL name", "DN"]
    valid_counters=[]
    rename_map = {}
    for counter in counter_columns:
        counter_extractd = extract_counter_name_code(counter)
        if counter_extractd is not None:
            counter_code=counter_extractd[1]
        else:
            counter_code=None
        if counter_code in counter_map:
            valid_counters.append(counter)
            rename_map.update({
                counter:counter_map[counter_code]
                })
        else:
            skeped_counters.append(counter) 
    print(f"valid_counters : {valid_counters}")
    print(f"skeped_counters: {skeped_counters}")  
    print(f"rename_map: {rename_map}")      
    df = df[id_vars+valid_counters]
    df=df.rename(columns=rename_map)
    return df
def transform_wide_to_long(df):
    id_vars = ["PERIOD_START_TIME", "LNCEL name", "DN"]
    column_vars = df.columns.to_list()
    value_vars = [
        col
        for col in column_vars
        if col not in id_vars
    ]
    long_df = df.melt(id_vars=id_vars,value_vars=value_vars,var_name="counter_id",value_name="counter_value")
    long_df["counter_id"] = pd.to_numeric(long_df["counter_id"],errors="coerce")
    return long_df
def rename_df_column(df,old_column, new_column):
    df=df.rename(columns={old_column:new_column})
    return df
def map_and_rename_column_from_dict(df,column_name):
    dict = get_distname_id_map(db_config)
    df["cell_id"] = df[column_name].map(dict)
    print(df)
    num_z = validate_nan_values(df,column_name)
    
    if num_z > 0:
        raise ValueError(f"there is {num_z} not in DB!")
    #df_new = df.drop(columns=[column_name])
    df["cell_id"] = pd.to_numeric(df["cell_id"],errors="coerce",downcast="integer")
    cleaned_df = df.dropna(subset=["cell_id"])
    cleaned_df["cell_id"] = pd.to_numeric(cleaned_df["cell_id"],errors="coerce",downcast="integer")
    cleaned_df["counter_value"] = pd.to_numeric(cleaned_df["counter_value"],errors="coerce",downcast="integer")
    return cleaned_df,df
# === VALIDATION ===
def validate_nan_values(df,column_name):
    num_z=df[column_name].isna().sum()
    return num_z
# === INSERT ===
def ingest_counters_values(df):
    df_reordered = df[["PERIOD_START_TIME","cell_id","counter_id","counter_value"]]
    print(df_reordered.head())
    df_reordered["PERIOD_START_TIME"] = pd.to_datetime(df_reordered["PERIOD_START_TIME"], format="%m.%d.%Y %H:%M:%S")
    df_last=df_reordered.rename(columns={"PERIOD_START_TIME":"period_start_time"})
    df_last['period_start_time'] = df_last['period_start_time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    csv_file_name = datetime.datetime.now().strftime("counter_values_%Y%m%d%H%M%S.csv")
    df_last.to_csv(csv_file_name,index=False)
    print(df_last.head())
    print(df_last.dtypes)
    insert_counter_values_to_db(csv_file_name,db_config)