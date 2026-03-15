import xml.etree.ElementTree as ET
from src.utils.distname_utils import distName_to_dict
def extract_selected_objects_stream(xml_path, selected_classes_set, obj_p):
    scanned = 0
    added = 0
    try:
        for event, elem in ET.iterparse(xml_path, events=("end",)):
            #tag_name = elem.tag.split("}")[-1]  # Remove namespace
            if elem.tag.endswith("managedObject"):
                scanned += 1
                if scanned % 100000 == 0:
                    print(f"{scanned} objects scanned | {added} objects added")
                class_name = elem.get("class")
                
                if class_name not in selected_classes_set:
                    elem.clear()
                    continue
                
                distName = elem.get("distName")
                object_info = None
                
                for child in elem:
                    if child.tag.endswith("p") and child.get("name") in obj_p:
                        if object_info is None:
                            object_info = {
                                "class": class_name,
                                "distName": distName
                            }
                            object_info.update(distName_to_dict(distName))
                        p_key = child.get("name")
                        if p_key is None:
                            continue
                        p_value = child.text.strip() if child.text is not None else ""
                        object_info[p_key] = p_value
                if object_info is not None:
                    added += 1
                    yield object_info

                
                elem.clear()
    except Exception as e:
        print(e)  
def extract_selected_objects(xml_path, selected_classes,object_counter):   
    counter = 0
    scanned = 0
    result ={}
    schema = {}
    selected_classes_set = set(selected_classes)
    try:
        for event, elem in ET.iterparse(xml_path, events=("end",)):
            #tag_name = elem.tag.split("}")[-1]  # Remove namespace
            if elem.tag.endswith("managedObject"):
                scanned += 1
                if scanned % 100000 == 0:
                    print("scanned:", scanned, ", out of total", object_counter, " | matched:", counter)
                class_name = elem.get("class")
                if class_name in selected_classes_set:
                    counter += 1
                    #print("processing object:", class_name)
                    if class_name not in result:
                        result[class_name] = []
                        schema[class_name] = set()  
                    distName = elem.get("distName")
                    object_info = {
                            "class": class_name,
                            "distName": distName
                    }                   
                    object_info.update(distName_to_dict(distName))
                    for key in object_info:
                        if key not in {"class", "distName", "PLMN"}:
                            schema[class_name].add(key)
                    for child in elem:                          
                        #p_tag = child.tag.split("}")[-1]
                        if child.tag.endswith("p"):
                            p_key = child.get("name")
                            if p_key is None:
                                continue
                            p_value = child.text.strip() if child.text is not None else ""
                            object_info[p_key] = p_value
                            schema[class_name].add(p_key)
                    result[class_name].append(object_info)                   
                elem.clear()
             # Clear the element to save memory
            #if counter > 2:
                #break
        print("loop finished")
        print("objects found:", scanned)   
        return result, schema, scanned
    except KeyboardInterrupt:
        print("Interrupted by user")
        return result, schema, scanned
def extract_classes(xml_path):
    """
    Extract class names from an XML file.
    Args:
        xml_path (str): path to xml file
    Returns:
        list: list of class names
    """
    counter=0
    classes_list = set()
    try:
        """xml_file = ET.open(xml_path)
        tree = ET.parse(xml_file)
        """
        
        for event, elem in ET.iterparse(xml_path, events=("end",)):
            #tag_name = elem.tag.split("}")[-1]  # Remove namespace
            if elem.tag.endswith("managedObject"):
                classes_list.add(elem.get("class"))
                counter += 1
                if counter % 100000 == 0:
                    print("processed:", counter)
                elem.clear()  # Clear the element to save memory
        return classes_list, counter         
    except Exception as e:
        print(f"Error parsing XML file: {e}")
        return classes_list, counter