import pandas as pd
def convert_xl_to_dict(xl_path):
    '''
    convert excel file to dict 
    {class_name: {
            parameters : {
                    parameter1:{value: value, warning: warning},
                    parameter2: {value: value, warning: warning},
                    ...}
            type: cell_or_site
            }
        }
    '''
    dict_result = {}
    classes = []
    all_sheets = pd.read_excel(xl_path, sheet_name=None)
    for sheet_name, df in all_sheets.items():
        class_name = sheet_name
        classes.append(class_name)
        dict_result[class_name] = {}
        for _, row in df.iterrows():
            param = row["param"]
            if pd.isna(param):
                continue
            value = row["value"]
            dict_result[class_name][param] = value
    return dict_result, classes