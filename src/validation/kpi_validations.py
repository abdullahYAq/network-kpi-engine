import pandas as pd
from src.parsers.kpi_formula_parser import parse_expression
from src.utils.expression_utils import analyze_formula
def validate_kpi_template_statics(kpi_df):
    expected_columns = ["kpi_name","numerator (ratio only)","denominator (ratio only)","expression (expression only)","multiplier","description","tech_name"]
    errors = []
    warnings = []
    missing_columns = set(expected_columns) - set(kpi_df.columns)
    missing = list(missing_columns)
    errors = [ 
        (0, col, "missing column", "error")
        for col in missing
    ]
    if missing:
        errors_df = pd.DataFrame(errors, columns=["row_number", "column", "message", "type"])
        warning_df = pd.DataFrame(warnings, columns=["row_number", "column", "message", "type"])
        return errors_df, warning_df    
    kpi_df["kpi_type"] = kpi_df["kpi_type"].str.strip().str.lower()
    non_empty_df = kpi_df.dropna(how="all")

    if non_empty_df.empty:
        errors = [(0, "-", "Excel contains no valid data", "error")]
        errors_df = pd.DataFrame(errors, columns=["row_number", "column", "message", "type"])
        warnings_df = pd.DataFrame(columns=["row_number", "column", "message", "type"])
        return errors_df, warnings_df
    invalid = kpi_df[~kpi_df["kpi_type"].isin(["ratio (num/den)", "expression"])]
    invalid_index = list(invalid.index)
    errors.extend(
        (i+2,"kpi_type","invalid value","error")
        for i in invalid_index
    )
    empty_num = kpi_df[(kpi_df["kpi_type"] == "ratio (num/den)") & (is_empty_series(kpi_df["numerator (ratio only)"]))]
    empty_den = kpi_df[(kpi_df["kpi_type"] == "ratio (num/den)") & (is_empty_series(kpi_df["denominator (ratio only)"]))]
    empty_exp = kpi_df[(kpi_df["kpi_type"] == "expression") & (is_empty_series(kpi_df["expression (expression only)"]))]
    empty_num_index = list(empty_num.index)
    empty_den_index = list(empty_den.index)
    empty_exp_index = list(empty_exp.index)
    errors.extend(
        (i+2,"numerator (ratio only)","missing value","error")
        for i in empty_num_index
    )
    errors.extend(
        (i+2,"denominator (ratio only)","missing value","error")
        for i in empty_den_index
    )
    errors.extend(
        (i+2,"expression (expression only)","missing value","error")
        for i in empty_exp_index
    )
    forbidden_exp_num = kpi_df[(kpi_df["kpi_type"] == "expression") & (~is_empty_series(kpi_df["numerator (ratio only)"]))]
    forbidden_exp_num_index = list(forbidden_exp_num.index)
    errors.extend(
        (i+2,"numerator (ratio only)","should be empty when kpi type is expression","error")
        for i in forbidden_exp_num_index
    )
    forbidden_exp_den = kpi_df[(kpi_df["kpi_type"] == "expression") & (~is_empty_series(kpi_df["denominator (ratio only)"]))]
    forbidden_exp_den_index = list(forbidden_exp_den.index)
    errors.extend(
        (i+2,"denominator (ratio only)","should be empty when kpi type is expression","error")
        for i in forbidden_exp_den_index
    )
    forbidden_ratio_exp = kpi_df[(kpi_df["kpi_type"] == "ratio (num/den)") & (~is_empty_series(kpi_df["expression (expression only)"]))]
    forbidden_ratio_exp_index = list(forbidden_ratio_exp.index) 
    errors.extend(
        (i+2,"expression (expression only)","should be empty when kpi type is ratio","error")
        for i in forbidden_ratio_exp_index
    )
    empty_tech = kpi_df[is_empty_series(kpi_df["tech_name"])]
    invalid_tech = kpi_df[
        (~kpi_df["tech_name"].isin(["LTE","UMTS","GSM","NSANR"]))
        & (~is_empty_series(kpi_df["tech_name"]))
    ]
    empty_tech_index = list(empty_tech.index)
    invalid_tech_index = list(invalid_tech.index)
    errors.extend(
        (i+2,"tech_name","missing value","error")
        for i in empty_tech_index
    )
    errors.extend(
        (i+2,"tech_name","invalid value","error")
        for i in invalid_tech_index
    )
    empty_name = kpi_df[is_empty_series(kpi_df["kpi_name"])]
    empty_name_index = list(empty_name.index)
    errors.extend(
        (i+2,"kpi_name","missing value","error")
        for i in empty_name_index
    )
    empty_desc = kpi_df[is_empty_series(kpi_df["description"])]
    empty_desc_index = list(empty_desc.index)
    warnings = [
        (i+2,"description","missing description","warning")
        for i in empty_desc_index
    ]
    multipler_zero = kpi_df[(kpi_df["multiplier"].notna()) & (kpi_df["multiplier"] == 0)]
    multipler_zero_index = list(multipler_zero.index)
    warnings.extend(
        (i+2,"multiplier","multiplier is zero, kpi value will be zero","warning")
        for i in multipler_zero_index
    )
    multipler_negative = kpi_df[(kpi_df["multiplier"] < 0) & ~kpi_df["multiplier"].isna()]
    multipler_negative_index = list(multipler_negative.index)
    warnings.extend(
        (i+2,"multiplier","multiplier is negative, kpi value will be negative","warning")
        for i in multipler_negative_index
    )
    kpi_df["multiplier"] = pd.to_numeric(kpi_df["multiplier"], errors="coerce")
    errors_df = pd.DataFrame(errors,columns=["row_number","column", "message","type"])
    warning_df=pd.DataFrame(warnings,columns=["row_number","column", "message","type"])
    return errors_df, warning_df
