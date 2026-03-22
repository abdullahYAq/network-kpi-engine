def extract_counter_code(value):
    counter_name, *rest = value.split("(")
    
    if rest:
        counter_code = rest[0].rstrip(")")
        counter_extracted = (counter_name.strip(),counter_code.strip())
        return counter_extracted
    else:
        return None