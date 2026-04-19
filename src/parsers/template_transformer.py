import collections
def transform_parameters(parameters_dict):
    """
    Transform the parameters dictionary to the desired format.
    Args:
        class_name: {
            parameters : {
                    parameter1:[value1, value2,...],
                    parameter2: [value1, value2,...],
                    ...}
            type: cell_or_site
            }
    Returns:
        {class_name: {
            parameters : {
                    parameter1:{value: value, warning: warning},
                    parameter2: {value: value, warning: warning},
                    ...}
            type: cell_or_site
            }
        }
    """
    transformed_dict = {}
    for class_name, class_info in parameters_dict.items():
        transformed_dict[class_name] = {"type": class_info["type"], "parameters": {}}
        for param_name, param_values in class_info["parameters"].items():
            # Here you can implement your logic to determine the warning based on the parameter values
            if not param_values:
                most_common_value = None
                warning = "No values"
                transformed_dict[class_name]["parameters"][param_name] = {"value": most_common_value, "warning": warning}
                continue
            param_counter = collections.Counter(param_values)
            max_count = max(param_counter.values())
            most_common_value = max(param_counter.items(), key=lambda x: x[1])[0]
            warning = "Inconsistent" if max_count < len(param_values) else "ok"
            transformed_dict[class_name]["parameters"][param_name] = {"value": most_common_value, "warning": warning}
    return transformed_dict
def flatten_transformed_dict(transformed_dict):
    flattened_list = []
    for class_name, class_info in transformed_dict.items():
        for param_name, param_data in class_info["parameters"].items():
            flattened_list.append({
                "class_name": class_name,
                "param": param_name,
                "value": param_data["value"],
                "warning": param_data["warning"],
                "type": class_info["type"]
                })
    return flattened_list
def group_by_class(flattened_list):
    grouped_dict = {}
    for row in flattened_list:
        class_name = row["class_name"]
        if class_name not in grouped_dict:
            grouped_dict[class_name] = []
        grouped_dict[class_name].append(row)
    return grouped_dict