def is_empty_series(series):
    return series.isna() | (series.astype(str).str.strip() == "")
def validate_kpi_template_dynamic(kpi_df, db_counters):
    row_data = []
    errors = []
    for index, row in kpi_df.iterrows():
        expression_counters = []
        numerator_counters = []
        denominator_counters = []
        if row["kpi_type"] == "ratio (num/den)":
            numerator = row["numerator (ratio only)"]
            denominator = row["denominator (ratio only)"]
            num_list, numerator_counters = parse_expression(numerator)
            den_list, denominator_counters = parse_expression(denominator)
        elif row["kpi_type"] == "expression":
            expression = row["expression (expression only)"]
            exp_list, expression_counters = parse_expression(expression)
        row_data.append({
            "row_number": index + 2,
            "numerator_counters": set(numerator_counters),
            "denominator_counters": set(denominator_counters),
            "expression_counters": set(expression_counters)
        })
    all_counters = set()
    for data in row_data:
        all_counters.update(data["numerator_counters"])
        all_counters.update(data["denominator_counters"])
        all_counters.update(data["expression_counters"])
    missing_counters = all_counters - set(db_counters)
    for row in row_data:
        for counter in row["numerator_counters"]:
            if counter in missing_counters:
                errors.append((row["row_number"], "numerator (ratio only)", f"counter '{counter}' not found in database", "error"))
        for counter in row["denominator_counters"]:
            if counter in missing_counters:
                errors.append((row["row_number"], "denominator (ratio only)", f"counter '{counter}' not found in database", "error"))
        for counter in row["expression_counters"]:
            if counter in missing_counters:
                errors.append((row["row_number"], "expression (expression only)", f"counter '{counter}' not found in database", "error"))
    errors_df = pd.DataFrame(errors, columns=["row_number", "column", "message", "type"])
    return errors_df, all_counters
def validate_expression_syntax(expression):
    expression_tremed = expression.strip()
    allowed_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_+-'()")
    if not set(expression_tremed).issubset(allowed_chars):
        return False
    # check for ++ -- ** -+ +- and other invalid combinations
    invalid_combinations = ["++", "--", "**", "-+", "+-", "()", "(+", "(-", "+)", "-)"]
    for combo in invalid_combinations:
        if combo in expression_tremed:
            return False
    return True
