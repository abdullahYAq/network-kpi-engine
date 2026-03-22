from src.utils.counter_code_utils import extract_counter_code
def extract_counters_from_csv_header(csv_path):
    headers_op = {"PERIOD_START_TIME","MRBTS name","LNCEL name","DN", "LNBTS name"}
    counters_dict ={}
    with open(csv_path) as csv_file:
        header_line = csv_file.readline()
        print(header_line)
        column_values = header_line.split(";")
        print(column_values)
        for v in column_values:
            if v.strip() not in headers_op:
                counter_extracted = extract_counter_code(v)
                if counter_extracted:
                    counters_dict.update({counter_extracted[0]:counter_extracted[1]})
        return counters_dict