import re
def extract_counter_codes(formula):
    counters_list = re.findall(r"M\d+(?:[A-Z]\d+)?",formula)
    return counters_list
def analyze_formula(formula):
    result_dict = {
        "counter_codes": [],
        "kpi_dependencies": []
    }
    #counter_codes = re.findall(r"M\d+(?:[A-Z]\d+)?", formula)
    #terms = [t.strip() for t in terms if t.strip()]
    expresion_list = re.findall(r"'([^']+)'",formula)
    for term in expresion_list:
        counter = extract_counter_codes(term)
        if counter:
            result_dict["counter_codes"].extend(counter)
        else:
            result_dict["kpi_dependencies"].append(term)
    return result_dict