def validate_kpi_template_statics_new(kpi_df):
    expected_columns = ["kpi_name", "formula","description","tech_name"]
    errors = []
    warnings = []
    missing_columns = set(expected_columns) - set(kpi_df.columns)
    missing = list(missing_columns)
    errors = [ 
        (0, col, "missing column", "error")
        for col in missing
    ]
    if missing:
        errors_df = pd.DataFrame(errors, columns=["row_number", "column", "message", "type"])
        warning_df = pd.DataFrame(warnings, columns=["row_number", "column", "message", "type"])
        return errors_df, warning_df
    empty_desc = kpi_df[is_empty_series(kpi_df["description"])]
    empty_desc_index = list(empty_desc.index)
    warnings = [
        (i+2,"description","missing description","warning")
        for i in empty_desc_index
    ]
    empty_tech = kpi_df[is_empty_series(kpi_df["tech_name"])]
    invalid_tech = kpi_df[
        (~kpi_df["tech_name"].isin(["LTE","UMTS","GSM","NSANR"]))
        & (~is_empty_series(kpi_df["tech_name"]))
    ]
    empty_tech_index = list(empty_tech.index)
    invalid_tech_index = list(invalid_tech.index)
    errors.extend(
        (i+2,"tech_name","missing value","error")
        for i in empty_tech_index
    )
    errors.extend(
        (i+2,"tech_name","invalid value","error")
        for i in invalid_tech_index
    )
    empty_name = kpi_df[is_empty_series(kpi_df["kpi_name"])]
    empty_name_index = list(empty_name.index)
    errors.extend(
        (i+2,"kpi_name","missing value","error")
        for i in empty_name_index
    )
    empty_formula = kpi_df[is_empty_series(kpi_df["formula"])]
    empty_formula_index = list(empty_formula.index)
    errors.extend(
        (i+2,"formula","No formula added to KPI", "error")
        for i in empty_formula_index
    )
    errors_df = pd.DataFrame(errors,columns=["row_number","column", "message","type"])
    warning_df=pd.DataFrame(warnings,columns=["row_number","column", "message","type"])
    return errors_df, warning_df
def validate_kpi_template_dynamic_new(kpi_df, db_counters,kpi_names):
    row_data = []
    errors = []
    graph = {}
    for index, row in kpi_df.iterrows():
        formula = row["formula"]
        counter_kpi_dict = analyze_formula(formula)
        row_data.append({
            "row_number":index+2,
            "counters": counter_kpi_dict["counter_codes"],
            "kpi_dependencies" : counter_kpi_dict["kpi_dependencies"]
        })
        graph[row["kpi_name"]] = counter_kpi_dict["kpi_dependencies"]
    all_counters = set()
    all_kpis = set()
    db_counters_set = set(db_counters)
    kpi_names_set = set(kpi_names)
    for data in row_data:
        all_counters.update(data["counters"])
        all_kpis.update(data["kpi_dependencies"])
    missing_counter = all_counters - db_counters_set
    current_kpis = set(kpi_df["kpi_name"])

    missing_kpi = all_kpis - (kpi_names_set | current_kpis)
    for row in row_data:
        for counter in set(row["counters"]):
            if counter in missing_counter:
                errors.append((row["row_number"], "formula", f"counter '{counter}' not found in database", "error"))
        for kpi in row["kpi_dependencies"]:
            if kpi in missing_kpi:
                errors.append((row["row_number"], "formula", f"KPI '{kpi}' not found in database", "error"))  
    if has_cycle(graph):
        errors.append(("all","formula","Circular dependency detected","error"))
    
    errors_df = pd.DataFrame(errors,columns=["row_number","column", "message","type"])
    return errors_df
def has_cycle(graph):
    for node in graph:
        if df(node,graph,[]):
            return True
    return False
def df(node,graph, path):
    if node in path:
        return True
    path.append(node)
    for dep in graph.get(node,[]):
        if df(dep,graph,path):
            return True
    path.pop()
    return False
         