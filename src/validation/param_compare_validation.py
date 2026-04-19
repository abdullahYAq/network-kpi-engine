def compare_template_with_xml(template_dict, new_data_dict):
    result=[]
    for class_name in template_dict:
        if class_name not in new_data_dict:
            continue
        for obj in new_data_dict[class_name]:
            for param in template_dict[class_name]:
                template_value = template_dict[class_name][param]
                new_value = obj["parameters"].get(param)
                if template_value == new_value :
                    status = "Match"
                else:
                    status = "Mismatch"
                result.append({
                    "id":obj["id"],
                    "class": class_name,
                    "parameter": param,
                    "template": template_value,
                    "actual": new_value,
                    "status": status
                })
    return result
