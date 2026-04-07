from src.utils.counter_code_utils import extract_counter_code
def parse_expression(counter_term):
    term_dict = {}
    counter_codes_in_formula = []
    if "-" in counter_term:
        counter_term = counter_term.replace("-", "+-")
    counter_term_sign_split = counter_term.split("+")
    counter_term_sign_split = [t.strip() for t in counter_term_sign_split if t.strip()]
    for term in counter_term_sign_split:
        if term.startswith("-"):
            term_name = term[1:].strip()
            term_coef = -1
            if "*" in term_name:
                name, coef = term_name.split("*")
                term_name = name.strip()
                try:
                    term_coef *= float(coef.strip())
                except ValueError:
                    print(f"Warning: Could not convert coefficient '{coef.strip()}' to float. Defaulting to -1.")
        else:
            term_name = term.strip()
            term_coef = 1
            if "*" in term_name:
                name, coef = term_name.split("*", 1)
                term_name = name.strip()
                try:
                    term_coef *= float(coef.strip())
                except ValueError:
                    print(f"Warning: Could not convert coefficient '{coef.strip()}' to float. Defaulting to 1.")
        term_name = term_name.strip("'").strip('"')
        counter_code = extract_counter_code(term_name)
        counter_codes_in_formula.append(counter_code)
        if not counter_code:
            raise ValueError(f"Invalid counter format: {term_name}")
        if counter_code in term_dict:
            term_dict[counter_code] += term_coef    
        else:
            term_dict[counter_code] = term_coef
        term_list = [{"counter_code": c, "coef": coef} for c, coef in term_dict.items()]
    return term_list, counter_codes_in_formula
    